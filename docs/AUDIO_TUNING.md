# Audio Tuning for Lenovo Yoga 7 (Linux)

Getting the best audio out of your Lenovo Yoga 7 (and other modern Lenovo laptops with the ALC3306 or ALC287 codecs) on Linux requires two major steps:
1. Fixing the hardware mapping so all 4 speakers (2 tweeters, 2 woofers) fire.
2. Applying DSP (Digital Signal Processing) to correct the sound signature and maximize loudness without clipping, simulating the "Dolby Atmos" experience you get on Windows.

---

## 1. The Kernel Quirk (Fixing "Tinny" Sound)

⚠️ **IMPORTANT:** For Lenovo Yoga 7 2-in-1 14AKP10, see [KERNEL_QUIRK_FIX.md](KERNEL_QUIRK_FIX.md) for the correct fix. This section is outdated.

By default, the Linux kernel often misidentifies the ALC287/ALC3306 chip and fails to route audio to the bottom bass speakers. This is a **BIOS firmware issue** where Pin 0x17 (bass speakers) is incorrectly marked as unconnected.

### For Yoga 7 2-in-1 14AKP10 (Device SSID 0x17aa:391c)

See **[KERNEL_QUIRK_FIX.md](KERNEL_QUIRK_FIX.md)** for:
- The actual kernel patch that fixes your device
- When it will be available (Linux 6.14+)
- How to apply it now (kernel upgrade or modprobe workaround)

### For Other Yoga/Thinkpad Models

If you have a different model, the fix process varies:

1. Identify your audio card and codec SSID:
   ```bash
   aplay -l                              # Check card number
   cat /proc/asound/card1/codec* | grep "Subsystem Id"  # Your SSID
   ```

2. Search kernel source for your device SSID:
   ```bash
   grep -r "0x391c" /usr/src/linux*     # Replace 391c with your SSID
   ```

3. If your device is in the kernel:
   - Upgrade to a kernel version that includes your quirk
   - No manual modprobe needed (automatic)

4. If your device is NOT in the kernel:
   - Submit a bug report to kernel ALSA maintainers
   - Or apply a workaround modprobe temporarily
   - See [KERNEL_QUIRK_FIX.md](KERNEL_QUIRK_FIX.md) for modprobe option

---

## 2. EasyEffects "Dolby DAX3" Extracted Presets

To truly replicate the Windows sound experience, we use presets extracted directly from Lenovo's official Dolby DAX3 Windows audio drivers. The presets provided in this repository are from the ThinkPad Z16 Gen 1 (which shares a very similar 4-speaker, ALC3306 hardware design with your Yoga).

These presets use a "Convolver" plugin to load an Impulse Response (IRS) file—an acoustic measurement that corrects the physical limitations of your laptop chassis and perfectly mimics Dolby Atmos spatial widening and EQ.

### Installation

1. Install EasyEffects from your distribution's repository:
```bash
sudo pacman -S easyeffects
```
*(Make sure optional dependencies like `lsp-plugins-lv2`, `zam-plugins-lv2`, and `mda.lv2` are installed if you want full effect compatibility).*

2. Create the necessary EasyEffects directories if they don't exist:
```bash
mkdir -p ~/.config/easyeffects/irs
mkdir -p ~/.config/easyeffects/output
```

3. Copy the extracted Dolby files from this repository to your local EasyEffects config:
```bash
cp configs/audio/easyeffects_irs/*.irs ~/.config/easyeffects/irs/
cp configs/audio/easyeffects_presets/ThinkPad_Z16_Dolby/*.json ~/.config/easyeffects/output/
```

4. Open EasyEffects, go to **Preferences** (top-right menu) and enable **Launch Service at System Startup**.
5. Go to the **Presets** menu (top-left). You will now see a list of `Z16-` presets (e.g., `Z16-Dynamic-Balanced`, `Z16-Music-Detailed`).
6. Select **Z16-Dynamic-Balanced** (the default Windows experience) and click **Load**.

### What these presets do:
*   **Convolver (IRS)**: Accurately replicates Lenovo's Dolby Atmos acoustic correction curve specifically designed for this chassis style.
*   **Stereo Widening (`stereo_tools`)**: Widens the soundstage to match the cinematic feel of Dolby.
*   **Targeted EQ (`equalizer`)**: Exact frequency boosts and cuts pulled from the official Windows driver XML files.
*   **Maximized Loudness (`limiter`)**: Smooths out volume spikes and pushes the average loudness up safely without letting the speakers clip, crackle, or distort.

---

## 3. The "Harman Target" Curve (Audiophile Alternative)

If you prefer a sound signature modeled after the industry-standard **Harman Target Curve** (which simulates flat studio monitors in a treated room), we have crafted a native preset: `Yoga_7_Harman_Target.json`.

This preset does **not** use the Dolby Convolver. Instead, it relies on precise Parametric EQ and Bass Harmonics to:
1. **Push vocals forward** (+4.5dB at 3000Hz).
2. **Add punchy warmth** (+3.0dB at 105Hz).
3. **Tame the screech** (-2.0dB at 5500Hz to remove harsh laptop tweeter resonance).

### Installation:
1. Copy the preset from the repo to your local EasyEffects output directory (depending on your EasyEffects version, this is either in `~/.config/` or `~/.local/share/`):
```bash
cp configs/audio/easyeffects_presets/Yoga_7_Harman_Target.json ~/.local/share/easyeffects/output/
# OR
cp configs/audio/easyeffects_presets/Yoga_7_Harman_Target.json ~/.config/easyeffects/output/
```
2. Open EasyEffects, go to **Presets**, select **Yoga_7_Harman_Target**, and click **Load**.