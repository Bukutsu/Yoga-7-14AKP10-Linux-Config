# Lenovo Yoga 7 2-in-1 (14AKP10) System Configuration

**Target Hardware:** Lenovo Yoga 7 2-in-1 14AKP10 (AMD Ryzen AI 7 350)  
**Primary OS:** CachyOS (Arch-based)  
**Last Updated:** 2026-03-18

This repository contains configuration files, guides, and scripts for optimizing the Lenovo Yoga 7 2-in-1 14AKP10 on Linux.

## Core Philosophy & Goals

Every configuration and guide in this repository is built around three primary engineering objectives:

1. **"Updates Forever" (Longevity & Maintainability):** Building a resilient architecture (utilizing Btrfs snapshots and containerized development) to ride rolling or bleeding-edge updates without the fear of system breakage, eliminating the need to ever reinstall the OS.
2. **"Make the Most of My Hardware" (Performance):** Utilizing advanced, compiler-optimized environments (CachyOS) and cutting-edge eBPF kernel schedulers (`scx_bpfland`) to extract maximum efficiency, battery life, and UI responsiveness from the AMD Zen 5 architecture.
3. **"Support Every Part of My Hardware" (Completeness):** Ensuring 100% of the silicon is active—from the 4-speaker Atmos array and IR facial recognition to tracking upstream driver support for the XDNA 2 NPU.

## Quick Start

1. **Choose Your Distribution:**
   - Already running CachyOS? Use this README for quick optimizations
   - Fresh Arch install? See [Arch Hybrid Guide](Arch_Hybrid_Guide.md)
   - Prefer Fedora stability? See [Fedora Optimized Guide](Fedora_Optimized_Guide.md)

2. **Check Hardware Compatibility:** [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference)

3. **Apply Key Optimizations** (see sections below)

---

## Table of Contents

- [Core Philosophy](#core-philosophy--goals)
- [Quick Start](#quick-start)
- [Results](#results)
- [Key Optimizations](#key-optimizations)
- [Related Guides](#related-guides)

---

## Results

- **Idle Power:** Reduced to ~6.8W - 7.2W (previously ~7.4W)
- **Active Light Power:** ~8W (yielding ~9 hours of real-world use on the 70Wh battery)
- **Video:** 10-12W draw during YouTube playback with hardware acceleration confirmed via `vainfo` / `mpv`
- **Audio:** Native 4-speaker support (Kernel 6.18+) + Atmos-style 3D effects via PipeWire/EasyEffects
- **Screen:** Fixed flickering

---

## Key Optimizations

### Battery & Power
- **Battery Longevity:** Use the native **Battery Health / Conservation Mode** in your Desktop Environment (KDE Plasma 6.1+ or GNOME) to limit charge to 80%
- **Results:** ~6.8W - 7.2W idle power, ~8W active light use (9 hours battery life on 70Wh)

### CPU Scheduler
For productive coding and web-browsing, use the eBPF **`scx_bpfland`** scheduler through `scx_loader`.

- **Why `bpfland`?** Unlike `lavd` (gaming-centric), `bpfland` uses a vruntime-based algorithm that excels at prioritizing interactive desktop tasks while aggressively idling background processes
- **Auto-Power Logic:** The config (`configs/system/scheduler/scx_loader.toml`) uses `["-m", "auto", "-f"]` flags to communicate with `power-profiles-daemon`. On battery, it automatically throttles background tasks and uses efficient cores
- **Frequency Control:** The `-f` flag enables direct CPU frequency management with `amd_pstate=active` driver

### Audio
Starting with **Kernel 6.18+**, all 4 speakers work natively via the `alc287-yoga9-bass-spk-pin` quirk.

- **EasyEffects:** Use for spatial depth and Dolby Atmos-style effects
- **Presets:** Located in `configs/audio/easyeffects_presets/`
- **Requirements:** `lsp-plugins-lv2` and `calf` for EQ effects

---

## Related Guides

- [Arch Hybrid Guide](Arch_Hybrid_Guide.md): Arch base with CachyOS kernel + safety net
- [Fedora Optimized Guide](Fedora_Optimized_Guide.md): Fedora stock kernel + "performance injection"

## Shared Hardware Reference

- [Hardware Optimization Reference](Hardware_Optimization_Reference.md) consolidates distro-agnostic steps for hardware compatibility, EasyEffects, Wi-Fi configuration, and troubleshooting

---

Configuration tailored for CachyOS/Fedora using Gemini CLI.
