# AGENTS.md — Abigail

## Hardware

- **Laptop** — Lenovo Yoga 7 2-in-1 14AKP10 (83JR)
- **CPU** — AMD Ryzen AI 7 350 w/ Radeon 860M (Strix Point, Zen 5, 8C/16T)
- **RAM** — 32GB
- **Storage** — 1TB NVMe SSD
- **WiFi** — Realtek RTL8922AE (WiFi 7)
- **Display** — 2.8K 120Hz OLED
- **OS** — Arch Linux w/ CachyOS kernel (Limine bootloader, GNOME Wayland)
- **Shell** — Fish · **Terminal** — Ghostty

## Constraints

- **Android device** — Banking app blocks developer options. Do **not** enable USB debugging or developer options.
- **System changes** — User prefers "plan first". Wait for explicit approval before executing system-modifying commands.
- **Security** — Avoid untrusted packages. Prefer official repos or well-vetted AUR packages.

## Goals (in order)

1. **Battery life** — maximise runtime (target: 3–4W idle, 6–7W YouTube)
2. **Longevity** — keep hardware running long-term while staying updated
3. **Minimal maintenance** — set-and-forget, avoid break-prone upgrade events

## Workflow

### Research approach

1. Define problem & constraints
2. Search official channels (Arch Wiki, `pacman -Ss`, AUR, upstream docs)
3. Evaluate community solutions (activity, license, feedback)
4. Test feasibility (dependencies, integration, user reports)
5. Document findings — create plan in `.opencode/plans/`
6. Record successful approach — update this file

### Decision thresholds

| Context | Action |
|---------|--------|
| System config (`/etc/`), service restarts, package installs, bootloader, kernel | Ask first |
| Reading logs, checking status, querying hardware | Just do it |
| Anything that could prevent boot, removing critical packages, modifying `/boot/limine.conf` | Explicit approval required |

### Communication

- Direct answers, no fluff
- Honest trade-offs, not marketing
- One sentence when possible
- Link to existing docs rather than re-summarising

## Known issues

- **Screen recording** — OBS/Discord screen share glitchy on GNOME 49.x (mutter ↔ PipeWire timing). Wait for GNOME 50 (~1–2 weeks).
- **UFW** — Not needed behind NAT router with no exposed services. Can be disabled.
- **limine-snapper-restore** — Hardcodes terminal list, missing Ghostty. Fix via `~/.config/environment.d/override.conf`.

## Common scenarios

| Issue | Status | Reference |
|-------|--------|-----------|
| Battery optimisation | Done | Kernel params `amd_pstate=active pcie_aspm=force` |
| CPU scheduling | Done | scx_lavd with custom TOML profiles in `configs/system/scheduler/` |
| Audio (4 speakers) | Done | ALC3306 quirk + EasyEffects presets in `configs/audio/` |
| Screen recording | Waiting | GNOME 50 |
| CachyOS de-branding | Done | `scripts/arch-fortify.py` |
| Flatpak fonts | Done | `scripts/setup-flatpak-fonts.sh sync` |

## Docs map

- `docs/INSTALL_GUIDE.md` — CachyOS + Limine installation
- `docs/TRANSFORM_TO_ARCH.md` — exit strategy to vanilla Arch
- `docs/AUDIO_TUNING.md` — ALC3306 quirk + EasyEffects setup
- `docs/LIMINE_THEMING.md` — Tokyo Night Dark theme
- `docs/DEBRANDING.md` — GDM / Plymouth / identity cleanup

## Quick ref

```bash
# Battery draw
sudo powertop

# GPU encoding support
vainfo

# Audio
pactl list cards

# Scheduler
systemctl status scx_loader

# Recent errors
journalctl -p err -b --no-pager

# Kernel command line
cat /proc/cmdline
```

> Working with Yoga 7 14AKP10 (CachyOS/Arch, Fish, Ghostty). Goals: battery life, longevity, minimal maintenance. Ask before system changes. Docs in `docs/`. Known issue: screen recording wait for GNOME 50.
