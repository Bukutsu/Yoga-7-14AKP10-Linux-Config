# Theming the Limine Bootloader

Limine uses a simple configuration file for theming. You can change the color palette, background image, and branding text.

By default on CachyOS, Limine is themed with **Catppuccin Mocha**. If you want to switch to a different aesthetic like **Tokyo Night Dark**, follow these steps.

## Step 1: Edit the Configuration

Open your Limine configuration file. On UEFI systems with a standard layout, this is usually located at `/boot/limine.conf` or `/boot/efi/limine.conf`.

```bash
sudo nano /boot/limine.conf
```

## Step 2: Apply the Theme

Look for the existing `term_palette` and `term_background` lines. Replace them with your preferred theme.

### Tokyo Night Dark

Paste this at the top of your `limine.conf`:

```conf
# Tokyo Night Dark theme
term_palette: 1a1b26;f7768e;9ece6a;e0af68;7aa2f7;bb9af7;7dcfff;c0caf5
term_palette_bright: 414868;f7768e;9ece6a;e0af68;7aa2f7;bb9af7;7dcfff;c0caf5
term_background: 1a1b26
term_foreground: c0caf5
term_background_bright: 414868
term_foreground_bright: c0caf5
```

### Removing Branding (Optional)

If you want to hide the "Limine" title or the Arch Linux title at the top, add an empty `interface_branding` variable:

```conf
interface_branding:
```

### Changing the Wallpaper (Optional)

You can specify a background image (BMP, PNG, or JPEG). Place your image in the `/boot/` directory and reference it:

```conf
wallpaper: boot():/your-wallpaper.png
wallpaper_style: stretched
```

## Step 3: Deploy the Changes

Once you've saved the file, you need to apply the changes to your EFI partition.

```bash
sudo limine-update
```

Reboot your system to see the new theme in action!

*(Note: These changes are permanent because the `limine.conf` file is user-managed and will not be overwritten by system updates.)*