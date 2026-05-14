# Contributing

This is a personal configuration repo, but you're welcome to contribute or fork it for your own device.

## For Personal Use (This Repo)

If you're improving configs for this Yoga 7 14AKP10:

1. **Test on the actual device** before committing
2. **Document why** the change matters (comment in the code, note in the commit message)
3. **Update the relevant doc** in `docs/` if you change behavior
4. **Add a CHANGELOG entry** with the date and what changed
5. **Use descriptive commit messages:**
   ```
   fix: audio preset names for clarity
   docs: add Biopass PAM setup guide
   refactor: consolidate WiFi configs
   ```

## For Forking (Your Own Device)

- Replace hardware-specific paths (`configs/system/etc/modprobe.d/rtl8922ae.conf`, audio presets for Dolby/Harman, etc.) with yours
- Copy the docs structure but update device model, specs, and kernel tuning
- Share improvements back if they're general (better scripts, clearer docs, etc.)

## File Organization

```
docs/           — How-to guides, troubleshooting, notes
├── AUDIO_TUNING.md          — Speaker tuning and EasyEffects profiles
├── BIOPASS_PAM_SETUP.md     — Biometric authentication setup
├── DEBRANDING.md            — Removing CachyOS branding
├── INSTALL_GUIDE.md         — Fresh Arch/CachyOS setup
├── LIMINE_THEMING.md        — Bootloader customization
└── TRANSFORM_TO_ARCH.md     — Migration from CachyOS to Arch

configs/        — System configuration files
├── system/etc/  — System-wide configs (copy to /etc/)
└── audio/       — EasyEffects presets, PEQ filters

scripts/        — Automation tools
├── arch-fortify.py          — De-branding and persistence
└── setup-flatpak-fonts.sh   — Font syncing for Flatpak
```

## Before Committing

```bash
# Check git status
git status

# Review your changes
git diff docs/  # or configs/ or scripts/

# If it's a config file, test it on the device first
# If it's a doc, spell-check and verify links

# Commit with a clear message
git commit -m "category: brief description

Longer explanation if needed.
Fixes #123 (if applicable)"
```

## No Force Pushes

- Never rewrite history on `main`
- Each commit should be a logical, testable change
- If you make a mistake, revert with a new commit instead

## Questions?

For device-specific issues, check `docs/` first. If it's a general Linux config question, issues and PRs are welcome.
