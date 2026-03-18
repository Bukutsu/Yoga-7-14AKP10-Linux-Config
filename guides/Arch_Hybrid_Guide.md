# Lenovo Yoga Slim 7 14AKP10 — Arch Hybrid Optimization Guide (v4.0)
**Target Device:** Lenovo Yoga Slim 7 14AKP10 (AMD Ryzen AI 300 Series)  
**Goal:** Turn a fresh Arch install into a hybrid workstation with CachyOS performance plus a Btrfs safety net.  
**Base OS:** Arch Linux (any desktop environment)  
**Kernel:** `linux-cachyos` (stock headers recommended)  
**Version:** v4.0  
**Last Updated:** 2026-03-18

---

## Table of Contents
- [Hardware Compatibility](#hardware-compatibility)
- [Common Hardware Reference](#common-hardware-reference)
- [Phase 1: Adding CachyOS Power (Kernel & Repos)](#phase-1-adding-cachyos-power-kernel--repos)
- [Phase 2: The Automatic Safety Net (Btrfs Snapshots)](#phase-2-the-automatic-safety-net-btrfs-snapshots)
- [Phase 3: System & Power Optimization](#phase-3-system--power-optimization)
- [Phase 4: Hardware-Accelerated Multimedia](#phase-4-hardware-accelerated-multimedia)
- [Phase 5: Final Verification](#phase-5-final-verification)

---

## Hardware Compatibility
See the [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference) for the complete hardware compatibility table.

## Common Hardware Reference
Shared hardware tweaks (EasyEffects, Wi-Fi, etc.) live in [Hardware Optimization Reference](Hardware_Optimization_Reference.md). Use that doc whenever the same config is needed on Fedora or Arch, then return here for the distro-specific steps.

## Phase 1: Adding CachyOS Power (Kernel & Repos)

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

## Phase 2: The Automatic Safety Net (Btrfs Snapshots)

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

## Phase 3: System & Power Optimization

1. **ZRAM** (compressed swap-in-RAM — ships enabled by default on CachyOS, verify):
   ```bash
   zramctl  # Should show a zram0 device. If empty, install zram-generator.
   ```
2. **Battery Longevity:** Set the 80% charge limit in your DE (KDE/GNOME) settings.
3. **Wi-Fi Powersave flicker fix (MT7925e):** The default NetworkManager Wi-Fi powersave setting causes screen flickering on this hardware. Disable it:
   ```bash
   sudo cp configs/system/network/disable-wifi-powersave.conf /etc/NetworkManager/conf.d/
   sudo systemctl restart NetworkManager
   ```
   *This sets `wifi.powersave = 2` (disabled). The network reconnects immediately, no reboot needed.*

**Verify:** `zramctl` lists a `zram0`, and `nmcli general status` shows `connected` without `powersave` errors.

---

## Phase 4: Hardware-Accelerated Multimedia

1. **Video Acceleration:**
   ```bash
   sudo pacman -S libva-mesa-driver
   ```
2. **Audio (4-Speaker + Quad-Mic):** All 4 speakers are native in Kernel 6.18+ via `alc287-yoga9-bass-spk-pin`. Import the EasyEffects presets from `configs/audio/easyeffects_presets/` in this repo.
   * **Noise Cancellation:** Use the **RNNoise** plugin in EasyEffects on the mic input for real-time noise removal.
   * **Verify mic sources are active:**
     ```bash
     pactl list sources | grep -E 'Name:|Description:' | grep alsa_input
     # Should show both Mic1 (Digital) and Mic2 (Stereo) sources
     ```

## Phase 5: Final Verification

Run `fastfetch`. You should see the **Arch Linux Logo** running on the `linux-cachyos` kernel.

For any remaining hardware questions, consult the [Hardware Optimization Reference](Hardware_Optimization_Reference.md) for troubleshooting steps and verification commands.

**Your post-install optimization is complete.**
