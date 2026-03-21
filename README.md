# System Config

Personal Linux configuration files for the **Lenovo Yoga 7 2-in-1 14AKP10** (AMD Ryzen AI 7 350).

> Treat as reference material, not gospel.

---

## Hardware

- **Laptop**: Lenovo Yoga 7 2-in-1 14AKP10 (83JR)
- **CPU**: AMD Ryzen AI 7 350 w/ Radeon 860M (Strix Point, Zen 5)
- **RAM**: 32GB
- **Storage**: 1TB NVMe SSD
- **WiFi**: Realtek RTL8922AE (WiFi 7)
- **OS**: Arch Linux (CachyOS kernel)

---

## What's Inside

### `configs/system/scheduler/scx_loader.toml`
sched-ext (`scx_lavd`) scheduler profiles tuned for AMD Strix Point.

Core mapping (ACPI-verified):
```
P-Tier1: cores 4, 6  (ACPI perf 208, fastest)
P-Tier2: core  0      (ACPI perf 202)
P-Tier3: core  2      (ACPI perf 196)
E-Cores: cores 1,3,5,7 (ACPI perf 135, ~2.0GHz max)
```
Shared 16MB L3. Single die.

Powersave mode routes tasks to **E-cores first** under light load, with `lb-low-util-pct=70` to skip periodic load balancing.

### `configs/system/network/disable-wifi-powersave.conf`
Disables WiFi runtime power management for stability on the RTL8922AE.

### `configs/audio/easyeffects_presets/`
Noise reduction and EQ presets for various microphones.

---

## Key Findings

### SCX LAVD Powersave Mode

The powersave profile routes tasks to **E-cores first**. Strix Point E-cores max at ~2GHz and draw significantly less power than P-cores. With `lb-low-util-pct=70`, periodic load balancing is suppressed until 70% system utilization -- eliminating unnecessary cross-core migrations for typical desktop workloads.

### Don't Use TLP on AMD

Use `power-profiles-daemon` instead. TLP interferes with AMD's ACPI platform profile integration.

### Kernel Parameters for Battery Optimization

Add these to your bootloader kernel command line (e.g., `/etc/default/limine`):

```
amd_pstate=active pcie_aspm=force
```

**Measured idle power draw on Yoga 7 14AKP10:**
- With optimization: **3–4W**
- Stock (Windows): ~5.0W

**Verify on your system:**

```bash
sudo turbostat --quiet --show PkgWatt -n 1
```

(Requires `turbostat`. Let the system idle for ~30 seconds before reading.)

---

## Quick Setup

1. Copy configs to their destinations
2. Restart the relevant services
3. Reboot

---

## Sources

- [CachyOS Wiki - sched-ext](https://wiki.cachyos.org/configuration/sched-ext/)
- [sched-ext/scx GitHub](https://github.com/sched-ext/scx)
- [archlinux.org - CPU Frequency Scaling](https://wiki.archlinux.org/title/CPU_Frequency_Scaling)
