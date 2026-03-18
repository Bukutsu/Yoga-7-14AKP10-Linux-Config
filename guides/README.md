# Lenovo Yoga 7 2-in-1 (14AKP10) System Configuration

**Target Hardware:** Lenovo Yoga 7 2-in-1 14AKP10 (AMD Ryzen AI 7 350)  
**Primary OS:** CachyOS (Arch-based)  
**Last Updated:** 2026-03-18

This repository contains configuration files, guides, and scripts for optimizing the Lenovo Yoga 7 2-in-1 14AKP10 on Linux.

## Quick Start

1. **Choose Your Distribution:**
   - Already running CachyOS? Use this README for quick optimizations
   - Fresh Arch install? See [Arch Hybrid Guide](Arch_Hybrid_Guide.md)
   - Prefer Fedora stability? See [Fedora Optimized Guide](Fedora_Optimized_Guide.md)

2. **Check Hardware Compatibility:** [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference)

3. **Apply Key Optimizations** (see sections below)

---

## Table of Contents

- [Results](#results)
- [1. Power and Kernel](#1-power-and-kernel)
- [2. CPU Scheduler](#2-cpu-scheduler-work--efficiency)
- [3. Audio Setup](#3-audio-setup)
- [Related Guides](#related-guides)

---

## Results

- **Idle Power:** Reduced to ~6.8W - 7.2W (previously ~7.4W)
- **Active Light Power:** ~8W (yielding ~9 hours of real-world use on the 70Wh battery)
- **Video:** 10-12W draw during YouTube playback with hardware acceleration confirmed via `vainfo` / `mpv`
- **Audio:** Native 4-speaker support (Kernel 6.18+) + Atmos-style 3D effects via PipeWire/EasyEffects
- **Screen:** Fixed flickering

---

## 1. Power and Kernel

- **Battery Longevity:** Use the native **Battery Health / Conservation Mode** support in the Desktop Environment (KDE Plasma 6.1+ or GNOME) to limit the charge to 80%

---

## 2. CPU Scheduler (Work & Efficiency)

For a productive coding and web-browsing workflow, use the eBPF **`scx_bpfland`** scheduler through `scx_loader`.

- **Why `bpfland`?** Unlike `lavd` (which is gaming-centric), `bpfland` uses a vruntime-based algorithm that excels at prioritizing interactive desktop tasks while aggressively idling background processes
- **Auto-Power Logic:** The config (`configs/system/scheduler/scx_loader.toml`) uses the `["-m", "auto", "-f"]` flags. This allows the scheduler to natively communicate with `power-profiles-daemon`. When on battery, it automatically throttles background tasks and utilizes the most efficient cores, keeping the CPU in deep C-states longer
- **Frequency Control:** The `-f` flag enables the scheduler to manage CPU frequencies directly, working in tandem with the `amd_pstate=active` driver for maximum efficiency 

---

## 3. Audio Setup

Previously, Linux only used the top two speakers by default. Starting with **Kernel 6.18+**, the subwoofers (bass speakers) are now natively supported via the `alc287-yoga9-bass-spk-pin` quirk. This quirk is automatically applied by the kernel, making all 4 speakers work as a single hardware sink out of the box.

- **EasyEffects:** Since the hardware is now fully active, use EasyEffects primarily for spatial depth and physical correction using a Dolby Atmos Impulse Response (IR) file
- **Presets:** Presets are located in `configs/audio/easyeffects_presets/`
- **Requirements:** You still need `lsp-plugins-lv2` and `calf` installed for the EQ effects

---

## Related Guides

- [Arch Hybrid Guide](Arch_Hybrid_Guide.md): Arch base with CachyOS kernel + safety net
- [Fedora Optimized Guide](Fedora_Optimized_Guide.md): Fedora stock kernel + "performance injection"

## Shared Hardware Reference

- [Hardware Optimization Reference](Hardware_Optimization_Reference.md) consolidates the distro-agnostic steps for EasyEffects, Wi-Fi, and hardware compatibility so both guides can stay focused on their unique flows

Configuration tailored for CachyOS/Fedora using Gemini CLI.
