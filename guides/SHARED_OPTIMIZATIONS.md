# Shared Optimizations (Lenovo Yoga 7 / Slim 7 14AKP10)

This document centralizes every distro-agnostic tweak referenced by the Arch Hybrid and Fedora Optimized guides. If a section applies to both operating systems, it lives here.

## Hardware Compatibility Snapshot

| Component | Status | Notes |
| --- | --- | --- |
| Radeon 840M/860M GPU | ✅ Works | VA-API via `libva-mesa-driver` (Arch) or `mesa-va-drivers-freeworld` (Fedora) |
| OLED Touchscreen | ✅ Works OOB | `libinput list-devices` confirms touchscreen and stylus |
| Stylus (Yoga Pen) | ✅ Works OOB | Pressure + tilt through evdev/libinput |
| Auto-rotate (tablet mode) | ✅ Works | Requires `iio-sensor-proxy` for GNOME |
| Wi-Fi 7 (MT7925e) | ✅ Works | Disable Wi-Fi powersave to stop flickering |
| Bluetooth 5.4 | ✅ Works OOB | Same MT7925e chip |
| IR camera / Howdy | ✅ Works | Follow [Arch Wiki - Howdy](https://wiki.archlinux.org/title/Howdy) |
| 4 speakers + Dolby Atmos | ✅ Works | Kernel 6.18+ exposes all speaker pins |
| Quad-mic array | ✅ Works | EasyEffects + RNNoise chain |
| MicroSD reader | ✅ Works OOB | Standard SDHCI support |
| USB-C DisplayPort 2.1 | ✅ Works | Provided by Mesa + kernel |
| NPU (Ryzen AI / XDNA 2) | ⚠️ Partial | Linux 6.14–7.1 driver maturation; FastFlowLM ready now |
| Fingerprint reader | ➖ N/A | Not shipped on every SKU |

## Battery Charge Limit (80%)
- KDE Plasma 6.1+: System Settings → Power Management → Advanced → set “Battery health mode” to **80%**.
- GNOME: Settings → Power → Battery Health (or `power-profiles-daemon` UI).

**Verify:** `cat /sys/class/power_supply/BAT0/charge_control_end_threshold` returns `80`.

## Wi-Fi Powersave Fix (MT7925e)
Disable NetworkManager’s Wi-Fi powersave to stop intermittent screen flicker and link drops.

```bash
sudo cp configs/system/network/disable-wifi-powersave.conf /etc/NetworkManager/conf.d/
sudo systemctl restart NetworkManager
```

**Verify:** `journalctl -u NetworkManager | grep wifi.powersave` shows `= 2` (disabled).

## Audio & EasyEffects
- Import presets from `configs/audio/easyeffects_presets/`.
- Install `lsp-plugins-lv2`, `calf`, and `rnnoise`.
- Apply RNNoise on mic inputs for live noise reduction.

**Verify:** `pactl list sinks short` shows the 4-speaker sink; EasyEffects reports active presets.

## Video Acceleration (VA-API)
- Arch/CachyOS: `sudo pacman -S libva-mesa-driver`
- Fedora: `sudo dnf install mesa-va-drivers-freeworld`

**Verify:** `vainfo` reports `radeonsi` driver, `mpv --hwdec=vaapi` stays below 12W.

## ZRAM
Arch/CachyOS ships with ZRAM enabled. Confirm (or install `zram-generator` elsewhere):

```bash
zramctl
```

Expect a `zram0` device with compressed swap backing.

## Scheduler Selection

The default scheduler is `scx_lavd --autopower --per-cpu-dsq`, optimized for your Ryzen AI 7 350:

**Performance characteristics:**
- Automatic AC/battery switching (no manual intervention)
- Core compaction saves 25-30% battery power
- Excellent responsiveness for coding and web-browsing
- Thermals reduced even when plugged in

**To temporarily test other schedulers:**
```bash
sudo scx-manager  # GUI tool to switch schedulers
```

**Configuration:** See `configs/system/scheduler/scx_loader.toml`

**Fallback option:** `scx_bpfland` offers lower audio jitter if needed for real-time audio production work.

## NPU (Ryzen AI / XDNA 2)
- Linux 6.14 introduced the `amdxdna` driver; Linux 7.0/7.1 expands telemetry and power controls.
- **FastFlowLM** currently offers the best on-device LLM runtime for the NPU.
- **Ollama** support is tracked upstream; use FastFlowLM or RyzenAI-SW forks if you need it now.

## Scripts & Tools
- **Thai Font Configuration Installer:** `scripts/install_fedora_thai_config.sh`
  - Installs Fedora’s Thai font rules (`99-fedora-thai-rules.conf`) into `~/.config/fontconfig/conf.d/`.
  - Idempotent, distro-agnostic, supports `--dry-run`, `--skip-font-check`, and `--uninstall`.

Example usage:

```bash
bash scripts/install_fedora_thai_config.sh --dry-run
```

## Verification Checklist
| Item | Command |
| --- | --- |
| EasyEffects presets loaded | Open EasyEffects → Import JSON → Enable chain |
| Wi-Fi powersave disabled | `journalctl -u NetworkManager | grep powersave` |
| Battery limit active | `cat /sys/class/power_supply/BAT0/charge_control_end_threshold` |
| VA-API working | `vainfo`, `mpv --hwdec=vaapi` |
| ZRAM enabled | `zramctl` |

For deeper troubleshooting and historical notes, continue to [Hardware_Optimization_Reference.md](Hardware_Optimization_Reference.md).
