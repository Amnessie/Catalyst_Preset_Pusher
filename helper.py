"""Catalyst Preset Picker helper.

Serves the picker page on http://127.0.0.1:8765 and adds two actions:
  Load to amp:       the page sends a preset here, it is saved under "Loaded presets", and
                     Catalyst Edit is told to open it (the same as Ctrl+O -> pick the file -> Open).
  Save to amp slot:  loads it as above, then uses Catalyst Edit's own "Save Current Preset to
                     Catalyst" window (Ctrl+D) to pick the bank and channel and press SAVE.
Catalyst Edit's own screens are read through Windows UI Automation (via PowerShell), so the
helper can check the right sound loaded and the right slot is picked before anything is saved.

Start it with "Start Preset Picker.bat" or:  python helper.py
Only uses the Python standard library. Windows only.
"""
import ctypes
import ctypes.wintypes as wt
import http.server
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser

HOST, PORT = "127.0.0.1", 8765
HERE = os.path.dirname(os.path.abspath(__file__))
LOADED_DIR = os.path.join(HERE, "Loaded presets")
PAGE = "Catalyst Preset Picker.html"
CATALYST_TITLE = "Catalyst Edit"
CATALYST_EXE = "catalyst edit.exe"

# ---------------------------------------------------------------- Win32 bits
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
user32.EnumWindows.argtypes = [WNDENUMPROC, wt.LPARAM]
user32.GetWindowTextW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
user32.GetClassNameW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
user32.IsWindowVisible.argtypes = [wt.HWND]
user32.IsIconic.argtypes = [wt.HWND]
user32.ShowWindow.argtypes = [wt.HWND, ctypes.c_int]
user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
user32.GetWindowThreadProcessId.restype = wt.DWORD
user32.GetForegroundWindow.restype = wt.HWND
user32.SetForegroundWindow.argtypes = [wt.HWND]
user32.BringWindowToTop.argtypes = [wt.HWND]
user32.AttachThreadInput.argtypes = [wt.DWORD, wt.DWORD, wt.BOOL]
user32.GetDlgItem.argtypes = [wt.HWND, ctypes.c_int]
user32.GetDlgItem.restype = wt.HWND
user32.FindWindowExW.argtypes = [wt.HWND, wt.HWND, wt.LPCWSTR, wt.LPCWSTR]
user32.FindWindowExW.restype = wt.HWND
user32.SendMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.SendMessageW.restype = ctypes.c_ssize_t
user32.PostMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.IsWindow.argtypes = [wt.HWND]
user32.keybd_event.argtypes = [wt.BYTE, wt.BYTE, wt.DWORD, ctypes.c_size_t]
user32.mouse_event.argtypes = [wt.DWORD, wt.DWORD, wt.DWORD, wt.DWORD, ctypes.c_size_t]
user32.GetWindowRect.argtypes = [wt.HWND, ctypes.POINTER(wt.RECT)]
user32.WindowFromPoint.argtypes = [wt.POINT]
user32.WindowFromPoint.restype = wt.HWND
user32.GetAncestor.argtypes = [wt.HWND, wt.UINT]
user32.GetAncestor.restype = wt.HWND
user32.GetCursorPos.argtypes = [ctypes.POINTER(wt.POINT)]
user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetProcessDPIAware()  # so window positions match what UI Automation reports
kernel32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
kernel32.OpenProcess.restype = wt.HANDLE
kernel32.QueryFullProcessImageNameW.argtypes = [wt.HANDLE, wt.DWORD, wt.LPWSTR, ctypes.POINTER(wt.DWORD)]
kernel32.CloseHandle.argtypes = [wt.HANDLE]
kernel32.GetCurrentThreadId.restype = wt.DWORD

SW_RESTORE = 9
WM_SETTEXT = 0x000C
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL, VK_MENU, VK_O, VK_D = 0x11, 0x12, 0x4F, 0x44
MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP = 0x0002, 0x0004
GA_ROOT = 2
IDOK, IDCANCEL = 1, 2
ID_FILENAME_COMBO = 1148   # file name box in the Windows Open dialog
ID_FILENAME_EDIT_OLD = 1152
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


