# Lenovo Yoga 7 (14AKP10) — Fedora Optimization Guide (v4.1)
**Goal:** Maximum reliability (5+ years) with injected performance tuning.  
**Base OS:** Fedora Workstation (official)  
**Kernel:** Fedora stock (periodic updates)  
**Version:** v4.1  
**Last Updated:** 2026-03-19

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

> 🔁 **Shared steps:** Battery limits, Wi-Fi powersave, audio presets, VA-API, and scripts live in [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md).

## Table of Contents
- [Hardware Compatibility](#hardware-compatibility)
- [Phase 1: Invincible Core (Reliability & Safety)](#%F0%9F%9B%A1%EF%B8%8F-phase-1-invincible-core-reliability--safety)
- [Phase 2: Performance Injection (Sched-EXT)](#%E2%9A%A1-phase-2-performance-injection-sched-ext)
- [Phase 3: Multimedia & Shared Optimizations](#%F0%9F%8E%AC-phase-3-multimedia--shared-optimizations)
- [Phase 4: Development Environment](#%F0%9F%92%BB-phase-4-development-environment)
- [Phase 5: Verify](#phase-5-verify)

## Hardware Compatibility
See [Hardware Optimization Reference](Hardware_Optimization_Reference.md#hardware-optimization-reference) for the full hardware table.

---

## 🛡️ Phase 1: Invincible Core (Reliability & Safety)
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

## ⚡ Phase 2: Performance Injection (Sched-EXT)
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

## 🎬 Phase 3: Multimedia & Shared Optimizations
Reference [SHARED_OPTIMIZATIONS.md](SHARED_OPTIMIZATIONS.md) for:
- Battery health limit (80%)
- Wi-Fi powersave fix (MT7925e)
- EasyEffects presets + RNNoise
- VA-API packages (`mesa-va-drivers-freeworld`)
- Thai font installer script usage

**Verify:** `journalctl -u NetworkManager | grep wifi.powersave`, EasyEffects active chains, `vainfo` with `radeonsi`.

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

## Phase 5: Verify
Run `fastfetch`. You have the **Official Fedora Logo** and **Stock Kernel**, but your system is powered by **`scx_bpfland`**, has a **Btrfs Safety Net**, and is physically protected for a long life.

**Your Yoga 7 is now a high-integrity professional workstation.**
