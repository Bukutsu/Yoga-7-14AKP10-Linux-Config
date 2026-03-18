# Lenovo Yoga 7 (14AKP10) — Fedora Optimization Guide (v4.0)
**Goal:** Maximum Reliability (5+ Year Target) + Peak Hardware Optimization.  
**Base OS:** Fedora Workstation (official)  
**Kernel:** Fedora stock (stable + periodic updates)  
**Version:** v4.0  
**Last Updated:** 2026-03-18

---

## Table of Contents
- [Hardware Compatibility](#hardware-compatibility)
- [Common Hardware Reference](#common-hardware-reference)
- [Phase 1: The "Invincible" Core (Reliability & Safety)](#phase-1-the-invincible-core-reliability--safety)
- [Phase 2: The "Performance Injection" (Optimization)](#phase-2-the-performance-injection-optimization)
- [Phase 3: Hardware Longevity (Physical Health)](#phase-3-hardware-longevity-physical-health)
- [Phase 4: Development Environment](#phase-4-development-environment)
- [Phase 5: Hardware-Accelerated Multimedia](#phase-5-hardware-accelerated-multimedia)
- [Phase 6: Verify](#phase-6-verify)

---

## Hardware Compatibility
See the [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference) for the complete hardware compatibility table.

## Common Hardware Reference
Shared tweaks (scx scheduler, EasyEffects, Wi-Fi, etc.) are documented in [Hardware Optimization Reference](Hardware_Optimization_Reference.md). Use it anytime both guides need the same config or verification steps.

---

## 🛡️ Phase 1: The "Invincible" Core (Reliability & Safety)
We use Fedora's official vetted kernel but add a safety net to ensure you can always "undo" any change.

1. **Install Snapper & DNF Plugin:**
   ```bash
   sudo dnf install snapper grub-btrfs python3-dnf-plugin-snapper
   ```
2. **Configure Root Snapshots:**
   ```bash
   sudo snapper -c root create-config /
   sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer
   ```
3. **Inject Snapshots into GRUB:**
   ```bash
   sudo grub2-mkconfig -o /boot/grub2/grub.cfg
   sudo systemctl enable --now grub-btrfsd.service
   ```
   *Benefit:* If an update ever glitches, reboot into a previous snapshot from the GRUB menu.

**Verify:** `sudo snapper -c root list` shows recent snapshots, and `systemctl status snapper-timeline.timer snapper-cleanup.timer grub-btrfsd.service` reports `active`.

---

## ⚡ Phase 2: The "Performance Injection" (Optimization)
We gain the "CachyOS feel" without replacing the core system kernel.

1. **Enable Sched-EXT (scx) via COPR:**
   ```bash
   sudo dnf copr enable bieszczaders/kernel-cachyos-addons
   sudo dnf install scx-scheds scx-manager
   ```
2. **Enable the SCX Service:**
   ```bash
   sudo systemctl enable --now scx.service
   ```
3. **The "Bpfland" Setting:** Open `scx-manager` (GUI) and select **`scx_bpfland`**. 
   *Why:* This scheduler prioritizes UI/interactive tasks on your Zen 5 cores, giving you the snappiest possible desktop experience.

**Verify:** `systemctl status scx.service` reports `active`, and `scx-manager` shows `scx_bpfland` as the current scheduler.

---

## 🔋 Phase 3: Hardware Longevity (Physical Health)
To make the laptop physically last 5+ years.

1. **Battery Health (Charge Limit):** 
   * **KDE:** System Settings -> Power Management -> Advanced -> Set Charge Limit to **80%**.
   * **GNOME:** Settings -> Power -> Battery Health.
   *Benefit:* Effectively doubles the lifecycle of your battery by preventing 100% "cooking."

**Verify:** `cat /sys/class/power_supply/BAT0/charge_control_end_threshold` (or KDE/GNOME charge limit UI) reads `80`.

---

## 💻 Phase 4: Development Environment
Keep your host system clean by using containers for development.

1. **Clean Development (Distrobox):** 
   *Instead of installing dev tools on your host, use containers:*
   ```bash
   sudo dnf install distrobox
   distrobox create -n dev-env -i fedora:latest
   ```

**Verify:** `distrobox list` shows the `dev-env` container.

---

## 🎬 Phase 5: Hardware-Accelerated Multimedia
Ensure the 14AKP10 hardware is fully utilized for audio/video.

1. **Enable RPM Fusion & Codecs:**
   ```bash
   sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
   sudo dnf swap ffmpeg-free ffmpeg --allowerasing
   sudo dnf install mesa-va-drivers-freeworld
   ```
2. **Audio Presets:** Import your EasyEffects presets from `configs/audio/easyeffects_presets/` for the 4-speaker Atmos profile.

**Verify:** `rpm -q mesa-va-drivers-freeworld` and `ffmpeg` show the swapped packages, and `pactl list sinks short` reports the four-speaker sink with EasyEffects processing active.

---

## Phase 6: Verify
Run `fastfetch`. You have the **Official Fedora Logo** and **Stock Kernel**, but your system is powered by **`scx_bpfland`**, has a **Btrfs Safety Net**, and is physically protected for a long life.

**Your Yoga 7 is now a high-integrity professional workstation.**
