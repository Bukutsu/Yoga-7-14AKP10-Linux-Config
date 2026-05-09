# De-branding CachyOS

## 1. Arch Identity (Forever Persistent)
Masks branding hooks to keep package updates while staying "Arch Linux" forever.

```bash
# 1. Mask branding hooks (Prevents overwrites)
sudo mkdir -p /etc/libalpm/hooks/
for hook in os-release.hook lsb-release.hook; do
  sudo ln -sf /dev/null "/etc/libalpm/hooks/$hook"
done

# 2. Restore identity files
sudo pacman -S filesystem lsb-release
sudo ln -sf /usr/lib/os-release /etc/os-release
sudo ln -sf /usr/lib/lsb-release /etc/lsb-release

# 3. Update boot menu
sudo limine-mkinitcpio && sudo limine-update
```

## 2. GDM Logo (Login Screen)
Choose based on your preference for CachyOS performance tweaks.

**Option A: Purge (100% Pure Arch)**
```bash
sudo pacman -Rs cachyos-settings
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
```

**Option B: Mask (Keep performance tweaks, remove logo)**
```bash
# Create schema override that wins over CachyOS (zzzz > zz_c)
printf '[org.gnome.login-screen]\nlogo='\'''\''\n' | sudo tee /usr/share/glib-2.0/schemas/zzzz_arch-fix.gschema.override
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
```

## 3. Limine Visuals
Clean up the bootloader theme and remove stale CachyOS entries.

```bash
# Remove CachyOS theme block
sudo sed -i '/# CachyOS Limine theme/,/wallpaper:/d' /boot/limine.conf
sudo sed -i '/interface_branding:/d' /boot/limine.conf
sudo sed -i '/term_palette/d; /term_background/d; /term_foreground/d' /boot/limine.conf
```

Then open `/boot/limine.conf` and manually remove the `/+CachyOS` entry block and set `default_entry` to the Arch Linux entry number.

```bash
sudo limine-update
```

## 4. Plymouth (Boot Splash)
```bash
sudo plymouth-set-default-theme bgrt
sudo mkinitcpio -P
sudo limine-update
```