def window_text(hwnd):
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value


def class_name(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, 256)
    return buf.value


def window_pid(hwnd):
    pid = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def process_exe(pid):
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wt.DWORD(1024)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value).lower()
        return ""
    finally:
        kernel32.CloseHandle(handle)


def top_windows():
    found = []

    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found


def find_catalyst_window():
    for hwnd in top_windows():
        if window_text(hwnd) == CATALYST_TITLE and process_exe(window_pid(hwnd)) == CATALYST_EXE:
            return hwnd
    return None


def find_dialog(pid):
    for hwnd in top_windows():
        if class_name(hwnd) == "#32770" and window_pid(hwnd) == pid:
            return hwnd
    return None


def wait_for(fn, timeout, interval=0.05):
    end = time.time() + timeout
    while time.time() < end:
        result = fn()
        if result:
            return result
        time.sleep(interval)
    return None


def bring_to_front(hwnd):
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
    fg = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg, None) if fg else 0
    me = kernel32.GetCurrentThreadId()
    attached = bool(fg_thread) and fg_thread != me and user32.AttachThreadInput(me, fg_thread, True)
    try:
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
    finally:
        if attached:
            user32.AttachThreadInput(me, fg_thread, False)
    if user32.GetForegroundWindow() != hwnd:
        # Windows refuses focus changes from background apps; a tapped Alt key lifts that block.
        user32.keybd_event(VK_MENU, 0, 0, 0)
        user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
        user32.SetForegroundWindow(hwnd)
    return wait_for(lambda: user32.GetForegroundWindow() == hwnd, 1.5)


def press_ctrl(key):
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(key, 0, 0, 0)
    user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)


def click_title_bar(hwnd):
    """Clicks the middle of Catalyst Edit's title bar, which closes its in-app popups without choosing anything."""
    rect = wt.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    x, y = (rect.left + rect.right) // 2, rect.top + 22
    under = user32.WindowFromPoint(wt.POINT(x, y))
    if not under or user32.GetAncestor(under, GA_ROOT) != hwnd:
        return False
    old = wt.POINT()
    user32.GetCursorPos(ctypes.byref(old))
    user32.SetCursorPos(x, y)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.4)
    user32.SetCursorPos(old.x, old.y)
    return True


# ---------------------------------------------------------------- reading Catalyst Edit's screen
# Catalyst Edit draws its own windows (WPF), so its preset name, popups and the "Choose Save
# Location" controls are only reachable through UI Automation. Python's standard library has no
# UI Automation, so this small PowerShell script does that part. Its buttons have no names, so
# each is found by the text label drawn on top of it. Uses single quotes only (see run_uia).
UIA_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$Scope = [System.Windows.Automation.TreeScope]
$CT = [System.Windows.Automation.ControlType]
$Any = [System.Windows.Automation.Condition]::TrueCondition
$req = $env:CPP_REQ | ConvertFrom-Json
$root = $AE::FromHandle([IntPtr][long]$req.hwnd)

