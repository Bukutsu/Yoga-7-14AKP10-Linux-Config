# Lenovo Yoga Slim 7 14AKP10 — Arch Hybrid Guide (v4.1)
**Target Device:** Lenovo Yoga Slim 7 14AKP10 (AMD Ryzen AI 300 Series)  
**Goal:** Turn a fresh Arch install into a CachyOS-powered workstation with a Btrfs safety net.  
**Base OS:** Arch Linux (any desktop environment)  
**Kernel:** `linux-cachyos` (with headers)  
**Version:** v4.1  
**Last Updated:** 2026-03-19

---

## Table of Contents
- [Hardware Compatibility](#hardware-compatibility)
- [Common Hardware Reference](#common-hardware-reference)
- [Phase 1: Add CachyOS Power (Kernel & Repos)](#phase-1-add-cachyos-power-kernel--repos)
- [Phase 2: Automatic Safety Net (Btrfs Snapshots)](#phase-2-automatic-safety-net-btrfs-snapshots)
- [Phase 3: Scheduler + Multimedia](#phase-3-scheduler--multimedia)
- [Phase 4: Shared Optimizations](#phase-4-shared-optimizations)
- [Phase 5: Final Verification](#phase-5-final-verification)

---

## Hardware Compatibility
See [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference) for the complete hardware compatibility table.

## Common Hardware Reference
Hardware-agnostic tweaks live in [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md). For deeper context and troubleshooting, consult [Hardware_Optimization_Reference.md](Hardware_Optimization_Reference.md).

> 🔁 **Shared steps:** Battery limits, Wi-Fi powersave, audio presets, VA-API, and scripts live in [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md).

## Phase 1: Add CachyOS Power (Kernel & Repos)

Assuming you have a fresh Arch Linux installation (base + desktop environment), we will now inject the CachyOS optimizations.

1. **Enable the CachyOS Repositories:**
   ```bash
   wget https://mirror.cachyos.org/cachyos-repo.tar.xz
   tar xvf cachyos-repo.tar.xz
   cd cachyos-repo
   sudo ./cachyos-repo.sh
   ```
2. **Install the CachyOS Kernel & Sched-EXT Tools:**
   ```bash
   sudo pacman -Syu linux-cachyos linux-cachyos-headers scx-scheds cachyos-settings scx-manager
   ```
3. **Enable the Optimization Services:**
   ```bash
   sudo systemctl enable --now scx_loader.service cachyos-settings.service
   ```
4. **Configure via scx-manager (GUI):**
   Open `scx-manager` and set:
   * **Scheduler:** `scx_bpfland`
   * **Profile:** `Auto`
   * **Extra flags:** *(leave empty — Auto mode already includes `-m auto -f`)*

> `Auto` mode integrates with `power-profiles-daemon` (battery → powersave slice, AC → performance) and uses `-f` to hand frequency hints directly to `amd_pstate=active`. This gives the best efficiency for coding/browsing/light gaming without manual switching.

**Verify:** `uname -r` should show a `linux-cachyos` kernel, and `systemctl status scx_loader.service cachyos-settings.service` should report active services. `scx-manager` should list `scx_bpfland` as the active scheduler.

---

## Phase 2: Automatic Safety Net (Btrfs Snapshots)

This setup provides "easy" snapshots that appear directly in your bootloader (Limine, GRUB, or systemd-boot).

1. **Install the Snapshot Synchronization Tools:**
   ```bash
   sudo pacman -S snapper snap-pac inotify-tools
   # If using Limine:
   sudo pacman -S limine-snapper-sync
   # If using GRUB:
   sudo pacman -S grub-btrfs
   ```
2. **Configure Snapper for Root:**
   ```bash
   sudo snapper -c root create-config /
   ```
3. **The Snapshot Fix (Standard Btrfs Layout):**
   ```bash
   sudo btrfs subvolume delete /.snapshots
   sudo mkdir /.snapshots
   sudo mount -a
   ```
4. **Enable Auto-Sync & Maintenance:**
   ```bash
   sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer
   # If using Limine (Syncs snapshots to boot menu):
   sudo systemctl enable --now limine-snapper-sync.timer
   ```

**Verify:** `sudo snapper -c root list` shows timeline/cleanup snapshots and `systemctl status snapper-timeline.timer snapper-cleanup.timer` reports `active`. If using Limine, check `systemctl status limine-snapper-sync.timer`.

---

## Phase 3: Scheduler + Multimedia
1. `scx_manager` GUI → Scheduler `scx_bpfland`, Profile `Auto`.
2. Ensure EasyEffects presets and VA-API per [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md).

**Verify:** `systemctl status scx_loader.service cachyos-settings.service` shows `active`; `vainfo` lists `radeonsi`; EasyEffects chains are engaged.

## Phase 4: Shared Optimizations
Follow [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md) for:
- Battery health limit (80%)
- Wi-Fi powersave disable (`wifi.powersave = 2`)
- ZRAM verification
- Audio presets, RNNoise chain, Thai font installer

## Phase 5: Final Verification

Run `fastfetch`. You should see the **Arch Linux Logo** running on the `linux-cachyos` kernel.

Need additional troubleshooting? Check [Hardware_Optimization_Reference.md](Hardware_Optimization_Reference.md).

**Your Arch → Cachy hybrid is ready.**
