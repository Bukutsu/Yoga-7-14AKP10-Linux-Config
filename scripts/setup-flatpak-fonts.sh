#!/bin/bash
# setup-flatpak-fonts.sh: Automate font prioritization for Flatpak apps.
# Usage: ./scripts/setup-flatpak-fonts.sh                    (Interactive Mode)
#        ./scripts/setup-flatpak-fonts.sh <lang-code> <font-family> (Quick Mode)
#        ./scripts/setup-flatpak-fonts.sh uninstall <lang-code>    (Remove)

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
    echo "Usage: $0                                 (Interactive Mode)"
    echo "       $0 <lang-code> <font-family>        (Quick Mode)"
    echo "       $0 uninstall <lang-code>           (Remove)"
    echo ""
    echo "Example: $0 th \"Noto Sans Thai\""
    echo "         $0 uninstall th"
}

get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null || dirname "$(dirname "$(readlink -f "$0")")"
}

run_interactive() {
    echo "--- Flatpak Font Setup Wizard ---"
    
    # 1. Select Language
    echo "Searching for available languages..."
    # Use fc-list to get a list of common language codes
    local langs
    langs=$(fc-list : lang | cut -d= -f2 | cut -d: -f1 | tr ',' '\n' | sort -u | grep -E '^[a-z]{2}(-[a-z]{2})?$' | head -n 30)
    
    echo "Common language codes found on your system:"
    select lang in $langs "Other"; do
        if [[ "$lang" == "Other" ]]; then
            read -p "Enter language code (e.g., ja, ko, zh-cn): " LANG_CODE
            break
        elif [[ -n "$lang" ]]; then
            LANG_CODE=$lang
            break
        fi
    done

    # 2. Select Font
    echo "Searching for fonts supporting '$LANG_CODE'..."
    local fonts
    # Get unique font family names for the selected language
    fonts=$(fc-list ":lang=$LANG_CODE" family | cut -d, -f1 | sort -u | head -n 20)
    
    if [[ -z "$fonts" ]]; then
        echo "No specific fonts found for language '$LANG_CODE'. Showing all fonts..."
        fonts=$(fc-list : family | cut -d, -f1 | sort -u | head -n 20)
    fi

    echo "Select a font family to prioritize:"
    # Use a while loop with an array for better select handling of spaces
    IFS=$'\n' read -r -d '' -a font_array <<< "$fonts" || true
    select font in "${font_array[@]}" "Manual Entry"; do
        if [[ "$font" == "Manual Entry" ]]; then
            read -p "Enter font family name exactly: " FONT_FAMILY
            break
        elif [[ -n "$font" ]]; then
            FONT_FAMILY=$font
            break
        fi
    done

    echo ""
    echo "Summary:"
    echo "  Language: $LANG_CODE"
    echo "  Font:     $FONT_FAMILY"
    read -p "Proceed with installation? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
}

install_logic() {
    local lang=$1
    local font=$2
    local repo_root=$3

    local conf_dir="$HOME/.config/fontconfig/conf.d"
    local conf_file="$conf_dir/99-$lang-fonts.conf"

    echo "--- Setting up $font for language: $lang ---"

    mkdir -p "$conf_dir"

    if [[ -f "$conf_file" ]]; then
        read -p "Warning: Config file already exists at $conf_file. Overwrite? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping file creation for $lang."
            return
        fi
    fi

    local repo_conf_file="$repo_root/.config/fontconfig/conf.d/99-$lang-fonts.conf"

    if [[ -f "$repo_conf_file" ]]; then
        echo "Found existing config in repository: $repo_conf_file"
        echo "Copying to $conf_file..."
        cp "$repo_conf_file" "$conf_file"
    else
        echo "Generating new configuration at $conf_file..."
        cat > "$conf_file" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <!-- Preferred fonts for $lang language -->
  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$lang</string>
    </test>
    <test name="family">
      <string>sans-serif</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$font</string>
    </edit>
  </match>

  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$lang</string>
    </test>
    <test name="family">
      <string>serif</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$font</string>
    </edit>
  </match>

  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$lang</string>
    </test>
    <test name="family">
      <string>monospace</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$font</string>
    </edit>
  </match>
</fontconfig>
EOF
    fi

    echo "Applying global Flatpak overrides..."
    flatpak override --user --filesystem=xdg-config/fontconfig:ro --filesystem=~/.local/share/fonts:ro

    echo "Refreshing font cache..."
    fc-cache -f

    echo "--- Done! Restart your Flatpak applications to see the changes. ---"
    echo "Verification: flatpak run --command=fc-match <AppID> :lang=$lang"
}

uninstall_logic() {
    local lang=$1
    local conf_file="$HOME/.config/fontconfig/conf.d/99-$lang-fonts.conf"

    if [[ -f "$conf_file" ]]; then
        echo "Removing font configuration for $lang at $conf_file..."
        rm -i "$conf_file"
        echo "Refreshing font cache..."
        fc-cache -f
        echo "Successfully uninstalled font config for $lang."
    else
        echo "No configuration found for language: $lang at $conf_file"
    fi
}

# --- Main ---

check_dependencies
REPO_ROOT=$(get_repo_root)

if [[ $# -eq 0 ]]; then
    run_interactive
    install_logic "$LANG_CODE" "$FONT_FAMILY" "$REPO_ROOT"
elif [[ "$1" == "uninstall" ]]; then
    if [[ -z "$2" ]]; then
        show_usage
        exit 1
    fi
    uninstall_logic "$2"
else
    if [[ -z "$2" ]]; then
        show_usage
        exit 1
    fi
    install_logic "$1" "$2" "$REPO_ROOT"
fi
