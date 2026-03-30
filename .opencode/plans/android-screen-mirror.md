# Android Screen Mirroring to Linux Plan

## Goal
Mirror Android device screen to Linux (Arch, GNOME) without enabling developer options (blocked by banking app). Preference for a simple, native-like solution.

## Constraints
- No enabling of Android developer options / USB debugging.
- No system changes (plan mode only; suggestions only).
- User wants a "nice simple native way".

## Recommended Solution: ScreenStream (Android App) + Web Browser
ScreenStream is an open-source Android app that streams device screen via HTTP (MJPEG) to any web browser. No developer options, no root, no internet required for local mode.

### Advantages
- **No developer options needed**: Uses Android MediaProjection API (requires Android 6.0+).
- **Simple setup**: Install app, start stream, open browser on Linux.
- **Local network**: Works over Wi-Fi, no internet required.
- **Open source**: Available on F-Droid (ad‑free) and GitHub.

### Steps for User (High‑Level)
1. **Install ScreenStream on Android**:
   - Download from F-Droid: https://f-droid.org/packages/info.dvkr.screenstream/
   - Or from GitHub: https://github.com/dkrivoruchko/ScreenStream
   - (Google Play version includes ads and extra WebRTC global mode; F‑Droid version is ad‑free.)
2. **Start streaming**:
   - Open ScreenStream app, choose “Local (MJPEG)” mode.
   - The app will display an IP address and port (e.g., `http://192.168.1.100:8080`).
3. **View on Linux**:
   - Open a web browser on the same local network.
   - Navigate to the displayed IP address.
   - The Android screen appears in the browser window.

### Limitations
- **No audio**: Local MJPEG mode does not transmit audio. (Audio is supported in RTSP mode, which requires an RTSP client like VLC.)
- **Latency**: Expect ~0.5‑1 s delay, not suitable for fast‑paced gaming.
- **No control**: View‑only; cannot control Android from Linux. (For control, developer options are required.)
- **Security**: Optional PIN can be set for local stream; no encryption by default.

## Alternative Solutions (Require Developer Options)
If the user can temporarily enable developer options (e.g., on a secondary device or by hiding them later), the following are more powerful:

### scrcpy (Official Repository)
- **Install**: `sudo pacman -S scrcpy`
- **Requires**: USB debugging (developer options) or wireless ADB (Android 11+).
- **Features**: Real‑time mirroring, keyboard/mouse control, audio forwarding (Android 11+), recording, etc.
- **Wireless setup**: After initial USB connection, can switch to TCP/IP mode.

### GNOME Network Displays (AUR)
- **Install**: `paru -S gnome-network-displays`
- **Note**: Designed as a Miracast **source** (casting Linux to external displays), not a sink (receiving from Android). Likely not suitable for phone→desktop.

### Miracast Sink (Experimental)
- **Miraclecast**: https://github.com/albfan/miraclecast
- **Complex setup**, requires dedicating Wi‑Fi interface, high latency, no UIBC (input). Not recommended for interactive use.

## Decision Points
- If the user only needs **view‑only** and can install an app, **ScreenStream** is the simplest.
- If the user needs **control** and can enable developer options temporarily, **scrcpy** is the best.
- If the user absolutely cannot install any app and cannot enable developer options, there is currently no simple native solution. Hardware HDMI capture or a Raspberry Pi acting as a Miracast sink could be considered, but are complex.

## Next Steps (If User Proceeds with ScreenStream)
1. Download ScreenStream APK from F‑Droid or GitHub.
2. Install on Android (allow “install from unknown sources” if needed).
3. Open app, grant screen capture permission.
4. Choose “Local (MJPEG)” mode, note the IP address.
5. Open browser on Linux, enter the IP address.
6. Optionally set a PIN for security.

## Notes
- This plan is for **information only**. No system changes will be made.
- The user must perform all installation steps themselves.
- For further details, refer to ScreenStream documentation and repository.