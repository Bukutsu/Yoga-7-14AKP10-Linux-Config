# Changelog

All notable changes to this system configuration are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project uses dates (YYYY-MM-DD) for tracking real-world updates.

## [Unreleased]

## [2026-05-14]

### Added
- **Biopass PAM setup guide** (`docs/BIOPASS_PAM_SETUP.md`)
  - Complete AUR installation instructions
  - Working PAM config using `sufficient` flag (fixes `[success=2 default=ignore]` bug on Arch)
  - Step-by-step deployment with safety checks
  - Testing procedures for sudo and GDM unlock
  - Migration path from fingerprint PAM (`pam_fprintd`)
  - Bug report template for upstream

### Fixed
- PAM configuration now uses portable `sufficient` flag instead of `[success=n default=ignore]`
  - Resolves issue where biopass would succeed but still prompt for password
  - Verified working on Arch Linux + GNOME

## [2026-05-11]

### Added
- Initial repository structure (LICENSE, CONTRIBUTING, etc.)
- README with quick navigation

## [Before 2026-05-11]

### Documentation
- `AUDIO_TUNING.md` — ALC3306 speaker tuning, EasyEffects, Dolby Atmos IRs
- `DEBRANDING.md` — Removing CachyOS branding
- `INSTALL_GUIDE.md` — Fresh Arch/CachyOS installation
- `LIMINE_THEMING.md` — Bootloader customization
- `TRANSFORM_TO_ARCH.md` — CachyOS → Arch migration

### Configurations
- **Audio:** EasyEffects presets (Dolby, Harman), PEQ filters
- **System:** sched-ext profiles, WiFi power-save configs
- **Font:** Thai support, Flatpak font syncing

### Scripts
- `arch-fortify.py` — Persistent de-branding automation
- `setup-flatpak-fonts.sh` — Host → Flatpak font synchronization

---

## Device Specs (This Configuration)

- **Model:** Lenovo Yoga 7 2-in-1 (14AKP10)
- **CPU:** AMD Ryzen AI 7 350
- **RAM:** 32GB LPDDR5X
- **Storage:** SSD (NVMe)
- **Audio:** Realtek ALC3306 (4 speakers) + Dolby Atmos
- **WiFi:** Realtek RTL8922AE
- **Display:** 14" 2.8K OLED touchscreen
- **OS:** Arch Linux (or CachyOS with kernel tuning)

---

## Maintenance Notes

### Regular Checks
- **Monthly:** Run `pacman -Syu` and test audio/biopass after kernel updates
- **Quarterly:** Check for new sched-ext scheduler profiles
- **Annually:** Review `docs/` for outdated links or deprecated tools

### Known Limitations
- Some configs are Yoga 7-specific (audio IRs, speaker tuning)
- WiFi driver (`rtl8922ae`) may need re-tuning after Arch updates
- CachyOS branding requires re-application after system upgrades

### Troubleshooting
See individual docs in `docs/` for specific systems:
- Audio issues → `AUDIO_TUNING.md`
- Boot problems → `LIMINE_THEMING.md`
- Biometric auth → `BIOPASS_PAM_SETUP.md`
- Fresh install → `INSTALL_GUIDE.md`

---

**Last Updated:** 2026-05-14  
**Maintainer:** bukutsu
