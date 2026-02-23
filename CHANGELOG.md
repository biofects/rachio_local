# Changelog

All notable changes to this project will be documented in this file.

## v2.5.1 (2026-02-23) - Bug Fix Release

### 🐛 Bug Fixes
- **services.yaml:** Fixed duplicate 'fields' key in `update_program` service definition that was causing YAML validation errors (PR #26 by [@truffshuff](https://github.com/truffshuff)) - Fixes issue #25

### 🙏 Contributors
- [@truffshuff](https://github.com/truffshuff) - Bug fix for duplicate fields key

---

## v2.5.0 (2025-10-23) - Major Smart Hose Timer Enhancement Release

### 🎉 Major Contributions by [@truffshuff](https://github.com/truffshuff)
A huge thank you to **@truffshuff** for this massive PR #20 with comprehensive Smart Hose Timer enhancements, new platforms, and diagnostic features!

### 🆕 New Platforms
- **Button Platform:** Added refresh buttons for manual data updates
  - Normal refresh (respects cache)
  - Full refresh (clears program cache)
  - Available for both Controllers and Smart Hose Timers
- **Calendar Platform:** Smart Hose Timer schedule calendar entity
  - Shows past watering events (up to 180 days retention)
  - Displays future scheduled programs
  - Persists historical data across restarts
  - Skip/manual run annotations

### 🌊 Smart Hose Timer Enhancements
- **Program Management Services:** New services for complete program control
  - `rachio_local.create_program` - Create programs with full scheduling options
  - `rachio_local.update_program` - Update existing programs with intuitive UI
  - `rachio_local.enable_program` - Enable disabled programs
  - `rachio_local.disable_program` - Disable programs
  - `rachio_local.delete_program` - Remove programs
- **Program Caching:** Intelligent caching with timestamps to reduce API calls
- **Run History Tracking:** Previous and next run summaries for programs and valves
- **Dynamic Entity Management:** Automatic creation/removal of program entities
- **Enhanced Program Sensors:** Rich program details with scheduling information
- **Valve Day Views Integration:** Uses `getValveDayViews` API for comprehensive schedule data

### 📊 New Diagnostic Sensors
- **API Rate Limiting:** Track remaining API calls and rate limit status
- **Polling Status:** Monitor current polling behavior and intervals
- **Base Station Diagnostics:**
  - Connection status
  - BLE firmware version
  - WiFi firmware version
  - RSSI (signal strength)
- **Valve Diagnostics:**
  - Connection status per valve
  - Firmware version per valve
  - RSSI per valve
  - Battery level per valve

### ⚙️ Configurable Settings (Number Entities)
- **Idle Polling Interval:** Configure polling frequency when system is idle (default: 300s)
- **Active Watering Polling Interval:** Configure polling frequency during watering (default: 120s)
- **Program Details Refresh Interval:** Configure how often to refresh program details (default: 3600s/1 hour)
- **Summary End Days:** Configure calendar future day range (default: 7 days)
- All settings persist to config entry options

### 🔧 Controller Improvements
- **Better Running Zone Detection:** Enhanced `/current_schedule` API usage with multiple fallbacks
- **Optimistic State Handling:** Configurable optimistic window with automatic cleanup
- **Safe Polling Calculation:** Helper function to compute safe intervals based on device count
- **Reduced Log Noise:** Fixed incorrect WARNING log levels, cleaned up verbose logging

### 🎨 User Experience Improvements
- **Intuitive Service UI:** Time format (HH:MM:SS) instead of seconds
- **Global Valve Selection:** Select valves once, apply to all runs
- **Entity Pickers:** Dropdown selectors for easy valve/program selection
- **Run-Specific Settings:** Per-run concurrent and cycle-and-soak options
- **Flexible Update Modes:** Full update or valve-only update support

### 🐛 Bug Fixes
- **Entity Registry Cleanup:** Properly removes entities for deleted programs
- **State Restoration:** Last watered sensors now restore state on startup
- **Rate Limit Handling:** Better HTTP 429 detection and backoff
- **Program Discovery:** Fixed detection of multi-valve programs
- **Service Registration:** All services now properly documented in services.yaml

### 📚 Documentation
- Added comprehensive service examples
- Added quick start guides for program management
- Added implementation summaries
- Added user-friendly UI documentation

### 🔒 Code Quality
- Proper async/await patterns throughout
- Better error handling and validation
- Defensive programming with fallbacks
- Entity registry integration
- Config entry options migration

## v2.4.0 (2025-10-09) - Smart Hose Timer Enhancement Release

### 🎉 Major Contributions by [@truffshuff](https://github.com/truffshuff)
A huge thank you to **@truffshuff** for these excellent improvements to Smart Hose Timer functionality and overall reliability!

### Enhanced Smart Hose Timer Features
- **Improved State Tracking:** Enhanced valve-level connection checks before marking zones as running
- **Optimistic State Preservation:** Better handling of API lag during quick start/stop operations  
- **Accurate Last Watered Times:** Fixed zone optimistic state detection when valves are force-stopped then restarted
- **Persistent Last Watered:** Last watered times now persist across Home Assistant restarts using RestoreEntity
- **Enhanced Stop Logic:** Better verification of actual valve operations before recording completion times
- **Connection Status Monitoring:** Added diagnostic sensors for base station connectivity and detailed valve status
- **API Call Optimization:** Enhanced API call tracking to read actual API calls from response headers when available
- **Improved Polling:** Updated polling interval calculation to account for pending valve starts
- **Reliability Improvements:** Prevented false positive time updates when base station or valves are disconnected
- **Smart Hose Timer Program Sensors:** Added comprehensive program display with multi-valve support
- **Enhanced Program Discovery:** Uses getValveDayViews endpoint to capture all programs including multi-valve schedules
- **Rich Program Information:** Programs show schedule times, days of week, duration, valve associations, and colors
- **User-Configurable Polling:** Added persistent, user-configurable polling intervals
- **Improved API Efficiency:** Added POST request support and better program metadata extraction

### Bug Fixes
- **Service Registration:** Fixed missing `rachio_local.turn_on` and `rachio_local.turn_off` service registration
- **Switch Logic:** Updated switch logic to better reflect actual state when manually stopping zones

## v2.3.1 (2025-06-27)
- Fix: Smart Hose Timer switch and sensor now correctly reflect stopped state when stopped from either the app or Home Assistant.
- Improved: Enhanced polling logic for Smart Hose Timer to detect active/inactive valves based on reported state and last watering action.
- Chore: Bump manifest version to 2.3.1.

## v2.3.0 (2025-06-27)
- Fix: Zone and schedule sensors now always reflect the true running state, even for manual runs started from the Rachio app.
- Improved: Polling logic is now fully dynamic and API-efficient, with interval and device count exposed via a Home Assistant sensor.
- Fix: Polling status sensor now correctly shows the total number of devices/controllers.
- Improved: API call sensor resets and tracks calls per window more accurately.
- Refactor: Data structure and setup logic for better multi-device support and diagnostics.
- Debug: Enhanced logging for all state transitions and API responses.

## v2.2.0 (2025-06-23)
- Feature: Added support for starting and stopping schedules using the Rachio ScheduleRuleService API (`/public/schedulerule/start` and `/public/schedulerule/stop`).
- No changes to zone logic; zone start/stop remains as before.

## v2.0.1 (2025-06-23)
- Fix: Prevent KeyError if no schedule is running (safe access to schedule id in controller).

## v2.0.0 (2025-06-20)
- Major refactor: Device handler logic split into dedicated files for controllers and smart hose timers.
- Added full support for Rachio Smart Hose Timer devices (valves, battery, last watered, etc.).
- Improved and fixed optimistic timer and state clearing logic for both device types.
- Persistent caching for last watered on smart hose timer.
- Added new diagnostic sensors: battery, paused, on, rain sensor tripped, and schedule status.
- Rain delay control now includes a switch and a dropdown (select entity) for duration.
- Removed connection sensor for smart hose timers (still present for controllers).
- Improved Home Assistant compatibility and removed warnings about device_class/unit_of_measurement.
- Robust error handling and more efficient polling logic.
- All sensors/entities are now registered with the correct handler/coordinator.
- Many bug fixes and code cleanups.

## v1.2.0 (2024-12-10)
- Feature: Added rain delay control and improved error handling.
- Feature: Added support for multiple controllers.
- Fix: Improved compatibility with Home Assistant 2024.x releases.

## v1.1.0 (2024-10-05)
- Feature: Added support for zone last watered sensor.
- Feature: Added connection status sensor.
- Fix: Improved polling reliability and reduced API calls.

## v1.0.0 (2024-08-01)
- Initial release: Basic support for Rachio controllers and zone switches in Home Assistant.

---

### Breaking Change in v2.0.0
- The device handler logic was refactored and split into dedicated files for controllers and smart hose timers.
- Entity unique IDs and structure may have changed. You may need to reconfigure or re-add entities in Home Assistant after upgrading to v2.0.0.
