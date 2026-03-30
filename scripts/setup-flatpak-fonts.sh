#!/bin/bash
# setup-flatpak-fonts.sh: Automate font prioritization for Flatpak apps.
# Usage: ./scripts/setup-flatpak-fonts.sh <lang-code> <font-family>

set -e

LANG_CODE=$1
FONT_FAMILY=$2

if [[ -z "$LANG_CODE" || -z "$FONT_FAMILY" ]]; then
    echo "Usage: $0 <lang-code> <font-family>"
    echo "Example: $0 th \"Noto Sans Thai\""
    exit 1
fi

CONF_DIR="$HOME/.config/fontconfig/conf.d"
CONF_FILE="$CONF_DIR/99-$LANG_CODE-fonts.conf"

echo "--- Setting up $FONT_FAMILY for language: $LANG_CODE ---"

# 1. Create directory
mkdir -p "$CONF_DIR"

# 2. Generate Fontconfig
echo "Generating font configuration at $CONF_FILE..."
cat > "$CONF_FILE" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <!-- Preferred fonts for $LANG_CODE language -->
  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$LANG_CODE</string>
    </test>
    <test name="family">
      <string>sans-serif</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$FONT_FAMILY</string>
    </edit>
  </match>

  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$LANG_CODE</string>
    </test>
    <test name="family">
      <string>serif</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$FONT_FAMILY</string>
    </edit>
  </match>

  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$LANG_CODE</string>
    </test>
    <test name="family">
      <string>monospace</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$FONT_FAMILY</string>
    </edit>
  </match>
</fontconfig>
EOF

# 3. Apply Flatpak Overrides
echo "Applying global Flatpak overrides for fontconfig access..."
flatpak override --user --filesystem=xdg-config/fontconfig:ro --filesystem=~/.local/share/fonts:ro

# 4. Refresh Cache
echo "Refreshing font cache..."
fc-cache -f

echo "--- Done! Restart your Flatpak applications to see the changes. ---"
echo "Verification command: flatpak run --command=fc-match <AppID> :lang=$LANG_CODE"
