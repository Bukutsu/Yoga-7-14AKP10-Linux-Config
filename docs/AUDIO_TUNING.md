# Audio Tuning for Lenovo Yoga 7 (Linux)

Getting the best audio out of your Lenovo Yoga 7 (and other modern Lenovo laptops with the ALC3306 or ALC287 codecs) on Linux requires two major steps:
1. Fixing the hardware mapping so all 4 speakers (2 tweeters, 2 woofers) fire.
2. Applying DSP (Digital Signal Processing) to correct the sound signature and maximize loudness without clipping, simulating the "Dolby Atmos" experience you get on Windows.

---

## 1. The Kernel Quirk (Fixing "Tinny" Sound)

By default, the Linux kernel often misidentifies the ALC3306 chip and fails to route audio to the bottom bass speakers.

To fix this:

1. Identify your audio card index by running `aplay -l`. Note if your `ALC287/ALC3306 Analog` device is `card 0` or `card 1`.
2. Create a modprobe configuration file to apply the specific Lenovo Yoga 9 bass pin fix to your card.

Create `/etc/modprobe.d/alc3306-yoga-fix.conf`:
```bash
sudo nano /etc/modprobe.d/alc3306-yoga-fix.conf
```

Add the following line (if your ALC chip is **Card 1**, which is common when HDMI audio is Card 0):
```conf
options snd-hda-intel model=(null),alc287-yoga9-bass-spk-pin
```
*(If your ALC chip is **Card 0**, remove the `(null),` prefix).*

3. Rebuild your initramfs and reboot:
```bash
sudo mkinitcpio -P
```

Upon rebooting, your woofers will be active, providing a significantly fuller sound base.

---

## 2. EasyEffects "Perfect Tuning" Preset

Even with all 4 speakers working, laptop speakers need heavy EQ and compression to sound good. We have crafted a custom **Yoga_7_Perfect_Tuning** preset that balances clarity, bass depth, and stereo width without relying on external impulse response (IRS) files.

### Installation

1. Install EasyEffects from your distribution's repository:
```bash
sudo pacman -S easyeffects
```
2. Open EasyEffects, go to **Preferences** (top-right menu) and enable **Launch Service at System Startup**.
3. Go to the **Presets** menu (top-left).
4. Click **Import Preset** and select the `Yoga_7_Perfect_Tuning.json` file located in the `configs/audio/easyeffects_presets/` directory of this repository.
5. Select the imported preset and click **Load**.

### What this preset does:
*   **Stereo Tools**: Widens the soundstage to mimic Dolby Atmos spatial audio.
*   **Equalizer**: Boosts the low-mids (80-160Hz) to give body to vocals, cuts harsh frequencies at 3.5kHz, and adds "air" at 11kHz.
*   **Multiband Compressor**: Squashes harsh peaks in the audio automatically.
*   **Bass Enhancer**: Generates sub-bass harmonics (40Hz floor) that trick your ears into hearing deep bass the physical speakers can't produce.
*   **Exciter**: Adds slight saturation to make the audio "pop" and feel less muddy.
*   **Compressor & Limiter**: Safely maximizes the laptop's volume output without allowing the speakers to crackle or blow out.