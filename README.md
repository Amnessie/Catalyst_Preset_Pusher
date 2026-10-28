# Catalyst Preset Picker

196 ready-to-play sounds for the **Line 6 Catalyst** amps, plus a small app to browse, tweak and load them.
The sounds cover clean, blues, rock, metal, ambient and fingerstyle, plus 121 song sounds from Pink Floyd, Dire Straits,
Jimi Hendrix, B.B. King, Joe Cocker, Stevie Ray Vaughan, Santana, Chuck Berry and Van Halen.

![The picker: every sound as a card, with the selected sound's quick fixes and knobs on the right](screenshots/picker.png)

Made and tested on a **Catalyst 60**. The app can also build presets for the Catalyst 100 and 200, but that hasn't been tested on a real amp.

Not made by or affiliated with Line 6. The song sounds are starting points based on public gear rundowns, not the artists' exact settings.

## What you need

| | Needed for | Where to get it |
|---|---|---|
| A Line 6 Catalyst amp and a USB cable | Everything | Plug straight into the PC, not through a USB hub |
| **Catalyst Edit** (free) | Loading presets onto the amp | [line6.com/software](https://line6.com/software/) |
| **Python 3** (free) | The **Load to amp** / **Save to slot** buttons (Windows only) | [python.org/downloads](https://www.python.org/downloads/) |
| A web browser (Chrome, Edge or Firefox) | The picker app | Already on your PC |

Optional: Line 6's **Catalyst ASIO driver** (same software page) is for recording and USB audio on Windows. Catalyst Edit
doesn't need it for presets, but if Catalyst Edit can't find your amp, installing it is worth a try.

## Install

1. **Get the files.** On this page, click the green **Code** button, then **Download ZIP**. Right-click the zip and choose
   **Extract All**. Use the extracted folder, not the files inside the zip.
2. **Install Catalyst Edit** from Line 6, connect the amp by USB, switch it on and check that Catalyst Edit shows your amp.
3. **Install Python 3** (only for the amp buttons). In the installer, tick **"Add python.exe to PATH"** before clicking Install.

## Use the picker

1. Open Catalyst Edit with the amp connected.
2. Double-click **`Start Preset Picker.bat`**. A black helper window opens, and the picker opens in your browser.
   Keep the black window open while you play; close it when you're done.
3. Click a sound, then **Load to amp** to hear it. Tweak it with the sliders or the quick fix buttons ("Too bright", "More gain", …).
   **Save to slot** stores it on the amp in the slot you pick, after asking you first.
   While it saves (about 10 seconds), don't click around in Catalyst Edit.

Also in the picker: search by song or guitarist, favorites (☆), a 12-sound bank to download in one go, and importing or
exporting your own sounds. Pick your amp model and pickup type at the top.

**Windows warning?** Because the .bat came from the internet, Windows may warn you before running it. On
"Windows protected your PC", click **More info**, then **Run anyway**; on a security warning, click **Run**.
The helper only runs on your own PC (127.0.0.1) and installs nothing.

**No Python, or not on Windows?** Double-click `Catalyst Preset Picker.html` instead. Everything works except the amp
buttons: click **Download .catl6p**, then load the file in Catalyst Edit with **Ctrl+O**.

## Just want the preset files?

The `.catl6p` files are in [`presets/`](presets), made for the Catalyst 60, in three versions to match your guitar:

| Folder | For |
|---|---|
| `Mixed (HSS)` | Guitars with mixed pickups, or if you're not sure |
| `Humbucker` | Les Paul, SG and other humbucker guitars |
| `Single coil` | Strat, Tele and other single-coil guitars |

Each folder is sorted by style, and the song sounds are in `Songs/<artist>`.
To load one: in Catalyst Edit press **Ctrl+O** and pick the file. To keep it on the amp, press **Ctrl+D** and choose a slot.

## All presets

<!-- preset list: written by export_all.js -->
Every sound is in all three pickup folders, under `<pickups>/<style>/` (songs under `<pickups>/Songs/<artist>/`). Click a folder to see what's in it.

<details>
<summary><b>Clean (12)</b></summary>

| Sound | What it is |
|---|---|
| **Glass Clean** | Sparkly Fender-style clean with a touch of plate. Great on the neck and middle pickup. |
| **Funk Clean** | Tight, bright and percussive for 16th-note chicken picking and Nile Rodgers strums. |
| **Jazz Warm** | Round, dark and smooth for chord melodies. Roll your guitar's tone knob back a bit. |
| **Country Twang** | Snappy bridge-pickup twang with a single slapback repeat. Telecaster heaven. |
| **Surf Spring** | Drippy, splashy spring reverb for Dick Dale and Ventures style surf. |
| **80s Chorus** | Lush chorused clean like The Police or Andy Summers. Arpeggios love this. |
| **Vibe Clean** | Watery Uni-Vibe swirl for Little Wing and Machine Gun style clean parts. |
| **Trem Western** | Moody tremolo and spring. Spaghetti western, Chris Isaak, Boulevard of Broken Dreams. |
| **Reggae Skank** | Thin, bright off-beat chops with a short echo. Bob Marley rhythm parts. |
| **Neo Soul** | Warm, slightly swirly clean for John Mayer, H.E.R. and Tom Misch style chord work. |
| **Arpeggio Echo** | Big, airy clean with delay and hall for Coldplay-style arpeggios and pop ballads. |
| **Ballad Clean** | Chorused, glossy 80s clean for ballad verses before the big chorus. Pair with Stadium Rock. |

</details>

<details>
<summary><b>Fingerstyle (10)</b></summary>

| Sound | What it is |
|---|---|
| **Classical Soft** | Soft, round and dark for classical pieces. Neck pickup, tone knob around 6, play with your fingers. |
| **Concert Hall** | Classical guitar in a big hall. Long, gentle reverb that lets slow pieces breathe. |
| **Spanish Room** | Warm, woody midrange and a small room. For Spanish pieces, flamenco-style strums and arpeggios. |
| **Fingerstyle** | Clear, balanced and a little brighter for fingerpicked pop and folk. Middle + neck pickups. |
| **Practice Room** | Dry, close and honest. Hear every note clearly while you learn a piece. |
| **Baroque Clarity** | A bit brighter with a short room, so two-voice Bach lines stay separate. Not too boomy. |
| **Romantic Warm** | Warm, singing and lush for Tárrega, Barrios and expressive slow melodies with vibrato. |
| **Cathedral** | A huge stone church. Very long reverb for slow chorales, harmonics and Recuerdos tremolo. |
| **Bossa Nova** | Soft, dark and intimate for João Gilberto style comping and Girl from Ipanema. |
| **Chorus Picking** | Gentle chorus and hall that make fingerpicked arpeggios shimmer. Middle + neck pickups. |

</details>

<details>
<summary><b>Blues (6)</b></summary>

| Sound | What it is |
|---|---|
| **Edge Breakup** | Clean when you pick soft, growls when you dig in. Turn your guitar volume to 7 for clean. |
| **Texas Blues** | Fat SRV-style clean-ish drive with the boost on, like a Tube Screamer into a Fender. |
| **Chicago Blues** | Gritty tweed-style midrange push for shuffles and harp-player bands. |
| **Gravity Lead** | Smooth, singing John Mayer style lead. Neck pickup, bend slowly. |
| **Woman Tone** | Creamy, dark 60s Clapton lead. Neck humbucker with the tone knob near 0. |
| **Slow Blues** | Warm, fat and touch-sensitive for slow 12/8 blues. Neck pickup, lots of vibrato. |

</details>

<details>
<summary><b>Rock (32)</b></summary>

| Sound | What it is |
|---|---|
| **Brit Chime** | AC30-style chime and jangle. Beatles, Tom Petty, early U2, Britpop strumming. |
| **Classic Crunch** | Plexi-style crunch for AC/DC, Stones and open-chord rock. Bridge pickup. |
| **70s Rock** | Bigger, looser Zeppelin and Deep Purple rhythm crunch with room around it. |
| **Brown Sound** | Cranked, boosted Plexi in the spirit of early Van Halen. Plate reverb for that 1978 room. |
| **Rock Lead** | Slash-style singing lead with mids up front and a short delay tail. |
| **Comfortably** | Gilmour-style lead: big sustain, tape echo and hall. Slow bends, lots of space. |
| **Pop Punk** | Tight, saturated power chords for Green Day and Blink-182. Palm mute away. |
| **Grunge** | Thick, slightly scooped 90s Seattle drive for Nirvana and Soundgarden riffs. |
| **Leslie Rock** | Light crunch through a spinning rotary speaker. Think SRV's Cold Shot or Badge. |
| **Phase Crunch** | Slow phaser over crunchy rhythm, the classic Eruption-era swoosh. |
| **Stadium Rock** | Polished 80s arena crunch with a touch of chorus. Bon Jovi, Journey, Toto. |
| **Southern Rock** | Bright, open crunch for Lynyrd Skynyrd and Allman Brothers riffs. Bridge + middle pickups. |
| **Blues Rock** | Thick, mid-heavy boosted drive. Black Keys, Joe Bonamassa, Gary Clark Jr. |
| **Garage Rock** | Raw, honky and loud. White Stripes, The Hives, early Strokes. |
| **Indie Rock** | Crisp, punchy crunch with chime. Arctic Monkeys, Franz Ferdinand, Kings of Leon. |
| **Brit Rock Wall** | Big, saturated chimey wall of strums. Oasis and The Verve. |
| **90s Alt Rock** | Thick, tight and slightly scooped. Foo Fighters, Smashing Pumpkins, Weezer. |
| **Stoner Rock** | Fat, fuzzy midrange grind for Queens of the Stone Age and Kyuss. Down-tuned riffs. |
| **Funk Rock** | Bright, edgy crunch for Red Hot Chili Peppers style funky rhythm and riffs. |
| **Hard Rock 80s** | Hot-rodded Marshall rhythm for Guns N' Roses, Whitesnake and Scorpions. |
| **Voodoo Lead** | Wild, boosted lead with a Uni-Vibe swirl in the style of Hendrix and Robin Trower. |
| **Melodic Lead** | Singing, sustaining lead with lots of mids. Gary Moore, Santana-style held notes. |
| **Ballad Lead** | Smooth, medium-gain lead with long delay and hall for slow power-ballad solos. |
| **Rock Clean** | Clean that still has bite, for verses before the distortion kicks in. Pair it with a crunch sound. |
| **Punk Rock** | Loud, buzzy and mid-heavy downstroke power chords. Ramones, Sex Pistols, The Clash. |
| **Rockabilly** | Twangy, lightly driven slapback for Brian Setzer, Elvis and Johnny B. Goode licks. |
| **Treble Boost** | Brian May style: a boosted, singing Vox-type lead with echo. Neck humbucker, harmonies. |
| **Jet Flanger** | Slow jet-plane flanger over a hot crunch. Unchained, Barracuda and Walking on the Moon riffs. |
| **Octave Fuzz** | Ringing octave-up fuzz like the Purple Haze solo. Neck pickup, play above the 12th fret. |
| **Prog Rock** | Clear, articulate drive for Rush and Dream Theater: complex chords stay readable. Light chorus. |
| **Modern Rock** | Thick, tight, radio-ready rhythm. Foo Fighters' later records, Royal Blood, Shinedown. |
| **Ping Pong Lead** | Smooth lead with a bouncing rhythmic delay. Fills the space when you're the only guitar. |

</details>

<details>
<summary><b>Metal (8)</b></summary>

| Sound | What it is |
|---|---|
| **80s Hair Metal** | Big, bright high gain with delay and hall for Def Leppard and Mötley Crüe solos. |
| **Thrash Rhythm** | Scooped, tight 80s thrash for Metallica and Slayer downpicking. No reverb. |
| **Modern Metal** | Boosted, tight and punchy modern rhythm tone. Drop tunings welcome. |
| **Djent Tight** | Less gain, more boost, hard gate. Very tight for 7/8-strings and staccato riffs. |
| **Metal Lead** | Saturated, mid-forward lead with delay and hall. Sustains forever. |
| **Doom Sludge** | Huge, dark and woolly. Black Sabbath and Electric Wizard in drop C. |
| **Nu Metal** | Heavily scooped, bass-heavy and tight. Korn, Limp Bizkit, Slipknot. Drop tuning. |
| **Classic Metal** | Mid-forward, bright NWOBHM gain for galloping Iron Maiden and Judas Priest riffs. |

</details>

<details>
<summary><b>Ambient (7)</b></summary>

| Sound | What it is |
|---|---|
| **Dotted Eighth** | The Edge's rhythmic delay. 375 ms is a dotted 8th at 120 BPM, so play straight 8ths. |
| **Ambient Swells** | Fade in with your volume knob. Ducking delay stays out of the way until you stop playing. |
| **Shimmer Pad** | Octave-shimmer reverb that turns chords into a pad. Let notes ring. |
| **Shoegaze Wall** | Fuzzy, washed-out wall of sound for My Bloody Valentine and Slowdive. |
| **Lo-Fi Echo** | Clean tone into a crunchy, warbly digital delay. Bedroom-pop and indie. |
| **Post-Rock** | Shimmering, echoing chime that builds into walls. Explosions in the Sky, Mogwai. |
| **Floyd Rotary** | Dreamy clean through a slow spinning speaker. Pink Floyd's Breathe and Us and Them. |

</details>

<details>
<summary><b>Songs (121)</b></summary>

<details>
<summary><b>Pink Floyd (16)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Numb Solo 1** | Comfortably Numb (first solo) | The first, gentler solo: singing Strat bridge pickup with echo and hall. Slow, wide bends. |
| **Numb Solo 2** | Comfortably Numb (outro solo) | The big outro solo: Big Muff into a Hiwatt with about 430 ms of delay, as on his later tours. Bridge pickup. |
| **Time Solo** | Time | Fuzz Face plus Colorsound boost and Binson echo. A short 240 ms echo gives the busy multi-head repeats. Big reverb. |
| **Money Solo** | Money | Strat bridge pickup, Fuzz Face and Powerboost, Binson echo. The first solo is wet; for the dry second solo turn Mix down. |
| **Brick Rhythm** | Another Brick in the Wall, Part 2 | The funky, compressed clean Strat rhythm. Bridge pickup, palm-muted 16ths, dig in with the pick. |
| **Brick Solo** | Another Brick in the Wall, Part 2 (solo) | The solo was a Les Paul on the neck pickup into a Mesa/Boogie, gated and compressed. Warm, round and dry. |
| **Run Like Hell** | Run Like Hell | Esquire in drop D with a mild booster and the famous 380 ms (dotted 8th) delay. Play straight 8ths, let the echo fill in. |
| **Shine On** | Shine On You Crazy Diamond (Parts I-V) | The four-note theme and intro solo: Strat with a Colorsound boost and 370 ms echo, 5-6 repeats, lots of hall. |
| **Have a Cigar** | Have a Cigar | Strat bridge pickup, Colorsound heavy boost and a slow MXR Phase 90 on the funky riff. |
| **WYWH Acoustic** | Wish You Were Here | The record is 12-string and steel acoustics. Bright and thin with a little chorus for the 12-string shimmer. Middle + neck pickups. |
| **Learning to Fly** | Learning to Fly | Late-80s Gilmour: light overdrive and a Boss CE-2 chorus (rate 11:00, depth 1:00). Bridge for rhythm, neck for fills. |
| **Us and Them** | Us and Them | Clean Strat neck pickup through a Leslie, which dominates the sound. Slow rotor, gentle hands. |
| **Breathe** | Breathe | Strat chords through a Uni-Vibe and Binson echo, washed in reverb. The slide is a pedal steel; try a bottleneck. |
| **Hey You Solo** | Hey You | Double-tracked Big Muff solo, dark and thick, with Gilmour's typical 370 ms echo underneath. |
| **Dogs Solo** | Dogs | Boosted Big Muff, no modulation or delay. Dig in hard with the pick; the aggression is the point. |
| **Coming Back** | Coming Back to Life | The long, clean-ish opening solo: boosted Strat with 440 ms echo and a big hall. Let every note ring out. |

</details>

<details>
<summary><b>Dire Straits (13)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Sultans of Swing** | Sultans of Swing | '61 Strat on the neck + middle position, clean Vibrolux and probably a compressor. Pick with your fingers. |
| **Money For Nothin** | Money for Nothing | Les Paul into a Marshall (some say a Laney), with the famous honky, 'stuck wah' midrange. Fingers, dig in. |
| **Brothers in Arms** | Brothers in Arms | Les Paul neck pickup into a JTM45, compressed, with lots of echo and reverb. Soft attack, long sustain. |
| **Walk of Life** | Walk of Life | Tele on neck + middle, compressed and twangy with a short slapback. The famous riff is organ; this is the guitar. |
| **Romeo and Juliet** | Romeo and Juliet | Played on a National resonator. Bright, metallic and woody; fingerpick near the bridge. |
| **Telegraph Road** | Telegraph Road | The long outro solo: lightly driven Strat with echo. Builds from gentle to screaming, so ride your guitar volume. |
| **Investigations** | Private Investigations | The quiet classical-guitar theme. Dark, soft and spacious. Neck pickup, fingers, tone knob down. |
| **Lady Writer** | Lady Writer | Fast, clean Strat on the in-between pickup, a bit brighter and snappier than Sultans. |
| **Tunnel of Love** | Tunnel of Love | Driven Strat with echo for the long, emotional outro solo. |
| **So Far Away** | So Far Away | Relaxed, compressed clean rhythm with a touch of chorus. The record used a synth guitar; this gets the vibe. |
| **Why Worry** | Why Worry | Dreamy, compressed Strat on neck + middle with a long reverb. Soft fingers, let it float. |
| **Latest Trick** | Your Latest Trick | Smooth, compressed neck-pickup clean with reverb for the fills around the sax. |
| **Heavy Fuel** | Heavy Fuel | Knopfler's ZZ Top-style crunch. Gritty, mid-forward and tight. |

</details>

<details>
<summary><b>Jimi Hendrix (14)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Purple Haze** | Purple Haze | The riff: Fuzz Face into a cranked Marshall. Thick, hairy and loud. For the solo use Haze Octavia. |
| **Haze Octavia** | Purple Haze (solo) | Roger Mayer built the Octavia for this solo. Octave-up fuzz before the amp; neck pickup, above the 12th fret. |
| **Hey Joe** | Hey Joe | Strat neck pickup into a moderately driven Marshall. Warm, slightly hairy, with room around it. |
| **Little Wing** | Little Wing | The chord-melody intro with a Leslie-style rotating swirl. Neck pickup, thumb over the neck, lots of hammer-ons. |
| **Wind Cries Mary** | The Wind Cries Mary | Clean-ish Strat double-stops on neck/middle. Recorded in 20 minutes at the end of the Fire session. |
| **Foxy Lady** | Foxy Lady | Maximum Fuzz Face into a Marshall. Start with feedback: face the amp and let the note bloom. |
| **Voodoo Child** | Voodoo Child (Slight Return) | Wah, Fuzz Face and Marshall. No wah on the Catalyst, so the mids are pushed for that vocal honk. |
| **Watchtower** | All Along the Watchtower | Biting crunch with echo for the multi-part solo. Try a lighter or slide for the slide section. |
| **Machine Gun** | Machine Gun | Band of Gypsys: Fuzz Face plus a deep, slow Uni-Vibe throb into a Marshall. |
| **Red House** | Red House | Slow blues: less gain, more touch. Neck pickup; leave space between phrases like Jimi did. |
| **Fire** | Fire | Bright, punchy Marshall crunch for the stabbing riff. Bridge pickup. |
| **Manic Depression** | Manic Depression | Heavy, swinging 3/4 fuzz-rock. Thick and wild. |
| **Star Spangled** | The Star-Spangled Banner (Woodstock) | Woodstock 1969: Fuzz Face and Uni-Vibe through a wall of Marshalls. Use the whammy bar for the bombs. |
| **Angel** | Angel | Soft, shimmering clean chord-melody with a slow rotating-speaker swirl. Neck pickup. |

</details>

<details>
<summary><b>B.B. King (12)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Thrill Is Gone** | The Thrill Is Gone | Lucille with volume and tone up and Varitone on 2. Barely breaking up, sweet and stinging. Butterfly vibrato. |
| **Every Day Blues** | Every Day I Have the Blues | Up-tempo swing: bright, clean Lucille with just a hint of edge on hard notes. |
| **Sweet Lil Angel** | Sweet Little Angel | Slow blues, singing and vocal. Thick mids and a touch more hair for long, held notes. |
| **Rock Me Baby** | Rock Me Baby | Mid-tempo groove with punchy, slightly driven single notes. |
| **How Blue Can You** | How Blue Can You Get (Live at the Regal) | The 1964 Live at the Regal sound: bright, cutting and dynamic, driving a Fender amp hard on the peaks. |
| **Paying the Cost** | Paying the Cost to Be the Boss | Crisp late-60s Lucille: clean, confident and punchy. |
| **3 O'Clock Blues** | Three O'Clock Blues | His 1951 breakthrough: a small, darker amp breaking up more. Rawer than his later sound. |
| **Lucille** | Lucille | The slow talking blues where B.B. tells the story of his guitar. Warm, clean and expressive. |
| **Why I Sing Blues** | Why I Sing the Blues | Funky 1969 groove: clean, mid-forward fills between the vocal lines. |
| **When Love Comes** | When Love Comes to Town (with U2) | 1988 with U2: bright, stinging lead with a bigger, 80s-style reverb. |
| **Riding With King** | Riding with the King (with Eric Clapton) | 2000 with Clapton: a bit more drive and roundness, made for trading licks. |
| **Sweet Sixteen** | Sweet Sixteen | Dramatic slow blues: pushes into breakup when you dig in, sweet when you don't. |

</details>

<details>
<summary><b>Joe Cocker (12)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Little Help** | With a Little Help from My Friends | Jimmy Page played on the 1968 record; Henry McCullough at Woodstock. Raw, fuzzy British drive for the big intro. |
| **Feelin' Alright** | Feelin' Alright | Loose, funky clean-crunch rhythm with a little spring. |
| **The Letter** | The Letter (Mad Dogs & Englishmen) | The 1970 Mad Dogs band: driving, gritty rock-and-soul guitar. |
| **Delta Lady** | Delta Lady | Bluesy, swampy crunch with a ringing top end. |
| **High Time** | High Time We Went | Rollicking early-70s rock-and-roll crunch. |
| **So Beautiful** | You Are So Beautiful | A piano ballad on the record. Soft, chorused clean to accompany it gently. |
| **Where We Belong** | Up Where We Belong | 1982 soundtrack ballad: glossy, chorused clean with a big hall. |
| **Unchain My Heart** | Unchain My Heart | 1987 Ray Charles cover: tight, bright crunch stabs with the horns. |
| **Leave Hat On** | You Can Leave Your Hat On | 1986 bluesy strut: punchy, mid-heavy crunch for the stop-time riff. |
| **When Night Comes** | When the Night Comes | 1989 Bryan Adams song: chiming 80s crunch with chorus. |
| **N'oubliez Jamais** | N'oubliez jamais | 1997 acoustic-driven ballad. Bright, clean and open, with light chorus. |
| **Many Rivers** | Many Rivers to Cross | Gospel-soul ballad: warm clean with a deep reverb. |

</details>

<details>
<summary><b>Stevie Ray Vaughan (14)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Pride and Joy** | Pride and Joy | Tube Screamer into a Vibroverb, guitar tuned down to Eb. Let as many strings ring as you can, shuffle hard. |
| **Texas Flood** | Texas Flood | Slow blues with more drive: TS808 into a Dumble-style amp. Huge bends, dynamic picking. |
| **Lenny** | Lenny | Named after his wife and the '65 Strat she gave him. Soft, clean neck pickup with lots of spring and whammy. |
| **Cold Shot** | Cold Shot | The lazy shuffle rhythm through a Fender Vibratone (a Leslie-type speaker) driven by a Vibroverb. |
| **Scuttle Buttin'** | Scuttle Buttin' | Blistering, bright and tight for the fast instrumental. Tube Screamer on, pick hard. |
| **Stand Weather** | Couldn't Stand the Weather | Funky, punchy crunch with pushed mids. The record has wah in spots; this is the main rhythm. |
| **House Is Rockin'** | The House Is Rockin' | Jumping 1989 shuffle: driven, bright and swinging. |
| **Crossfire** | Crossfire | The sober-era 1989 sound: cleaner, compressed and polished, still with bite. |
| **Tightrope** | Tightrope | Driving clean-crunch rhythm with clear notes. |
| **Riviera Paradise** | Riviera Paradise | Jazzy, clean neck-pickup ballad. Soft touch, lots of room. |
| **Little Wing SRV** | Little Wing (instrumental) | SRV's instrumental version: fat neck pickup, slightly driven, with a gentle vibe swirl. |
| **Voodoo SRV** | Voodoo Child (Slight Return), SRV version | SRV's take on Hendrix: Tube Screamer and wah into a cranked amp. Mids pushed for the wah honk. |
| **Mary Little Lamb** | Mary Had a Little Lamb | Buddy Guy cover: snappy shuffle crunch with stop-time stabs. |
| **Tin Pan Alley** | Tin Pan Alley | Very slow, very quiet blues that explodes. Ride your guitar volume from whisper to scream. |

</details>

<details>
<summary><b>Santana (13)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Black Magic** | Black Magic Woman / Gypsy Queen | 1970 Abraxas: cranked, Boogie-modded Fender Twin. Humbucker with the tone knob around 6-7, long sustained notes. |
| **Oye Como Va** | Oye Como Va | Biting, sustaining lead over the organ groove. A bit brighter than Black Magic. |
| **Samba Pa Ti** | Samba Pa Ti | Abraxas ballad with a wah parked in its 'sweet spot', so the mids are high and the treble low. Neck pickup. |
| **Europa** | Europa (Earth's Cry Heaven's Smile) | 1976: Yamaha SG into a Mesa/Boogie Mark I. Violin-like sustain; hold notes and let them bloom. |
| **Smooth** | Smooth (with Rob Thomas) | 1999: PRS into a Boogie. Chunky crunch for the rhythm, singing for the fills and solo. |
| **Maria Maria** | Maria Maria | Smoother, lower-gain lead fills over the Latin groove. Neck pickup, sweet and warm. |
| **Soul Sacrifice** | Soul Sacrifice (Woodstock) | Woodstock 1969: raw, cranked SG through a loud amp. Wild and aggressive. |
| **Evil Ways** | Evil Ways | 1969 debut: gritty, mid-forward crunch trading lines with the organ. |
| **Put Your Lights** | Put Your Lights On | Dark, moody minor groove: warm crunch with a plate. |
| **Game of Love** | The Game of Love | 2002 pop-rock: light, clean-ish crunch and melodic fills. |
| **Corazon Espinado** | Corazón Espinado (with Maná) | Fiery, sustaining lead over the Latin rock groove. |
| **She's Not There** | She's Not There | 1977 Zombies cover: late-70s Boogie lead, smooth and cutting. |
| **Flor d'Luna** | Flor d'Luna (Moonflower) | Gentle, sustaining melody over a slow Latin groove. Soft hands, long hall. |

</details>

<details>
<summary><b>Chuck Berry (13)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Johnny B. Goode** | Johnny B. Goode | ES-350T into a Fender pushed into light crunch, plus the Chess studio room. Double-stops on the bridge pickup. |
| **Roll Over Beeth.** | Roll Over Beethoven | The famous intro lick: bright, slightly raunchy and in-your-face. |
| **Maybellene** | Maybellene | His 1955 debut: rawer and smaller-sounding, with more amp grit and room. |
| **Sweet Little 16** | Sweet Little Sixteen | Bouncy, cleaner rhythm and fills. Bright and articulate. |
| **RocknRoll Music** | Rock and Roll Music | Driving boogie rhythm with a little bite. |
| **No Particular** | No Particular Place to Go | 1964 cruising sound: clean-crunch and a touch brighter. |
| **Never Can Tell** | You Never Can Tell | The Pulp Fiction song: gentler, cleaner rhythm under the piano. |
| **Memphis** | Memphis, Tennessee | Soft, dark and clean 1959 recording. Neck pickup, gentle picking. |
| **Carol** | Carol | Raunchy, driving rhythm and double-stop lead. The Stones covered it. |
| **Brown Eyed Man** | Brown Eyed Handsome Man | Latin-tinged groove: clean, round and swinging. |
| **Back in the USA** | Back in the U.S.A. | Happy, bright 1959 rock and roll. Crisp and lively. |
| **Run Rudolph Run** | Run Rudolph Run | The Christmas rocker: the Johnny B. Goode sound with a little more snap. |
| **Little Queenie** | Little Queenie | Grinding, mid-tempo boogie with a bit of hair on it. |

</details>

<details>
<summary><b>Van Halen (14)</b></summary>

| Sound | Song | What it is |
|---|---|---|
| **Eruption** | Eruption | Brown sound with an MXR Phase 90 at a slow setting, plus a big plate. Tap away; the Echoplex is left out for the phaser. |
| **Runnin' w Devil** | Runnin' with the Devil | The 1978 brown sound with a single Echoplex slap and a huge plate reverb. |
| **Ain't Talkin'** | Ain't Talkin' 'bout Love | Phase 90 set slow (knob around 9 o'clock) over the brown sound for the arpeggiated riff. |
| **Really Got Me** | You Really Got Me | Kinks cover, straight brown sound: variac'd Plexi, bridge humbucker, plate. |
| **Unchained** | Unchained | MXR flanger on the drop-D riff. Slow sweep, lots of regeneration. |
| **Panama** | Panama | 1984: same Plexi, Kramer guitar, a slightly spongier, more laid-back crunch than the early records. |
| **Hot for Teacher** | Hot for Teacher | Fast, saturated brown sound for the tapping intro and boogie riff. |
| **Jump Solo** | Jump (guitar solo) | The song is synth; this is for the tapped solo. Brown sound with a little echo. |
| **Dance the Night** | Dance the Night Away | Lighter, poppier crunch for the harmonics and the singalong chords. |
| **Beautiful Girls** | Beautiful Girls | Swaggering 1979 brown sound with a fat bottom end. |
| **Atomic Punk** | Atomic Punk | Phased, menacing brown sound. Scrape the strings for the intro noise. |
| **Ice Cream Man** | Ice Cream Man | John Brim blues cover: starts acoustic, then this full-band brown sound kicks in. |
| **Mean Street** | Mean Street | The darker, heavier 1981 Fair Warning tone. Thick mids, less fizz. |
| **Why Cant This Be** | Why Can't This Be Love | 1986 '5150' era: smoother, higher-gain tone with a wide, chorus-like shimmer. |

</details>

</details>
<!-- end of preset list -->

## Troubleshooting

- **"python is not recognized" or "Python was not found"**: Python isn't installed or wasn't added to PATH. Reinstall it with
  "Add python.exe to PATH" ticked, or use the HTML file as above.
- **"Open Catalyst Edit to load sounds"** in the picker: start Catalyst Edit, or wait a few seconds after starting it.
- **Save says Catalyst Edit isn't connected to the amp**: check that the amp is on and the USB cable is plugged in, and wait until
  Catalyst Edit shows a bank and channel.
- **Too loud or too quiet overall**: use **Overall level** at the top of the picker.

## Files

| File | What it is |
|---|---|
| `Start Preset Picker.bat` | Starts the picker with the amp buttons (runs `helper.py`) |
| `Catalyst Preset Picker.html` | The picker itself, also works opened directly |
| `presets.js` | Every sound's settings |
| `models.js` | Catalyst amp and effect parameters, generated by `make_models.py` from Catalyst Edit's own files |
| `helper.py` | Loads and saves to the amp through Catalyst Edit (Python standard library only) |
| `presets/` | Every sound as a `.catl6p` file |
| `screenshots/` | The pictures in this README |
| `export_all.js` | Rebuilds `presets/` and the list above: `node export_all.js presets` (needs [Node.js](https://nodejs.org)) |
| `build_share.js` | Builds a share zip in `dist/`: `node build_share.js` (needs Node.js) |
