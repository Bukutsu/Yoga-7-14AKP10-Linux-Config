# Hardware Optimization Reference

**Hardware Compatibility Table**

| Component | Status | Notes |
| --- | --- | --- |
| Radeon 840M/860M GPU | ✅ Works | VA-API acceleration via `libva-mesa-driver` (Arch) or `mesa-va-drivers-freeworld` (Fedora) |
| OLED Touchscreen | ✅ Works OOB | `libinput list-devices` shows touchscreen and stylus |
| Stylus (Yoga Pen) | ✅ Works OOB | Pressure + tilt via evdev/libinput |
| Auto-rotate (tablet mode) | ✅ Works | Requires `iio-sensor-proxy` for GNOME rotation |
| Wi-Fi 7 (MT7925e) | ✅ Works | Disable Wi-Fi powersave to stop flickering |
| Bluetooth 5.4 | ✅ Works OOB | Same MT7925e chip |
| IR camera / Howdy | ✅ Works | Refer to the [Arch Wiki for Howdy](https://wiki.archlinux.org/title/Howdy) for setup |
| 4 speakers + Dolby Atmos | ✅ Works | Kernel 6.18+ exposes all speaker pins |
| Quad-mic array | ✅ Works | EasyEffects profiles + RNNoise chain |
| MicroSD reader | ✅ Works OOB | Standard SDHCI support |
| USB-C DisplayPort 2.1 | ✅ Works | Handled by Mesa + kernel drivers |
| Fingerprint reader | ➖ N/A | Not present on all hardware SKUs |

---

Shared hardware optimizations live here so both the Arch and Fedora guides can stay focused on distro-specific work. The steps below are distro-agnostic and apply whenever the Lenovo Yoga 7 14AKP10 (14AKP10 / 83JR) hardware is in use.

## System Performance
- **ZRAM:** Arch (CachyOS) ships with zram enabled; on other distros install `zram-generator` if `zramctl` shows no devices.

## Audio & EasyEffects
- **Presets:** The repository stores `configs/audio/easyeffects_presets/*.json` and is linked from both guides. Import the desired JSON in EasyEffects.  
- **RNNoise chain:** Use the `RNNoise` plugin on the mic input for real-time noise reduction.  
- **EQ:** `lsp-plugins-lv2` and `calf` provide the required filters.

## Wi-Fi Power Save (MT7925e)
- Use the canonical config `configs/system/network/disable-wifi-powersave.conf` and copy it to `/etc/NetworkManager/conf.d/`.  
  ```bash
  sudo cp configs/system/network/disable-wifi-powersave.conf /etc/NetworkManager/conf.d/
  sudo systemctl restart NetworkManager
  ```
  **Verify:** `nmcli general logging level` or check `journalctl -u NetworkManager` for `wifi.powersave = 2`.

## Troubleshooting
- **scx_loader/scx.service fails to start:** Run `journalctl -u scx_loader.service -u scx.service`. Confirm `scx-scheds`, `scx-manager`, and `cachyos-settings` are installed and match the kernel version.  
- **Wi-Fi still flickers:** `nmcli general logging level 3` plus `journalctl -u NetworkManager` will show if `wifi.powersave` reverted. Reapply `/etc/NetworkManager/conf.d/disable-wifi-powersave.conf` and restart the service.  
- **EasyEffects presets won't load:** Verify the JSON resides in `configs/audio/easyeffects_presets/`. Install `lsp-plugins-lv2`, `calf`, and `rnnoise` packages, then restart EasyEffects.

## Verification Checklist
| Task | Command |
| --- | --- |
| EasyEffects presets | Open EasyEffects, import JSON from `configs/audio/easyeffects_presets/` |
| Wi-Fi power save | `journalctl -u NetworkManager \| grep powersave` |
