#!/bin/bash
# setup-flatpak-fonts.sh: Automate font prioritization for Flatpak apps.
# Usage: ./scripts/setup-flatpak-fonts.sh                    (Interactive Mode)
#        ./scripts/setup-flatpak-fonts.sh <lang-code> <font-family> (Quick Mode)
#        ./scripts/setup-flatpak-fonts.sh <lang-code> <font-family> all    (Apply to all apps)
#        ./scripts/setup-flatpak-fonts.sh uninstall                (Interactive Uninstall)
#        ./scripts/setup-flatpak-fonts.sh uninstall <lang-code>    (Quick Uninstall)

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
    echo "       $0 <lang-code> <font-family> all    (Apply to all apps)"
    echo "       $0 list                             (List configured fonts)"
    echo "       $0 uninstall                        (Interactive Uninstall)"
    echo "       $0 uninstall <lang-code>           (Quick Uninstall)"
    echo ""
    echo "Example: $0 th \"Noto Sans Thai\""
    echo "         $0 th \"Noto Sans Thai\" all"
    echo "         $0 uninstall th"
    echo "         $0 list"
}

get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null || dirname "$(dirname "$(readlink -f "$0")")"
}

run_interactive_install() {
    echo "--- Flatpak Font Setup Wizard ---"
    echo ""
    
    # 1. Select Language - use common language list for better UX
    declare -A common_langs=(
        ["ar"]="Arabic"
        ["bn"]="Bengali"
        ["zh-cn"]="Chinese (Simplified)"
        ["zh-tw"]="Chinese (Traditional)"
        ["en"]="English"
        ["fr"]="French"
        ["de"]="German"
        ["gu"]="Gujarati"
        ["he"]="Hebrew"
        ["hi"]="Hindi"
        ["ja"]="Japanese"
        ["ko"]="Korean"
        ["ml"]="Malayalam"
        ["mr"]="Marathi"
        ["nb"]="Norwegian"
        ["pa"]="Punjabi"
        ["pt"]="Portuguese"
        ["ru"]="Russian"
        ["sa"]="Sanskrit"
        ["es"]="Spanish"
        ["sv"]="Swedish"
        ["ta"]="Tamil"
        ["te"]="Telugu"
        ["th"]="Thai"
        ["uk"]="Ukrainian"
        ["vi"]="Vietnamese"
    )
    
    echo "Select a language:"
    local lang_codes=("${!common_langs[@]}" "Other")
    PS3="Enter your choice (1-${#lang_codes[@]}): "
    select lang in "${lang_codes[@]}"; do
        if [[ "$lang" == "Other" ]]; then
            read -p "Enter language code (e.g., ja, ko, zh-cn): " LANG_CODE
            if [[ ! $LANG_CODE =~ ^[a-z]{2}(-[a-z]{2})?$ ]]; then
                echo "Invalid format. Please use format like 'ja' or 'zh-cn'"
                continue
            fi
            break
        elif [[ -n "$lang" && -n "${common_langs[$lang]}" ]]; then
            LANG_CODE=$lang
            break
        else
            echo "Invalid selection. Please choose a number from the list."
        fi
    done
    unset PS3
    
    echo ""
    echo "Searching for fonts supporting '$LANG_CODE'..."
    local fonts
    fonts=$(fc-list ":lang=$LANG_CODE" family 2>/dev/null | tr ',' '\n' | sort -u)
    
    if [[ -z "$fonts" ]]; then
        echo "No fonts found for language '$LANG_CODE'. Please install a font that supports this language."
        exit 1
    fi
    
    local font_count
    font_count=$(echo "$fonts" | wc -l)
    echo "Found $font_count font(s) supporting '$LANG_CODE'"
    echo ""
    
    # 2. Select Font
    echo "Select a font family:"
    local font_array=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && font_array+=("$line")
    done <<< "$fonts"
    
    # Add manual entry option
    font_array+=("Enter manually...")
    
    if [[ ${#font_array[@]} -eq 1 ]]; then
        echo "Only one font available: ${font_array[0]}"
        FONT_FAMILY="${font_array[0]}"
    else
        PS3="Enter your choice (1-${#font_array[@]}): "
        select font in "${font_array[@]}"; do
            if [[ "$font" == "Enter manually..." ]]; then
                read -p "Enter font family name exactly (check fc-list for exact name): " FONT_FAMILY
                FONT_FAMILY=$(echo "$FONT_FAMILY" | xargs)
                if [[ -z "$FONT_FAMILY" ]]; then
                    echo "Font name cannot be empty."
                    continue
                fi
                break
            elif [[ -n "$font" ]]; then
                FONT_FAMILY=$font
                break
            else
                echo "Invalid selection. Please choose a number from the list."
            fi
        done
        unset PS3
    fi
    
    # Validate font exists
    if ! fc-list ":family=$FONT_FAMILY" family 2>/dev/null | grep -qi "$FONT_FAMILY"; then
        read -p "Warning: Font '$FONT_FAMILY' not found in system. Proceed anyway? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 0
        fi
    fi
    
    # Ask about per-app configuration
    echo ""
    read -p "Apply to ALL installed Flatpak apps? (recommended for reliability) (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        APPLY_ALL="all"
    fi
    
    echo ""
    echo "========================================"
    echo "Summary:"
    echo "  Language: $LANG_CODE (${common_langs[$LANG_CODE]:-custom})"
    echo "  Font:     $FONT_FAMILY"
    echo "  Apply to all apps: ${APPLY_ALL:-no}"
    echo "========================================"
    read -p "Proceed with installation? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
}

run_interactive_uninstall() {
    local conf_dir="$HOME/.config/fontconfig/conf.d"
    echo "--- Flatpak Font Uninstall Wizard ---"
    echo ""
    
    if [[ ! -d "$conf_dir" ]]; then
        echo "No font configuration directory found at $conf_dir"
        exit 0
    fi
    
    local files
    files=$(find "$conf_dir" -maxdepth 1 -name "99-*-fonts.conf" -printf "%f\n" | sort)
    
    if [[ -z "$files" ]]; then
        echo "No custom font configurations found."
        echo "Run without arguments to set up a new font configuration."
        exit 0
    fi
    
    echo "Configured language fonts:"
    echo ""
    local file_array=()
    local lang_array=()
    while IFS= read -r file; do
        [[ -n "$file" ]] || continue
        file_array+=("$file")
        lang=$(echo "$file" | sed 's/^99-//;s/-fonts.conf$//')
        lang_array+=("$lang")
        
        local font_name
        font_name=$(grep -oP '(?<=<string>)[^<]+(?=</string>)' "$conf_dir/$file" | head -1)
        printf "  [%d] %-10s -> %s\n" "${#file_array[@]}" "$lang" "$font_name"
    done <<< "$files"
    
    echo ""
    read -p "Select a configuration to remove (or press Enter to cancel): " -n 1 -r
    echo ""
    
    if [[ -z "$REPLY" ]]; then
        echo "Aborted."
        exit 0
    fi
    
    if [[ ! "$REPLY" =~ ^[0-9]+$ ]] || [[ "$REPLY" -lt 1 ]] || [[ "$REPLY" -gt ${#file_array[@]} ]]; then
        echo "Invalid selection."
        exit 1
    fi
    
    local idx=$((REPLY - 1))
    local file="${file_array[$idx]}"
    local lang="${lang_array[$idx]}"
    
    echo ""
    read -p "Remove configuration for '$lang'? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
}

apply_per_app_configs() {
    local lang=$1
    local font=$2
    
    echo "Applying per-app fontconfig for ALL installed Flatpak apps..."
    
    local count=0
    while IFS=$'\t' read -r name app_id rest; do
        [[ -z "$app_id" ]] && continue
        [[ "$app_id" == "Application" ]] && continue
        
        local app_conf_dir="$HOME/.var/app/$app_id/config/fontconfig/conf.d"
        local app_conf_file="$app_conf_dir/99-$lang-fonts.conf"
        local legacy_app_conf_file="$HOME/.var/app/$app_id/config/fontconfig/fonts.conf"
        
        mkdir -p "$app_conf_dir"
        
        # Remove legacy per-app config to avoid conflicting behavior
        rm -f "$legacy_app_conf_file"
        
        # Balanced config: gentle alias + targeted strong lang match
        cat > "$app_conf_file" <<EOFCONF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer><family>$font</family></prefer>
  </alias>
  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$lang</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$font</string>
    </edit>
  </match>
</fontconfig>
EOFCONF
        echo "  Applied to: $app_id"
        count=$((count + 1))
    done < <(flatpak list --app 2>/dev/null)
    
    echo "  Total apps configured: $count"
}

install_logic() {
    local lang=$1
    local font=$2
    local apply_all=$3
    local repo_root=$4

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
  <!-- Balanced font override for $lang -->
  
  <!-- 1. Gentle Suggestion for generic families (No tofu) -->
  <alias>
    <family>sans-serif</family>
    <prefer><family>$font</family></prefer>
  </alias>
  <alias>
    <family>serif</family>
    <prefer><family>$font</family></prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer><family>$font</family></prefer>
  </alias>
  
  <!-- 2. Strong Priority for explicit $lang requests (Beats FreeSerif) -->
  <match target="pattern">
    <test name="lang" compare="contains">
      <string>$lang</string>
    </test>
    <edit name="family" mode="prepend" binding="strong">
      <string>$font</string>
    </edit>
  </match>
</fontconfig>
EOF
    fi

    echo "Applying global Flatpak overrides..."
    flatpak override --user --filesystem=xdg-config/fontconfig:ro --filesystem=~/.config/fontconfig:ro --filesystem=~/.local/share/fonts:ro --filesystem=/usr/share/fonts:ro --filesystem=/usr/share/fontconfig:ro
    
    if [[ "$apply_all" == "all" ]]; then
        echo ""
        apply_per_app_configs "$lang" "$font"
    fi
    
    echo "Refreshing font cache..."
    fc-cache -f
    
    echo ""
    echo "=== VERIFICATION ==="
    echo "Host system font match:"
    fc-match :lang=$lang
    
    echo ""
    echo "Flatpak runtime font match:"
    flatpak run --command=fc-match --app=org.freedesktop.Platform//24.08 :lang=$lang 2>/dev/null || \
    flatpak run --command=fc-match --app=org.freedesktop.Platform//23.08 :lang=$lang 2>/dev/null || \
    echo "(Could not test - no freedesktop runtime available)"
    
    echo ""
    echo "--- Done! Restart your Flatpak applications to see the changes. ---"
}

uninstall_logic() {
    local lang=$1
    local conf_file="$HOME/.config/fontconfig/conf.d/99-$lang-fonts.conf"

    if [[ -f "$conf_file" ]]; then
        echo "Removing font configuration for $lang at $conf_file..."
        rm -i "$conf_file"
    else
        echo "No global configuration found for language: $lang at $conf_file"
    fi

    echo "Removing per-app configurations for $lang..."
    find "$HOME/.var/app" -path "*/config/fontconfig/conf.d/99-$lang-fonts.conf" -type f -print -delete 2>/dev/null || true

    echo "Refreshing font cache..."
    fc-cache -f
    echo "Successfully uninstalled font config for $lang."
}

list_configs() {
    local conf_dir="$HOME/.config/fontconfig/conf.d"
    
    echo "--- Configured Font Overrides ---"
    echo ""
    
    if [[ ! -d "$conf_dir" ]]; then
        echo "No font configurations found."
        exit 0
    fi
    
    local files
    files=$(find "$conf_dir" -maxdepth 1 -name "99-*-fonts.conf" -printf "%f\n" | sort)
    
    if [[ -z "$files" ]]; then
        echo "No custom font configurations found."
        exit 0
    fi
    
    printf "%-12s %s\n" "LANGUAGE" "FONT"
    echo "-----------------------------------"
    
    while IFS= read -r file; do
        [[ -n "$file" ]] || continue
        lang=$(echo "$file" | sed 's/^99-//;s/-fonts.conf$//')
        font_name=$(grep -oP '(?<=<string>)[^<]+(?=</string>)' "$conf_dir/$file" | head -1)
        printf "%-12s %s\n" "$lang" "$font_name"
    done <<< "$files"
    
    echo ""
    echo "To uninstall: $0 uninstall <lang-code>"
}

# --- Main ---

check_dependencies
REPO_ROOT=$(get_repo_root)

if [[ $# -eq 0 ]]; then
    run_interactive_install
    install_logic "$LANG_CODE" "$FONT_FAMILY" "${APPLY_ALL:-}" "$REPO_ROOT"
elif [[ "$1" == "list" ]]; then
    list_configs
elif [[ "$1" == "uninstall" ]]; then
    if [[ -z "$2" ]]; then
        run_interactive_uninstall
        uninstall_logic "$LANG_CODE"
    else
        uninstall_logic "$2"
    fi
else
    if [[ -z "$2" ]]; then
        show_usage
        exit 1
    fi
    install_logic "$1" "$2" "$3" "$REPO_ROOT"
fi
