# Yoga 7 14AKP10 System Configuration

> Personal hardware tuning, installation notes, and configuration for a **Lenovo Yoga 7 2-in-1** (14AKP10) running Arch Linux with AMD Ryzen AI 7 350.

This repo documents the entire setup process, hardware-specific optimizations, and automation tools for this specific device. It's designed as both a **personal backup** and a **reference** for others with similar hardware.

---

## ✨ What's in Here

### 📖 Documentation (`docs/`)

Step-by-step guides for this specific device:

| Doc | Purpose |
|-----|----------|
| [INSTALL_GUIDE.md](docs/INSTALL_GUIDE.md) | Fresh Arch/CachyOS installation and post-install tweaks |
| [AUDIO_TUNING.md](docs/AUDIO_TUNING.md) | Realtek ALC3306 speaker tuning, EasyEffects presets, Dolby Atmos |
| [BIOPASS_PAM_SETUP.md](docs/BIOPASS_PAM_SETUP.md) | Biometric face authentication via biopass (AUR) |
| [DEBRANDING.md](docs/DEBRANDING.md) | Remove CachyOS branding and revert to vanilla Arch |
| [LIMINE_THEMING.md](docs/LIMINE_THEMING.md) | Custom bootloader styling with Limine |
| [TRANSFORM_TO_ARCH.md](docs/TRANSFORM_TO_ARCH.md) | Complete migration from CachyOS to pure Arch Linux |

### ⚙️ Configuration Files (`configs/`)

Ready-to-use system configs:

```
configs/
├── system/etc/          ← Copy to /etc/
│   ├── modprobe.d/      WiFi driver tuning (RTL8922AE)
│   ├── fontconfig/      Thai font support, Flatpak fonts
│   └── default/         System defaults
└── audio/
    ├── easyeffects/     EasyEffects presets (Music, Gaming, Calls, etc.)
    └── eq/              Parametric EQ curves for target response
```

### 🔧 Automation Scripts (`scripts/`)

- **`arch-fortify.py`** — Persistent de-branding (runs on every boot if CachyOS is detected)
- **`setup-flatpak-fonts.sh`** — Syncs host fonts into Flatpak sandbox

---

## 🚀 Quick Start

### New Installation

```bash
# Clone this repo
git clone https://github.com/Bukutsu/Yoga-7-14AKP10-Linux-Config.git
cd Yoga-7-14AKP10-Linux-Config

# Read the installation guide first
cat docs/INSTALL_GUIDE.md

# Then apply system configs
sudo cp -r configs/system/* /etc/

# Set up automation
sudo cp scripts/arch-fortify.py /usr/local/bin/
chmod +x /usr/local/bin/arch-fortify.py

# Optional: Set up font syncing
./scripts/setup-flatpak-fonts.sh
```

### For Your Own Device

1. **Fork this repo** — it's Yoga 7-specific (audio profiles, WiFi driver, scheduler tuning)
2. **Adapt the paths** — replace hardware-specific configs with yours
3. **Copy the structure** — keep `docs/`, `configs/`, `scripts/` organization
4. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

## 📋 Device Specs

| Part | Detail |
|------|--------|
| **Model** | Lenovo Yoga 7 2-in-1 (14AKP10) |
| **CPU** | AMD Ryzen AI 7 350 |
| **RAM** | 32GB LPDDR5X |
| **Storage** | NVMe SSD |
| **Display** | 14" 2.8K OLED, 120Hz, touchscreen |
| **Audio** | Realtek ALC3306 (4-speaker Dolby Atmos) |
| **WiFi** | Realtek RTL8922AE |
| **OS** | Arch Linux (ex-CachyOS) |
| **Kernel** | Linux (vanilla or sched-ext variant) |

---

## 📚 Full Documentation Index

- **[CHANGELOG.md](CHANGELOG.md)** — Version history and dates
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to submit changes
- **[LICENSE](LICENSE)** — MIT (feel free to fork and adapt)

---

## 🔍 Troubleshooting Quick Links

- **Audio cutting out?** → See [AUDIO_TUNING.md](docs/AUDIO_TUNING.md#troubleshooting)
- **WiFi dropping?** → Check `configs/system/etc/modprobe.d/rtl8922ae.conf`
- **Biopass not working?** → See [BIOPASS_PAM_SETUP.md](docs/BIOPASS_PAM_SETUP.md#verification--testing)
- **Boot stuck?** → See [LIMINE_THEMING.md](docs/LIMINE_THEMING.md) or [TRANSFORM_TO_ARCH.md](docs/TRANSFORM_TO_ARCH.md)
- **Fresh install?** → Start with [INSTALL_GUIDE.md](docs/INSTALL_GUIDE.md)

---

## 🛠 Maintenance

- **After kernel updates:** Re-run audio tests; WiFi driver may need rebuilding
- **Monthly:** `pacman -Syu` and spot-check key services (biopass, audio)
- **Quarterly:** Review new sched-ext scheduler updates
- **Annually:** Check [CHANGELOG.md](CHANGELOG.md) for deprecations

---

## 📝 Notes

- This is a **personal repo**, but you're welcome to fork and adapt for your device
- All configs are **Arch Linux-specific** (Pacman, systemd, PAM)
- Audio tuning is **Yoga 7-specific** (ALC3306, Dolby Atmos target curve)
- Biopass setup works for any Linux system with face recognition hardware

---

**Last Updated:** 2026-05-14  
**Status:** Actively maintained  
**License:** MIT
