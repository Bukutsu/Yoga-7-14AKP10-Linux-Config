# Yoga 7 14AKP10 — system\_config

Personal documentation and configuration for my **Lenovo Yoga 7 2-in-1** (AMD Ryzen AI 7 350, 32GB, Arch Linux / CachyOS kernel).

## Directories

| Path | What |
|------|------|
| `docs/` | How‑tos and notes about this laptop |
| `configs/` | Config files — drag and drop into their destinations |
| `scripts/` | Tools I wrote to make life easier |

## Highlights

- **Docs** — installation, audio tuning (ALC3306 4‑speaker), CachyOS de‑branding, Limine theming, Flatpak font sync, battery optimization
- **Configs** — sched‑ext scheduler profiles tuned for Strix Point (P‑core / E‑core), Dolby Atmos IRs and EasyEffects presets, WiFi power‑save disable (RTL8922AE), fontconfig for Thai and Flatpak
- **Scripts** — `arch-fortify.py` for persistent de‑branding, `setup-flatpak-fonts.sh` for host Flatpak font sync

## Quick start

```bash
# Copy system configs
sudo cp -r configs/system/* /etc/

# Optional: de‑brand CachyOS
sudo ./scripts/arch-fortify.py

# Fix Flatpak font rendering
./scripts/setup-flatpak-fonts.sh
```

See `docs/` for the full story.