function Reply($o) { Write-Output ('RESULT ' + ($o | ConvertTo-Json -Compress)); exit 0 }
function Items($el) { @($el.FindAll($Scope::Descendants, $Any)) }
function Popups { @($root.FindAll($Scope::Children, (New-Object System.Windows.Automation.PropertyCondition($AE::ClassNameProperty, 'Popup')))) }
function Texts($el) { @(Items $el | Where-Object { $_.Current.ControlType -eq $CT::Text -and $_.Current.Name } | ForEach-Object { $_.Current.Name } | Select-Object -Unique) }
function Until([scriptblock]$check, [double]$seconds) {
  $end = (Get-Date).AddSeconds($seconds)
  while ($true) {
    $r = & $check
    if ($r) { return $r }
    if ((Get-Date) -gt $end) { return $null }
    Start-Sleep -Milliseconds 100
  }
}
function Press($button) { $button.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke() }
function ButtonUnder($items, [string]$label) {
  $t = $items | Where-Object { $_.Current.ControlType -eq $CT::Text -and $_.Current.Name -eq $label } | Select-Object -First 1
  if (-not $t) { return $null }
  $r = $t.Current.BoundingRectangle
  $items | Where-Object { $_.Current.ControlType -eq $CT::Button -and ($_.Current.Name -eq '' -or $_.Current.Name -eq $label) -and $_.Current.BoundingRectangle.IntersectsWith($r) } | Select-Object -First 1
}
function PresetName {
  $edits = @(Items $root | Where-Object { $_.Current.ControlType -eq $CT::Edit } | Sort-Object { $_.Current.BoundingRectangle.Width } -Descending)
  if ($edits.Count) { $edits[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value } else { $null }
}
function SavePopup { Popups | Where-Object { (Texts $_) -contains 'Choose Save Location' } | Select-Object -First 1 }
function BankOf($items) {
  foreach ($b in ($items | Where-Object { $_.Current.ControlType -eq $CT::Button -and -not $_.Current.Name })) {
    $r = $b.Current.BoundingRectangle
    $t = $items | Where-Object { $_.Current.ControlType -eq $CT::Text -and $_.Current.Name -match '^[1-9]$' -and $_.Current.BoundingRectangle -eq $r } | Select-Object -First 1
    if ($t) { return @{ button = $b; bank = [int]$t.Current.Name } }
  }
  $null
}
function ChannelLit($items, [string]$ch) {
  $b = ButtonUnder $items $ch
  if (-not $b) { return $false }
  $r = $b.Current.BoundingRectangle
  [bool]($items | Where-Object { $_.Current.ControlType -eq $CT::Image -and -not $_.Current.IsOffscreen -and $_.Current.BoundingRectangle -eq $r })
}
function Fail([string]$stage, [string]$message) { Reply @{ ok = $false; stage = $stage; message = $message } }

if ($req.action -eq 'state') {
  Reply @{ ok = $true; name = (PresetName); popups = @(Popups | ForEach-Object { (Texts $_) -join ' / ' }) }
}

if ($req.action -eq 'save') {
  $pop = Until { SavePopup } 4
  if (-not $pop) {
    # With the amp off or unplugged, Catalyst Edit lights neither channel button and can't save.
    $main = Items $root
    if (-not ((ChannelLit $main 'A') -or (ChannelLit $main 'B'))) {
      Fail 'open' 'Catalyst Edit does not seem to be connected to your amp. Turn the amp on, check the USB cable, wait until Catalyst Edit shows a bank and channel, then try again.'
    }
    Fail 'open' 'Catalyst Edit did not open its Choose Save Location window (Ctrl+D).'
  }
  $bank = BankOf (Items $pop)
  if (-not $bank) { Fail 'bank' 'Could not find the bank selector in the save window.' }
  if ($bank.bank -ne $req.bank) {
    Press $bank.button
    $choice = Until { Items $pop | Where-Object { $_.Current.ControlType -eq $CT::Button -and $_.Current.Name -eq [string]$req.bank } | Select-Object -First 1 } 3
    if (-not $choice) { Fail 'bank' ('Bank ' + $req.bank + ' is not in the bank list.') }
    Press $choice
    if (-not (Until { $b = BankOf (Items $pop); $b -and $b.bank -eq $req.bank } 3)) { Fail 'bank' 'Could not switch the bank.' }
  }
  $chButton = ButtonUnder (Items $pop) $req.channel
  if (-not $chButton) { Fail 'channel' ('Could not find channel ' + $req.channel + ' in the save window.') }
  Press $chButton
  if (-not (Until { ChannelLit (Items $pop) $req.channel } 3)) { Fail 'channel' 'Could not switch the channel.' }

  $items = Items $pop
  $now = BankOf $items
  if (-not $now -or $now.bank -ne $req.bank -or -not (ChannelLit $items $req.channel)) { Fail 'check' 'The save window did not show the slot that was asked for.' }
  if ($req.dryRun) { Reply @{ ok = $true; dryRun = $true; bank = $now.bank; channel = $req.channel } }

  $save = ButtonUnder $items 'SAVE'
  if (-not $save) { Fail 'save' 'Could not find the SAVE button.' }
  Press $save
  $script:confirmed = $false
  $outcome = Until {
    $all = Texts $root
    if ($all -contains 'Preset Save Succeeded') { return 'saved' }
    if ($all -contains 'Save Failure') { return 'failed' }
    foreach ($p in Popups) {
      if ((Texts $p) -contains 'Overwrite Device Preset') {
        $yes = ButtonUnder (Items $p) 'Yes'
        if (-not $yes) { $yes = ButtonUnder (Items $p) 'Continue' }
        if ($yes) { Press $yes; $script:confirmed = $true }
      }
    }
    $null
  } 10
  if ($outcome -eq 'failed') { Fail 'save' 'Catalyst Edit says: An error occurred while saving the preset.' }
  Reply @{ ok = $true; saved = ($outcome -eq 'saved'); confirmed = $script:confirmed; stillOpen = [bool](SavePopup); popups = @(Popups | ForEach-Object { (Texts $_) -join ' / ' }) }
}
Fail 'request' 'Unknown request.'
"""
assert '"' not in UIA_SCRIPT


def run_uia(action, hwnd, timeout=40, **params):
    """Runs UIA_SCRIPT for one action. Returns its reply dict, or {"ok": False, "message": ...}."""
    env = dict(os.environ, CPP_REQ=json.dumps({"action": action, "hwnd": int(hwnd), **params}))
    try:
        # Passed as one -Command argument; the script has no double quotes, so nothing needs escaping.
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", UIA_SCRIPT],
            capture_output=True, text=True, env=env, timeout=timeout,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"ok": False, "stage": "uia", "message": f"Couldn't read Catalyst Edit's screen ({e.__class__.__name__})."}
    for line in reversed(out.stdout.splitlines()):
        if line.startswith("RESULT "):
            return json.loads(line[7:])
    err = (out.stderr.strip().splitlines() or ["no output"])[0]
    return {"ok": False, "stage": "uia", "message": f"Couldn't read Catalyst Edit's screen: {err}"}


def filename_box(dialog):
    combo = user32.GetDlgItem(dialog, ID_FILENAME_COMBO)
    if combo:
        inner = user32.FindWindowExW(combo, None, "ComboBox", None)
        edit = user32.FindWindowExW(inner or combo, None, "Edit", None)
        if edit:
            return edit
    return user32.GetDlgItem(dialog, ID_FILENAME_EDIT_OLD)


def read_text(hwnd):
    length = user32.SendMessageW(hwnd, WM_GETTEXTLENGTH, 0, 0)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.SendMessageW(hwnd, WM_GETTEXT, length + 1, ctypes.addressof(buf))
    return buf.value


def other_dialog(pid, exclude):
    for hwnd in top_windows():
        if hwnd != exclude and class_name(hwnd) == "#32770" and window_pid(hwnd) == pid:
            return hwnd
    return None


def cancel_dialog(dialog):
    if user32.IsWindow(dialog):
        user32.PostMessageW(user32.GetDlgItem(dialog, IDCANCEL), BM_CLICK, 0, 0)
        wait_for(lambda: not user32.IsWindow(dialog), 2)


def dialog_message(dialog):
    texts = []
    child = user32.FindWindowExW(dialog, None, "Static", None)
    while child:
        t = window_text(child).strip()
        if t:
            texts.append(t)
        child = user32.FindWindowExW(dialog, child, "Static", None)
    return " ".join(texts) or window_text(dialog)


def as_list(v):
    return v if isinstance(v, list) else [v] if v else []


def popup_problem(state):
    """A message for the user if Catalyst Edit is showing one of its own popups, else None."""
    for text in as_list(state.get("popups")):
        if "Unsaved Changes" in text:
            return ("Catalyst Edit is asking about unsaved changes to the current sound. "
                    "Answer it in Catalyst Edit (Yes throws your tweaks away and loads the new sound).")
        if text:
            return "Catalyst Edit has a popup open: " + text[:120]
    return None


def same_name(a, b):
    return (a or "").strip().casefold() == (b or "").strip().casefold()


def load_in_catalyst_edit(path, name, restore_focus=True):
    """Opens a .catl6p in Catalyst Edit through its Load Preset dialog. Returns (ok, message)."""
    hwnd = find_catalyst_window()
    if not hwnd:
        return False, "Catalyst Edit isn't open. Start it, connect the amp, and try again."
    pid = window_pid(hwnd)
    if find_dialog(pid):
        return False, "Catalyst Edit has a window or message open. Close it and try again."

    previous = user32.GetForegroundWindow()
    if not bring_to_front(hwnd):
        return False, "Couldn't bring Catalyst Edit to the front. Click on it once and try again."
    press_ctrl(VK_O)
    dialog = wait_for(lambda: find_dialog(pid), 4)
    if not dialog:
        problem = popup_problem(run_uia("state", hwnd))
        return False, problem or "Catalyst Edit didn't open its Load Preset window (Ctrl+O)."

    box = filename_box(dialog)
    if not box:
        cancel_dialog(dialog)
        return False, "Found the Load Preset window but not its file name box. Pick the file by hand."
    # The buffer must stay referenced until SendMessage returns, or Windows reads freed memory.
    path_buf = ctypes.create_unicode_buffer(path)
    user32.SendMessageW(box, WM_SETTEXT, 0, ctypes.addressof(path_buf))
    if read_text(box) != path:
        cancel_dialog(dialog)
        return False, "Couldn't type the file name into Catalyst Edit's Load window, so it was cancelled."
    user32.PostMessageW(user32.GetDlgItem(dialog, IDOK), BM_CLICK, 0, 0)
    if not wait_for(lambda: not user32.IsWindow(dialog), 5):
        popup = other_dialog(pid, dialog)
        message = ("Catalyst Edit says: " + dialog_message(popup)) if popup else "The Load Preset window didn't close."
        if popup:
            user32.PostMessageW(popup, WM_CLOSE, 0, 0)
            wait_for(lambda: not user32.IsWindow(popup), 2)
        cancel_dialog(dialog)
        return False, message

    # Catalyst Edit shows a message box if it rejects the file.
    popup = wait_for(lambda: find_dialog(pid), 1.0)
    if popup:
        return False, "Catalyst Edit says: " + dialog_message(popup)

    # Check it really took: no popup of its own waiting, and the preset name now matches.
    state = run_uia("state", hwnd)
    if state.get("ok"):
        problem = popup_problem(state)
        if problem:
            return False, problem
        if not same_name(state.get("name"), name):
            return False, f"Catalyst Edit shows \"{state.get('name')}\" instead of \"{name}\". Try loading again."
    if restore_focus and previous and previous != hwnd:
        bring_to_front(previous)
    return True, "Loaded into Catalyst Edit."


def save_to_amp_slot(path, name, bank, channel, dry_run=False):
    """Loads the preset, then saves it to bank/channel on the amp with Catalyst Edit's own save window.
    With dry_run it picks the slot, checks it, and closes the window without saving."""
    ok, message = load_in_catalyst_edit(path, name, restore_focus=False)
    if not ok:
        return False, message
    hwnd = find_catalyst_window()
    state = run_uia("state", hwnd)
    if not state.get("ok"):
        return False, state.get("message", "Couldn't read Catalyst Edit's screen, so nothing was saved.")
    if not same_name(state.get("name"), name):
        return False, f"Catalyst Edit shows \"{state.get('name')}\", not \"{name}\", so nothing was saved."

    previous = user32.GetForegroundWindow()
    if not bring_to_front(hwnd):
        return False, "Loaded, but couldn't bring Catalyst Edit to the front to save. Nothing was saved."
    press_ctrl(VK_D)
    result = run_uia("save", hwnd, bank=bank, channel=channel, dryRun=dry_run)
    slot = f"{bank}{channel}"
    if not result.get("ok") or result.get("dryRun"):
        if result.get("stage") != "open":
            click_title_bar(hwnd)  # close the save window without saving
        after = run_uia("state", hwnd)
        if as_list(after.get("popups")):
            return False, (result.get("message") or "Dry run") + " The save window may still be open; close it in Catalyst Edit."
        if result.get("dryRun"):
            return True, f"Dry run: slot {slot} was picked and checked, then the window was closed without saving."
        return False, result.get("message", "Saving failed.") + " Nothing was saved."
    if result.get("stillOpen"):
        click_title_bar(hwnd)
        return False, f"Pressed SAVE but the save window stayed open. Check slot {slot} in Catalyst Edit."
    if previous and previous != hwnd:
        bring_to_front(previous)
    if result.get("saved"):
        return True, f"Saved \"{name}\" to slot {slot} on your amp."
    return True, f"Saved \"{name}\" to slot {slot}. (Catalyst Edit didn't show its usual confirmation, so give it a quick listen.)"


# ---------------------------------------------------------------- web server
load_lock = threading.Lock()


RESERVED_NAMES = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}


def safe_filename(name):
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "-", str(name)).strip(" .")[:40] or "Preset"
    return "_" + name if name.split(".")[0].lower() in RESERVED_NAMES else name


def check_preset(preset):
    """Returns the preset's name, or raises ValueError if it isn't a Catalyst preset."""
    if not isinstance(preset, dict) or preset.get("schema") != "L6Preset":
        raise ValueError("not a Catalyst preset")
    data = preset.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("tone"), dict) or not isinstance(data.get("meta"), dict):
        raise ValueError("not a Catalyst preset")
    return str(data["meta"].get("name") or "Preset")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/api/" in (str(args[0]) if args else ""):
            sys.stderr.write("  " + (fmt % args) + "\n")

    def host_ok(self):
        # Blocks other websites (and DNS-rebinding tricks) from using this helper.
        allowed = {f"{HOST}:{PORT}", f"localhost:{PORT}"}
        if self.headers.get("Host") not in allowed:
            return False
        origin = self.headers.get("Origin")
        return origin is None or origin in {f"http://{h}" for h in allowed}

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self.host_ok():
            return self.send_json(403, {"ok": False, "message": "Forbidden"})
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/" + PAGE.replace(" ", "%20"))
            return self.end_headers()
        if self.path == "/api/status":
            return self.send_json(200, {"ok": True, "catalystEdit": bool(find_catalyst_window())})
        return super().do_GET()

    def do_POST(self):
        # /api/load  body: a .catl6p preset
        # /api/save  body: {"preset": <.catl6p preset>, "bank": 1-6, "channel": "A"|"B", "dryRun": bool}
        if not self.host_ok() or self.path not in ("/api/load", "/api/save"):
            return self.send_json(403, {"ok": False, "message": "Forbidden"})
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.send_json(415, {"ok": False, "message": "Expected JSON"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length < 200_000:
                raise ValueError("bad size")
            body = json.loads(self.rfile.read(length))
            if self.path == "/api/save":
                bank, channel = body.get("bank"), body.get("channel")
                if type(bank) is not int or not 1 <= bank <= 6 or channel not in ("A", "B"):
                    raise ValueError("bad slot")
                preset = body.get("preset")
            else:
                preset = body
            name = check_preset(preset)
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            return self.send_json(400, {"ok": False, "message": f"Bad request: {e}"})

        if not load_lock.acquire(blocking=False):
            return self.send_json(409, {"ok": False, "message": "Still busy with the previous sound."})
        try:
            os.makedirs(LOADED_DIR, exist_ok=True)
            path = os.path.join(LOADED_DIR, safe_filename(name) + ".catl6p")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(preset, f, indent=1)
            if self.path == "/api/save":
                ok, message = save_to_amp_slot(path, name, bank, channel, dry_run=bool(body.get("dryRun")))
            else:
                ok, message = load_in_catalyst_edit(path, name)
        finally:
            load_lock.release()
        print(("  OK   " if ok else "  FAIL ") + f"{name}: {message}")
        return self.send_json(200, {"ok": ok, "message": message, "file": path})


def main():
    if sys.platform != "win32":
        sys.exit("The helper only works on Windows.")
    url = f"http://{HOST}:{PORT}/"
    try:
        server = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError:
        print(f"Port {PORT} is busy, so the helper is probably already running. Opening the page.")
        webbrowser.open(url)
        return
    print("Catalyst Preset Picker is running at", url)
    print("Keep this window open while you use it. Close it to stop.")
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
