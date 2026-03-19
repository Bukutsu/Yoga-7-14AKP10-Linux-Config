# CachyOS Quick Start — Lenovo Yoga 7 / Slim 7 (14AKP10)

**Target Hardware:** Lenovo Yoga 7 2-in-1 / Slim 7 14AKP10 (AMD Ryzen AI 7 350)  
**Primary OS:** CachyOS (Arch-based)  
**Last Updated:** 2026-03-18

Use this page if you already run CachyOS and just need the high-impact optimizations. If you're installing Arch from scratch or sticking with Fedora, jump to the dedicated guides listed below.

## Core Philosophy & Goals

Every configuration and guide in this repository is built around three primary engineering objectives:

1. **"Updates Forever" (Longevity & Maintainability):** Building a resilient architecture (utilizing Btrfs snapshots and containerized development) to ride rolling or bleeding-edge updates without the fear of system breakage, eliminating the need to ever reinstall the OS.
2. **"Make the Most of My Hardware" (Performance):** Utilizing advanced, compiler-optimized environments (CachyOS) and cutting-edge eBPF kernel schedulers (`scx_bpfland`) to extract maximum efficiency, battery life, and UI responsiveness from the AMD Zen 5 architecture.
3. **"Support Every Part of My Hardware" (Completeness):** Ensuring 100% of the silicon is active—from the 4-speaker Atmos array and IR facial recognition to tracking upstream driver support for the XDNA 2 NPU.

## Quick Start

1. **Choose Your Distribution:**
   - Already on CachyOS? Stay here.
   - Fresh Arch install? Go to [Arch Hybrid Guide](Arch_Hybrid_Guide.md)
   - Prefer Fedora stability? Use [Fedora Optimized Guide](Fedora_Optimized_Guide.md)

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

## Core Optimizations

### Battery & Power
- **Battery Longevity:** Use the native battery health mode in KDE Plasma 6.1+ or GNOME to hold 80% charge.

### CPU Scheduler
For productive coding and web-browsing, use the eBPF **`scx_bpfland`** scheduler through `scx_loader`.

- **Why `bpfland`?** Unlike `lavd` (gaming-centric), `bpfland` uses a vruntime-based algorithm that excels at prioritizing interactive desktop tasks while aggressively idling background processes
- **Auto-Power Logic:** The config (`configs/system/scheduler/scx_loader.toml`) uses `["-m", "auto", "-f"]` flags to communicate with `power-profiles-daemon`. On battery, it automatically throttles background tasks and uses efficient cores
- **Frequency Control:** The `-f` flag enables direct CPU frequency management with `amd_pstate=active` driver

### Audio
With Kernel 6.18+, all 4 speakers work via the `alc287-yoga9-bass-spk-pin` quirk.

- Import EasyEffects presets from `configs/audio/easyeffects_presets/` (ensure `lsp-plugins-lv2`, `calf`, `rnnoise`).
- Use the RNNoise plugin on the mic input for live noise reduction.

---

## Related Guides

- [Arch Hybrid Guide](Arch_Hybrid_Guide.md): Arch base with CachyOS kernel + safety net
- [Fedora Optimized Guide](Fedora_Optimized_Guide.md): Fedora stock kernel + "performance injection"

## Shared Hardware Reference

- See [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md) for hardware-agnostic steps (battery limits, Wi-Fi powersave, audio presets, scripts).
- For deep dives (hardware tables, troubleshooting), open [Hardware Optimization Reference](Hardware_Optimization_Reference.md).

---

Configuration tailored for CachyOS/Fedora using Gemini CLI.
