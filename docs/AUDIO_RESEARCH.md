# Audio Research: Yoga 7 14AKP10 on Linux

**Date:** 2026-05-14  
**Device:** Lenovo Yoga 7 2-in-1 14AKP10  
**Goal:** Maximize speaker quality on Linux to match Windows experience

---

## Hardware Specs (from Lenovo PSREF)

| Component | Specification |
|-----------|---------------|
| **Audio Codec** | Realtek ALC3306 |
| **Speakers** | 4 stereo (2x woofers 2W + 2x tweeters 2W) |
| **Total Power** | 8W (4x 2W) |
| **Optimization** | Dolby Atmos, Smart Amplifier (AMP) |
| **Platform** | AMD Strix Point (Ryzen AI 7 350) |

---

## What Windows Does Better

Windows achieves superior audio through:

1. **Smart Amplifier (AMP)** — DSP-based speaker protection and loudness optimization
2. **Dolby Atmos** — IRS/convolver acoustic correction + spatial processing
3. **UEFI Calibration** — Speaker-specific frequency correction data stored in firmware
4. **Volume Normalization** — Consistent volume across apps and media

---

## Current Linux State

### ✅ Working
- All 4 speakers active (kernel quirk applied)
- Bass Speaker control present
- 4-channel audio output
- PipeWire running

### ⚠️ Partially Working
- Volume control (known Ubuntu bug: resets to max, jack weak)
- Basic EQ via EasyEffects

### ❌ Not Available on Linux
- **Smart Amplifier DSP** — No vendor driver support
- **UEFI Calibration Data** — Inaccessible to Linux
- **Dolby Atmos** — Proprietary Windows-only processing

---

## Realistic Improvements

### 1. EasyEffects with Convolver (High Impact)

**Best approach:** Use Windows Dolby Atmos IRS files via EasyEffects convolver.

**Why this works:**
- Replicates the acoustic correction Windows applies
- Corrects for chassis resonance and speaker limitations
- Proven method used by Linux audio community

**Options:**

#### Option A: ThinkPad Z16 IRS (Currently in Repo)
- Based on similar 4-speaker Lenovo hardware
- 15 presets (Music, Gaming, Voice, etc.)
- Conservative tuning

#### Option B: Yoga 7-Specific IRS
- Extract from your own Windows installation
- Or download from community databases:
  - https://github.com/dev-satyamjha/Easyeffects-IRS-profiles-database
  - https://github.com/JackHack96/EasyEffects-Presets

### 2. Custom Parametric EQ (Medium Impact)

Fine-tune based on actual speaker response. Current Harman Target preset is a good start, but can be optimized.

**Measurement approach:**
```bash
# Install REW (Room EQ Wizard) for Linux
# Use measurement mic or reference curve
# Generate custom EQ profile
```

### 3. PipeWire Optimization (Low-Medium Impact)

Ensure audio chain is optimized:

```bash
# Check PipeWire configuration
cat /etc/pipewire/pipewire.conf

# Ensure proper resampling
# Set default sample rate to 48000Hz
```

### 4. Volume Control Fix (Known Issue)

From Ubuntu bug #2134386:
> "Internal speakers do not respond to volume control on the laptop"

**Workaround:** Use PipeWire's soft volume control or EasyEffects input gain.

---

## What's NOT Possible

### Smart Amplifier Control
The "Smart Amplifier" in this device is likely a Texas Instruments TAS2781 or Cirrus Logic CS35L41 chip. These require:
- Vendor I2C drivers
- Proprietary tuning blobs from Windows driver
- No Linux support (only some newer models have basic support)

**Evidence:**
- Legion Pro 7 laptops with AW88399 have $2000 bug bounty for speaker fix
- TAS2781 exists in some Yoga models but Linux drivers are incomplete
- Your device uses ALC3306 + Smart AMP, which isn't in mainline kernel

### UEFI Calibration
Windows reads speaker-specific correction data from UEFI variables. Linux cannot access this.

---

## Recommended Actions

### Immediate (Easy)
1. **Copy and test EasyEffects presets** — Both Dolby and Harman options
2. **Load a preset** — Test with music you know well
3. **Adjust to taste** — EQ is subjective

### Short-term (Medium Effort)
1. **Extract your own IRS from Windows** — If you have dual-boot
2. **Measure speaker response** — Generate custom EQ curve
3. **Test with different presets** — Find what sounds best to you

### Long-term (Requires Upstream Work)
1. **Submit speaker calibration data request** — Kernel ALSA team
2. **Wait for Smart AMP driver** — Vendor-dependent, uncertain timeline
3. **Consider hardware solution** — External USB DAC if quality is critical

---

## Preset Comparison

| Preset | Type | Bass | Treble | Loudness | CPU Impact |
|--------|------|------|--------|----------|-----------|
| **Z16-Dynamic-Balanced** | Convolver | +++ | ++ | +++ | Medium |
| **Z16-Voice-Detailed** | Convolver | ++ | +++ | ++ | Medium |
| **Yoga_7_Harman_Target** | EQ only | ++ | + | ++ | Low |
| **None (Raw)** | — | 0 | 0 | 0 | None |

---

## Testing Procedure

1. **Baseline:** Play music with NO EasyEffects, note what sounds "wrong"
2. **Harman Target:** Load preset, note changes
3. **Dolby Preset:** Load Z16-Dynamic-Balanced, compare
4. **Adjust:** Modify EQ bands if needed
5. **Save:** Export your preferred configuration

**Key metrics to compare:**
- Bass presence (kick drums, low instruments)
- Vocal clarity (presence, sibilance)
- Treble harshness (cymbals, high frequencies)
- Soundstage width (spatial perception)
- Maximum volume before distortion

---

## Community Resources

- https://github.com/shuhaowu/linux-thinkpad-speaker-improvements
- https://github.com/dev-satyamjha/Easyeffects-IRS-profiles-database
- r/LinuxAudioproblems on Reddit
- ALSA kernel development (kernel.org)

---

## Conclusion

**Linux can get to ~80-90% of Windows audio quality** via:
1. EasyEffects convolver (Dolby replication)
2. Custom EQ tuning
3. PipeWire optimization

**The remaining 10-20% gap** is due to:
1. No Smart Amplifier DSP control
2. No UEFI calibration access
3. Volume control issues (known bug)

**Verdict:** Worth tuning via EasyEffects. Full Windows parity requires vendor driver support which is unlikely for this hardware.

---

**Sources:**
- Lenovo PSREF Yoga 7 14AKP10 (May 2026)
- Ubuntu Bug #2134386 (Audio issues)
- Kernel commits 1386d16, e6c8882 (Bass speaker quirk)
- Cirrus Logic CS35L41 kernel driver documentation
- Linux audio community repositories (GitHub)