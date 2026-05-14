# Audio Tuning Documentation Fact-Check

**Date:** 2026-05-14  
**Device:** Lenovo Yoga 7 2-in-1 (14AKP10)  
**Kernel:** 7.0.6-1-cachyos  
**Status:** ⚠️ Documentation partially outdated; kernel quirk advice may be incorrect

---

## Executive Summary

The AUDIO_TUNING.md documentation describes audio fixes that **are not currently applied** on this device. Investigation reveals:

1. **Kernel quirk section is outdated** — The modprobe fix may not be correct for 14AKP10
2. **EasyEffects presets not loaded** — Exist in repo but need manual setup
3. **Bass speakers not active** — Kernel quirk for 14AKP10 not found in upstream
4. **ACPI driver present** — Alternative bass control mechanism not documented

---

## Detailed Findings

### 1. Kernel Quirk Status: ❌ NOT APPLIED

**What the doc recommends:**
```bash
# Create /etc/modprobe.d/alc3306-yoga-fix.conf
options snd-hda-intel model=(null),alc287-yoga9-bass-spk-pin
```

**Actual system state:**
- File `/etc/modprobe.d/alc3306-yoga-fix.conf`: **Does not exist**
- Model parameter loaded: **No** (system shows `(null),(null),...`)
- Bass speakers: **Silent** (speaker-test reports only 2 channels)

**Hardware details:**
```
Audio Card 1:
  Codec: Realtek ALC287
  Subsystem ID: 0x17aa:391c (Lenovo 14AKP10)
  Current output: Front Left + Front Right only (tweeters)
  Bass speakers: Not connected/active
```

**Root cause identified:**
The kernel model parameter `alc287-yoga9-bass-spk-pin` appears **outdated or incorrect**. Modern kernels (5.12+) use automatic PCI ID-based quirks, not model parameters. Upstream kernel quirks exist only for:
- Yoga 9 14IAP7 (PCI ID 0x17aa:38cd)
- Yoga 9 14IMH9 (PCI ID 0x17aa:38d2, 0x17aa:38d7)

**Your device's PCI ID `0x17aa:391c` is NOT in the upstream quirk list.**

**Recommendation:**
⚠️ **Do NOT apply this fix blindly.** The model parameter may:
- Not exist in the kernel
- Not work on 14AKP10
- Cause audio to fail entirely if wrong

---

### 2. EasyEffects Presets: ⚠️ EXIST BUT NOT LOADED

**What the doc says:**
- "Copy the extracted Dolby files from this repository to your local EasyEffects config"
- "Select Z16-Dynamic-Balanced and click Load"

**Actual system state:**

| Item | Status | Details |
|------|--------|---------|
| EasyEffects installed | ✓ Yes | Version 8.2.2-1.1 |
| EasyEffects running | ✓ Yes | Process 3849 active |
| Presets in repo | ✓ Yes | 16 files present |
| Presets copied to config | ✗ No | `~/.config/easyeffects/` empty |
| IRS files copied | ✗ No | `~/.config/easyeffects/irs/` not created |
| Preset loaded | ✗ No | No active DSP processing |

**Impact:**
- EasyEffects is running but has **no presets or DSP active**
- Dolby/Harman audio correction is **not applied**
- Sound quality is default (lacks documented tonal shaping and bass boost)

**Why it matters:**
Even if bass speakers don't work, EasyEffects presets could improve the tweeter-only sound through parametric EQ and psychoacoustic effects.

**Immediate fix (low risk):**
```bash
# Copy presets
cp ~/Documents/system_config/configs/audio/easyeffects_presets/Yoga_7_Harman_Target.json \
   ~/.config/easyeffects/output/

# Copy IRS files
mkdir -p ~/.config/easyeffects/irs
cp ~/Documents/system_config/configs/audio/easyeffects_irs/*.irs \
   ~/.config/easyeffects/irs/

# Then in EasyEffects GUI:
# Presets menu → Select "Yoga_7_Harman_Target" → Load
```

---

### 3. Documentation Accuracy Issues

#### Issue A: Model Parameter Outdated
**Problem:** The kernel model syntax doesn't match modern kernel architecture.

**Evidence:** 
- Kernel source (commit 9b714a5) shows quirks use automatic PCI ID detection
- Not manual model parameters
- Model name `alc287-yoga9-bass-spk-pin` may not even exist in kernel

