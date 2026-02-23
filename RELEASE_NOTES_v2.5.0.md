# Release Notes - v2.5.0

## 🎉 Smart Hose Timer Enhancement Release

**Release Date:** October 23, 2025  
**Major Contributor:** [@truffshuff](https://github.com/truffshuff)

This is a **major feature release** bringing comprehensive Smart Hose Timer enhancements, new platforms, and diagnostic capabilities. A huge thank you to **@truffshuff** for the exceptional work on PR #20!

---

## 🆕 What's New

### New Platforms

#### 📅 Calendar Platform
- **Smart Hose Timer Schedule Calendar** - Visualize your watering schedules
  - Shows past watering events (up to 180 days history)
  - Displays future scheduled programs
  - Persists historical data across Home Assistant restarts
  - Includes skip and manual run annotations
  - Entity: `calendar.{device_name}_schedule`

#### 🔘 Button Platform
- **Manual Refresh Controls** - Force data updates on demand
  - **Normal Refresh** - Quick update respecting cache (1-2 API calls)
  - **Full Refresh** - Complete update clearing all caches
  - Available for both Controllers and Smart Hose Timers
  - Entities: `button.{device_name}_refresh_normal_polling` and `button.{device_name}_refresh_full`

### New Services

#### Smart Hose Timer Program Management
Complete control over your watering programs directly from Home Assistant!

- **`rachio_local.create_program`** - Create new watering programs
  - Full scheduling options (days of week, interval days, fixed times, sun-based times)
  - Multi-valve support
  - Custom durations per valve
  - Concurrent watering and cycle-and-soak options
  
- **`rachio_local.update_program`** - Update existing programs
  - Intuitive UI with HH:MM:SS time format
  - Global valve selection (no repetition needed)
  - Run-specific settings
  - Valve-only update mode
  
- **`rachio_local.enable_program`** - Enable disabled programs
  
- **`rachio_local.disable_program`** - Disable programs temporarily
  
- **`rachio_local.delete_program`** - Remove programs

### New Diagnostic Sensors

#### API & Polling Monitoring
- `sensor.{device_name}_api_calls_remaining` - Track remaining API calls
- `sensor.{device_name}_polling_status` - Monitor current polling behavior

#### Smart Hose Timer Base Station
- `sensor.{device_name}_basestation_connection` - Connection status
- `sensor.{device_name}_basestation_ble_fw` - BLE firmware version
- `sensor.{device_name}_basestation_wifi_fw` - WiFi firmware version
- `sensor.{device_name}_basestation_rssi` - Signal strength

#### Per-Valve Diagnostics
- `sensor.{device_name}_valve_{valve_name}` - Connection status
- `sensor.{device_name}_valve_{valve_name}_fw` - Firmware version
- `sensor.{device_name}_valve_{valve_name}_rssi` - Signal strength
- `sensor.{device_name}_{valve_name}_battery` - Battery level

### New Configuration Options

#### Number Entities for Customization
- **Idle Polling Interval** - Configure update frequency when idle (default: 300s)
- **Active Watering Polling Interval** - Configure updates during watering (default: 120s)
- **Program Details Refresh Interval** - Configure program cache refresh (default: 3600s/1 hour)
- **Summary End Days** - Configure calendar future range (default: 7 days)

All settings persist automatically to your configuration!

---

## 🔧 Improvements

### Smart Hose Timer
- **Intelligent Program Caching** - Reduces API calls with timestamp-based cache
- **Run History Tracking** - Previous and next run summaries for programs and valves
- **Dynamic Entity Management** - Automatically creates/removes entities for programs
- **Enhanced Program Sensors** - Rich details including scheduling, valves, colors
- **Valve Day Views Integration** - Comprehensive schedule data from Rachio API

### Controller
- **Better Running Zone Detection** - Enhanced API usage with multiple fallbacks
- **Optimistic State Handling** - Configurable window with automatic cleanup
- **Safe Polling Calculation** - Intelligent interval computation based on device count
- **Reduced Log Noise** - Fixed incorrect log levels and cleaned up verbose output

### User Experience
- **Intuitive Service UI** - Time format (HH:MM:SS) instead of seconds
- **Global Valve Selection** - Select valves once, apply to all runs
- **Entity Pickers** - Dropdown selectors for easy selection
- **Run-Specific Settings** - Per-run concurrent and cycle-and-soak options
- **Flexible Update Modes** - Full update or valve-only update support

---

## 🐛 Bug Fixes

- Fixed entity registry cleanup for deleted programs
- Fixed state restoration for last watered sensors on startup
- Improved HTTP 429 (rate limit) detection and handling
- Fixed detection of multi-valve programs
- Fixed service registration in services.yaml
- Fixed program discovery using getValveDayViews endpoint

---

## 📚 Documentation

New documentation files included:
- Service examples with real-world use cases
- Quick start guide for program management
- Implementation summaries
- User-friendly UI documentation
- Complete changelog with all changes

---

## ⚠️ Breaking Changes

**None!** This release is fully backward compatible with v2.4.0.

---

## 📦 Installation

### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to Integrations
3. Find "Rachio Local Control"
4. Click Update to v2.5.0

### Manual Installation
1. Download the latest release
2. Copy `custom_components/rachio_local` to your Home Assistant config
3. Restart Home Assistant

---

## 🚀 Getting Started with New Features

### Using the Calendar
```yaml
# Add to your dashboard
type: calendar
entities:
  - entity: calendar.hose_timers_schedule
```

### Using Refresh Buttons
```yaml
# Add to your dashboard
type: button
entity: button.tfam_sprinkler_refresh_full
tap_action:
  action: call-service
  service: button.press
  target:
    entity_id: button.tfam_sprinkler_refresh_full
```

### Creating a Program
```yaml
service: rachio_local.create_program
data:
  name: "Morning Garden"
  valves:
    - switch.hose_timer_valve_1
    - switch.hose_timer_valve_2
  total_duration: "00:15:00"  # 15 minutes split between valves
  run_1_start_time: "06:00"
  days_of_week: ["Mon", "Wed", "Fri"]
target:
  device_id: <your_device_id>
```

### Configuring Polling Intervals
Simply adjust the number entities in your dashboard or automation:
```yaml
service: number.set_value
target:
  entity_id: number.tfam_sprinkler_idle_polling_interval
data:
  value: 600  # 10 minutes
```

---

## 🔍 What's Next

We're committed to continuous improvement! Here's what we're considering for future releases:

- [ ] Weather-based watering adjustments
- [ ] Advanced scheduling templates
- [ ] Historical water usage analytics
- [ ] Integration with weather services
- [ ] More automation triggers and conditions

Have feature requests? Open an issue on [GitHub](https://github.com/biofects/rachio_local/issues)!

---

## 🙏 Acknowledgments

**Huge thank you to [@truffshuff](https://github.com/truffshuff)** for:
- 5,782 lines of code added
- 2 new platforms (Button, Calendar)
- 5 new services for program management
- Dozens of new diagnostic sensors
- 8 configurable number entities
- Comprehensive documentation
- Extensive testing and refinement

This release wouldn't be possible without your exceptional contribution! 🌟

---

## 📊 Statistics

- **Version:** 2.5.0
- **Files Changed:** 25
- **Lines Added:** 5,782
- **Lines Removed:** 79
- **New Platforms:** 2 (Button, Calendar)
- **New Services:** 5
- **New Sensors:** 14+
- **New Configuration Options:** 8

---

## 🐛 Found a Bug?

Please report issues on our [GitHub Issues](https://github.com/biofects/rachio_local/issues) page.

---

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for the complete list of changes.

---

**Happy Watering! 💦🌱**
