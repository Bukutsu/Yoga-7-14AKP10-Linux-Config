#!/bin/bash
# setup-flatpak-fonts.sh: Automate font prioritization for Flatpak apps.
# Usage: ./scripts/setup-flatpak-fonts.sh <lang-code> <font-family>
#        ./scripts/setup-flatpak-fonts.sh uninstall <lang-code>

set -e

# --- Functions ---

check_dependencies() {
    for cmd in git flatpak fc-cache; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: Required command '$cmd' is not installed. Please install it and try again."
            exit 1
        fi
    done
}

show_usage() {
    echo "Usage: $0 <lang-code> <font-family>        (Install/Update)"
    echo "       $0 uninstall <lang-code>           (Remove)"
    echo ""
    echo "Example: $0 th \"Noto Sans Thai\""
    echo "         $0 uninstall th"
    exit 1
}

# --- Initialization ---

check_dependencies

# Get repo root reliably
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || dirname "$(dirname "$(readlink -f "$0")")")

MODE="install"
if [[ "$1" == "uninstall" ]]; then
    MODE="uninstall"
    shift
fi

LANG_CODE=$1
FONT_FAMILY=$2

if [[ -z "$LANG_CODE" ]]; then
    show_usage
fi

if [[ "$MODE" == "install" && -z "$FONT_FAMILY" ]]; then
    show_usage
fi

CONF_DIR="$HOME/.config/fontconfig/conf.d"
CONF_FILE="$CONF_DIR/99-$LANG_CODE-fonts.conf"

# --- Logic ---

if [[ "$MODE" == "uninstall" ]]; then
    if [[ -f "$CONF_FILE" ]]; then
        echo "Removing font configuration for $LANG_CODE at $CONF_FILE..."
        rm -i "$CONF_FILE"
        echo "Refreshing font cache..."
        fc-cache -f
        echo "Successfully uninstalled font config for $LANG_CODE."
    else
        echo "No configuration found for language: $LANG_CODE at $CONF_FILE"
    fi
    exit 0
fi

echo "--- Setting up $FONT_FAMILY for language: $LANG_CODE ---"

# 1. Create directory
mkdir -p "$CONF_DIR"

# 2. Prevent accidental overwrites
if [[ -f "$CONF_FILE" ]]; then
    read -p "Warning: Config file already exists at $CONF_FILE. Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborting."
        exit 0
    fi
fi

# 3. Sync Configuration from Repository or Generate New
REPO_CONF_FILE="$REPO_ROOT/.config/fontconfig/conf.d/99-$LANG_CODE-fonts.conf"

if [[ -f "$REPO_CONF_FILE" ]]; then
    echo "Found existing config in repository: $REPO_CONF_FILE"
    echo "Copying to $CONF_FILE..."
    cp "$REPO_CONF_FILE" "$CONF_FILE"
else
    echo "No config found in repository for $LANG_CODE. Generating a new one at $CONF_FILE..."
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
fi

# 4. Apply Flatpak Overrides
echo "Applying global Flatpak overrides for fontconfig access..."
flatpak override --user --filesystem=xdg-config/fontconfig:ro --filesystem=~/.local/share/fonts:ro

# 5. Refresh Cache
echo "Refreshing font cache..."
fc-cache -f

echo "--- Done! Restart your Flatpak applications to see the changes. ---"
echo "Verification command: flatpak run --command=fc-match <AppID> :lang=$LANG_CODE"
