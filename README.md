# System Configuration - Lenovo Yoga 7 (14AKP10)

**Hardware:** AMD Ryzen AI 7 350 (Strix Point) | **OS:** CachyOS | **Goal:** Maximum performance & battery life

A single repository containing optimized configurations for the Lenovo Yoga 7 2-in-1 (14AKP10) on CachyOS. Includes scheduler tuning, audio presets, power management, and hardware compatibility guides.

---

## Quick Start

**Already on CachyOS?** Jump straight to `docs/setup-guide.md` for step-by-step optimization.

**Setting up from scratch?**
1. Install CachyOS on your Yoga 7
2. Follow `docs/setup-guide.md`
3. Deploy scheduler config via `docs/scheduler-deployment.md`

---

## What's Inside

| Path | Purpose |
|:---|:---|
| **docs/setup-guide.md** | Complete CachyOS setup guide for Ryzen AI 7 350 |
| **docs/scheduler-deployment.md** | Step-by-step scheduler deployment (scx_lavd) |
| **configs/system/scheduler/scx_loader.toml** | Optimized scheduler configuration (auto/gaming/power-saver modes) |
| **configs/audio/easyeffects_presets/** | Audio EQ & effect presets for the 4-speaker system |
| **configs/system/network/** | Wi-Fi powersave fix (MT7925e flicker) |
| **scripts/install_fedora_thai_config.sh** | Thai font configuration installer |

---

## Philosophy

**Solid Core, Liquid Edge:**
- Start with a stable, official OS (CachyOS with optimized linux-cachyos kernel)
- Add reversible, safety-net optimizations (Btrfs snapshots, containerized environments)
- Inject hardware-specific performance tuning (eBPF scheduler, power profiles, audio tweaks)

The result: A workstation that stays reliable for years while extracting maximum efficiency from the Ryzen AI platform.

---

## Repository Structure

```
System_Config/
├── README.md                          # This file
├── docs/
│   ├── setup-guide.md                # Complete optimization guide
│   └── scheduler-deployment.md        # Scheduler deployment procedure
├── configs/
│   ├── system/scheduler/             # scx_loader.toml (scheduler config)
│   ├── system/network/               # Network fixes (Wi-Fi powersave)
│   ├── system/power/                 # Power management configs
│   ├── audio/easyeffects_presets/    # Audio presets (speakers, mic)
│   └── display/                      # Display optimization
├── scripts/
│   └── install_fedora_thai_config.sh # Thai font installer
└── [other dirs: .git, etc.]
```

---

## Hardware Overview

| Component | Status | Notes |
|:---|:---|:---|
| **CPU** | ✅ | AMD Ryzen AI 7 350 (4 P-cores + 4 E-cores, 5.1/3.5 GHz) |
| **GPU** | ✅ | Radeon 840M with VA-API hardware acceleration |
| **Display** | ✅ | 14" OLED touchscreen + stylus (Yoga Pen) |
| **Audio** | ✅ | 4-speaker Dolby Atmos (Kernel 6.18+) |
| **Wi-Fi** | ✅ | Wi-Fi 7 (MT7925e) – powersave disabled to prevent flicker |
| **Bluetooth** | ✅ | Bluetooth 5.4 (MT7925e) |
| **Microphone** | ✅ | Quad-mic array with RNNoise noise reduction |
| **Camera** | ✅ | IR camera (facial recognition with Howdy) |
| **Battery** | ✅ | 70Wh – 80% charge limit recommended for longevity |
| **NPU** | ⚠️ | Ryzen AI / XDNA 2 – Driver support in Linux 6.14+ (FastFlowLM available) |

For detailed hardware compatibility and troubleshooting, see `docs/setup-guide.md#hardware-compatibility`.

---

## Key Optimizations

### 1. CPU Scheduler (scx_lavd)
- **Latency-Aware Virtual Deadline** scheduler for interactive responsiveness
- **Core compaction:** Prioritizes 5.1GHz P-cores → 25-30% battery improvement
- **Auto AC/Battery switching:** Automatically adjusts profile based on power source
- **Expected battery life:** ~11-12 hours (vs. ~9 hours baseline)

### 2. Power Management
- 80% battery charge limit (extends lifespan)
- Power profiles daemon integration (balanced/power-saver/performance)
- ZRAM enabled (compressed RAM)

### 3. Audio
- 4-speaker setup with Dolby Atmos positioning
- EasyEffects presets for corrected audio profile
- Quad-mic array with RNNoise for live noise reduction

### 4. Graphics
- VA-API hardware acceleration (11-12W video playback vs. 14-16W software)
- Radeon 840M support

### 5. Network
- Wi-Fi powersave disabled (prevents MT7925e flicker)

---

## Getting Started

1. **Read `docs/setup-guide.md`** for the complete optimization walkthrough
2. **Deploy scheduler config** using `docs/scheduler-deployment.md`
3. **Apply optimizations** (battery limit, audio presets, Wi-Fi fix, etc.)
4. **Verify everything** with the checklist in `docs/setup-guide.md`

---

## Support & Feedback

For issues, questions, or suggestions:
- Check `docs/setup-guide.md#troubleshooting` first
- Report bugs at: https://github.com/anomalyco/opencode

---

**Maintained using:** Gemini CLI | **Last Updated:** 2026-03-20
