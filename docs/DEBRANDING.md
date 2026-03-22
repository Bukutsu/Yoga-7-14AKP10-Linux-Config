# De-branding CachyOS Visuals

If you are transitioning your system back to an Arch Linux identity, you might want to remove CachyOS-specific visual elements from your boot sequence and login screen.

## 1. Remove CachyOS Logo from GDM (Login Screen)

CachyOS overrides the default GDM logo. There are two ways to remove it:

### Option A: Remove the override (Keep CachyOS Settings)
This removes the logo but keeps other `cachyos-settings` (like sysctl tweaks) intact. We do both a file deletion and a dconf override to ensure it's future-proof.

```bash
# 1. Delete the schema override file
sudo rm -f /usr/share/glib-2.0/schemas/zz_cachyos.org.gnome.login-screen.gschema.override

# 2. Recompile schemas
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

# 3. Set the dconf key (Permanent user-level override)
sudo -u gdm dbus-launch gsettings set org.gnome.login-screen logo ''

# 4. Restart GDM to apply changes (Note: This will log you out!)
sudo systemctl restart gdm
```

### Option B: Full Removal (Zero-Maintenance)
If you no longer want any CachyOS settings, simply remove the package entirely. This guarantees the logo will never return on updates.

```bash
sudo pacman -Rs cachyos-settings
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
```

---

## 2. Restore Arch Linux Boot Splash (Plymouth)

CachyOS uses its own boot animation. You can easily switch back to the default Arch Linux vendor logo (bgrt) or spinner. This change is managed in `/etc/plymouth/plymouthd.conf` and is 100% permanent across updates.

```bash
# 1. Switch to the default Arch 'bgrt' theme
sudo plymouth-set-default-theme -R bgrt

# 2. Rebuild the initramfs to embed the new theme
sudo mkinitcpio -P

# 3. (If using Limine) Update the bootloader
sudo limine-update
```