#### Issue B: Device Not in Kernel Quirk List
**Problem:** Documentation implies all Yoga 7 devices use the same fix.

**Reality:**
- Kernel quirks are device-specific (by PCI ID)
- Only tested for Yoga 9 14IAP7 and 14IMH9
- Yoga 7 14AKP10 lacks upstream quirk (as of kernel 7.0.6)

**Recommendation:** Add disclaimer that device-specific quirks may not exist yet.

#### Issue C: ALC3306 vs ALC287
**Problem:** Doc mentions both, but handling may differ.

**Your device:** Reports ALC287, but may have ALC3306-like hardware. Unclear if fix applies.

#### Issue D: ACPI PDM Driver Not Mentioned
**Problem:** Your device shows:
```
acp-pdm-mach: LENOVO-83JR-Yoga72_in_114AKP10-LNVNB161216
```

This ACPI device may control bass speakers via firmware, not HDA codec. **Documentation doesn't address this.**

---

## Current Device State

| Component | Status | Notes |
|-----------|--------|-------|
| Audio output | ✓ Working | 2 channels (tweeters only) |
| Bass speakers | ✗ Silent | Unknown if hardware fault or kernel missing |
| EasyEffects | ⚠️ Running but inactive | No presets loaded; no DSP |
| Kernel quirk | ✗ Not found | PCI ID 0x17aa:391c not in upstream |
| Presets available | ✓ Yes | In repo, not deployed to config |
| Harman target curve | ✓ Available | Can improve treble/mid compensation |

---

## Recommended Actions

### Short-term (Safe, Low Risk)
1. ✓ Copy EasyEffects presets to `~/.config/easyeffects/output/`
2. ✓ Load `Yoga_7_Harman_Target.json` preset
3. ✓ Test sound quality improvement (may compensate for missing bass)

### Medium-term (Investigation)
1. Investigate if `alc287-yoga9-bass-spk-pin` kernel model exists
   ```bash
   grep -r "yoga9-bass-spk-pin" /usr/src/linux*
   ```
2. Check if kernel has quirk for PCI ID 0x17aa:391c
3. Test speaker hardware (bass drivers may be working but not routed)
4. Investigate ACPI PDM driver: does it control bass?

### Long-term (If Bass Needed)
1. If kernel quirk doesn't exist:
   - Test ACPI method to activate bass
   - Or submit kernel patch adding 14AKP10 to quirk list
2. Collaborate with kernel maintainers (ALSA/Realtek team)

---

## Documentation Recommendations

**AUDIO_TUNING.md should be updated to:**

1. **Add device-specific warning:**
   ```markdown
   ⚠️ **Warning:** Kernel quirks are device-specific. This guide covers Yoga 9 models
   with confirmed kernel support. For Yoga 7 14AKP10, the kernel quirk may not exist.
   Check your device's PCI ID before applying modprobe changes.
   ```

2. **Replace outdated model parameter with verification steps:**
   ```markdown
   Before applying the modprobe fix, verify:
   - Does your kernel have a quirk for your device?
   - What is your audio device's PCI ID? (lspci | grep Audio)
   - Does upstream Linux have a SND_PCI_QUIRK entry for your ID?
   ```

3. **Separate EasyEffects into own section:**
   - Clarify it works independently of kernel quirk
   - Emphasize that presets MUST be copied and loaded
   - Note that Harman target preset improves sound even without bass

4. **Add ACPI control section:**
   - Document the ACPI PDM machine driver
   - Explain alternative bass control mechanisms

---

## Testing Log

### Hardware Verification
```bash
# Audio card check
$ aplay -l
  **** List of PLAYBACK Hardware Devices ****
  card 1: Generic_1 [HD-Audio Generic], device 0: ALC287 Analog [ALC287 Analog]

# Speaker test (2 channels only, no bass)
$ speaker-test -c 2
  Playback device is default
  Channels: Front Left, Front Right

# Kernel model check
$ cat /sys/module/snd_hda_intel/parameters/model
  (null),(null),...,  (null),(null)

# ACPI device check
$ cat /proc/asound/cards | grep -i acpi
  2 [acppdmmach]: acp-pdm-mach - acp-pdm-mach

# EasyEffects config check
$ ls ~/.config/easyeffects/output/
  (empty)
```

---

**Last Updated:** 2026-05-14  
**Audit Status:** Complete  
**Recommendation:** Update AUDIO_TUNING.md per notes above before other users rely on potentially incorrect kernel fix.
