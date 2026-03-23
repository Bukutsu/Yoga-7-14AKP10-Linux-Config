# Agent Instructions

Linux helper for **Lenovo Yoga 7 2-in-1 14AKP10 (AMD Ryzen AI 7 350)**.

---

## System Profile

### Hardware
- Laptop: Lenovo Yoga 7 2-in-1 14AKP10 (83JR)
- CPU: AMD Ryzen AI 7 350 w/ Radeon 860M (Strix Point, Zen 5)
- RAM: 32GB
- Storage: 1TB NVMe SSD
- WiFi: Realtek RTL8922AE (WiFi 7)
- Display: 2.8K 120Hz OLED (highest res)

### Distro
- **CachyOS** (Arch-based, rolling release)
- Kernel: CachyOS kernel (x86-64-v4)
- Bootloader: Limine

### Preferences
- Shell: **Fish**
- Terminal: **Ghostty** (primary), gnome-terminal (fallback)
- Desktop: GNOME Wayland
- Audio: EasyEffects with custom presets (Dolby Atmos IRS, Harman Target curve)

---

## Goals & Priorities (in order)

1. **Battery life** — Maximize runtime on 84Wh battery (target: 3-4W idle, 6-7W YouTube)
2. **Longevity** — Keep hardware running long-term while staying updated
3. **Minimal maintenance** — Set-and-forget, avoid upgrade events that can break

---

## Problem-Solving Approach

### Research First, Then Act
- For new optimizations: verify on actual hardware before recommending
- Check existing docs in repo first (`docs/` directory) — many answers already documented
- When uncertain: ask clarifying questions rather than guess

### Communication Style
- Direct answers, no fluff
- Honest trade-offs, not marketing
- One sentence if possible, paragraphs only when needed

### Documentation-First
- All solutions should be documented in the repo
- Create/extend docs when solving recurring issues
- Link to existing docs rather than re-summarizing

---

## Decision Thresholds

### Ask Before Doing
- System config changes (`/etc/`)
- Service restarts (`systemctl`)
- Package installs/removals (except readonly queries)
- Bootloader modifications
- Kernel changes

### Just Do It
- Reading logs (`journalctl`, `dmesg`)
- Checking status (`systemctl status`, `pacman -Q`)
- Querying hardware (`vainfo`, `lspci`, `cat /proc/...`)
- Non-destructive diagnostics

### Always Require Explicit Approval
- Anything that could prevent boot
- Removing packages that could break the system
- Modifying `/boot/limine.conf` entries outside of theme changes

---

## Known Issues

### Screen Recording (Wait for GNOME 50)
- OBS and Discord screen share have glitchy frames on GNOME 49.x
- Root cause: mutter ↔ PipeWire frame delivery timing
- Fix: GNOME 50 has improved frame scheduling for screencasting
- Estimated: ~1-2 weeks until CachyOS ships GNOME 50
- Alternative: Use non-PipeWire recording apps (temporary workaround)

### UFW
- Not needed — laptop behind NAT router with no exposed services
- Can be disabled: `sudo ufw disable` + `sudo systemctl mask ufw`

### Terminal for limine-snapper-restore
- Script hardcodes terminal list, missing Ghostty
- Fix: Set `TERMINAL=ghostty` and `TERMINAL_ARG=-e` in `~/.config/environment.d/override.conf`

---

## Common Scenarios Reference

| Issue | Status | Reference |
|---|---|---|
| Battery optimization | ✅ Done | Kernel params `amd_pstate=active pcie_aspm=force` |
| CPU scheduling | ✅ Done | scx_lavd with custom TOML profiles |
| Audio (4 speakers) | ✅ Done | ALC3306 quirk + EasyEffects presets |
| GNOME screen recording | ⏳ Waiting | Wait for GNOME 50 |
| Distro choice | ✅ Decided | CachyOS (exit strategy in `TRANSFORM_TO_ARCH.md`) |
| Firewall | ✅ Not needed | UFW disabled |

---

## System Monitoring Commands

```bash
# Battery power draw
sudo powertop

# GPU/video encoding support
vainfo

# Audio device info
pactl list cards

# Scheduler status
systemctl status scx_loader
scx-manager status

# Recent system logs
journalctl -p err -b --no-pager

# Kernel command line
cat /proc/cmdline
```

---

## Documentation Map

- `docs/INSTALL_GUIDE.md` — Full CachyOS + Limine installation
- `docs/TRANSFORM_TO_ARCH.md` — Exit strategy to vanilla Arch
- `docs/AUDIO_TUNING.md` — ALC3306 quirk + EasyEffects setup
- `docs/LIMINE_THEMING.md` — Tokyo Night Dark theme
- `docs/DEBRANDING.md` — GDM/Plymouth cleanup

---

## Quick Reference

When starting a new session, paste this summary:

> Working with Yoga 7 14AKP10 (CachyOS/Arch, Fish, Ghostty). Goals: battery life, longevity, minimal maintenance. Ask before system changes. Docs in `docs/`. Known issue: screen recording wait for GNOME 50.