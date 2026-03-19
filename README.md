# 🛠️ bukutsu's System Config
A single repo to optimize the Lenovo Yoga 7 / Slim 7 (14AKP10) on modern AMD hardware. Primary audience: CachyOS users who want maximum performance without giving up reliability.

## Start Here
- ✅ **Already on CachyOS?** Open `guides/CACHYOS_QUICK_START.md` for immediate tuning steps.
- 🆕 **Fresh Arch install?** Follow `guides/Arch_Hybrid_Guide.md` to layer CachyOS power on top of vanilla Arch.
- 🔵 **Prefer Fedora stability?** Use `guides/Fedora_Optimized_Guide.md` to keep stock Fedora while injecting performance tweaks.

## Repo Layout
- `guides/` – OS-specific guides plus shared hardware references.
- `configs/` – Ready-to-use configs (EasyEffects presets, scheduler settings, fontconfig snippets, etc.).
- `scripts/` – Standalone tools (e.g., Thai font installer) that complement the guides.

## Philosophy: Solid Core, Liquid Edge
- **Solid Core:** Start with an official, stable OS (Fedora Workstation or CachyOS kernel builds) and add a reversible safety net (Btrfs snapshots, containerized dev envs).
- **Liquid Edge:** Inject performance and hardware-specific optimizations (Sched-EXT `scx_bpfland`, power profiles, EasyEffects) in a non-destructive way.

You get a workstation that stays reliable for years, yet feels tuned for the Ryzen AI platform.

Maintained using Gemini CLI.
