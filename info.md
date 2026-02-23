# Rachio Local Control

**Rachio Local** is a Home Assistant integration that enables seamless control and monitoring of Rachio irrigation systems through the Rachio API. By leveraging secure, outgoing API calls, this integration allows you to retrieve real-time device status, manage watering schedules, control irrigation zones, and receive updates about your Rachio sprinkler system.

Unlike traditional integrations that require complex webhook setups, this plugin simplifies connectivity by making direct, authenticated API requests, ensuring a straightforward and secure method without exposing your home network to inbound connections.

## ✨ Key Features

### Core Functionality
- **Zone Watering Control:** Start and stop individual irrigation zones through switches
- **Device & Zone Status:** Real-time status sensors for devices and zones
- **Schedule Management:** Control and monitor irrigation schedules
- **Last Watered Tracking:** Track when each zone was last watered
- **Smart Polling:** 5-minute intervals when idle, 30-second intervals during active watering
- **API Rate Management:** Optimized to stay within Rachio's 1700 daily API call limit

### Smart Hose Timer Features (v2.5.0+)
- **Program Management Services:**
  - Create, update, enable, disable, and delete watering programs
  - Full scheduling options (days of week, interval days, fixed times, sun-based times)
  - Multi-valve support with custom durations
  - Concurrent watering and cycle-and-soak options

- **Calendar Platform:** Visualize watering schedules with 180-day history
- **Button Platform:** Manual refresh controls (normal and full refresh)
- **Diagnostic Sensors:**
  - API rate limiting tracking
  - Base station connection status and firmware versions
  - Valve diagnostics (connection, firmware, RSSI, battery levels)
- **Configurable Polling Intervals:** Customize idle and active watering polling rates

### Multi-Device Support
- Works with multiple Rachio controllers
- Full Smart Hose Timer support
- Mixed device configurations supported

## 📋 Requirements

- Home Assistant 2025.6.1 or newer
- Rachio irrigation controller or Smart Hose Timer
- Rachio API key (obtainable from your Rachio account)

## 🔧 Installation

### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the menu (⋮) and select "Custom repositories"
4. Add `https://github.com/biofects/rachio_local` as an Integration
5. Search for "Rachio Local Control"
6. Click "Download"
7. Restart Home Assistant
8. Add the integration via Settings → Devices & Services → Add Integration

### Manual Installation
1. Download the latest release from GitHub
2. Copy the `custom_components/rachio_local` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add the integration via Settings → Devices & Services → Add Integration

## ⚙️ Configuration

1. Navigate to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Rachio Local**
4. Enter your Rachio API key when prompted
5. The integration will automatically discover your devices

## 🆕 What's New in v2.5.2

### Bug Fixes
- Fixed duplicate 'fields' key in `update_program` service definition that was causing YAML validation errors

### Recent Major Updates (v2.5.0)
- Complete Smart Hose Timer program management
- Calendar integration for schedule visualization
- Button entities for manual refresh
- Comprehensive diagnostic sensors
- Configurable polling intervals
- Enhanced base station and valve diagnostics

## 📚 Documentation

For detailed documentation, service examples, and troubleshooting:
- [Full README](https://github.com/biofects/rachio_local/blob/main/README.md)
- [Service Examples](https://github.com/biofects/rachio_local/blob/main/SERVICE_EXAMPLES.md)
- [Changelog](https://github.com/biofects/rachio_local/blob/main/CHANGELOG.md)

## 💬 Support

- [Report Issues](https://github.com/biofects/rachio_local/issues)
- [View Changelog](https://github.com/biofects/rachio_local/blob/main/CHANGELOG.md)

## 💸 Support Development

If you find this integration useful, please consider supporting development:

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-purple?style=for-the-badge)](https://github.com/sponsors/biofects)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TWRQVYJWC77E6)

---

**License:** MIT  
**Developer:** [@biofects](https://github.com/biofects)
