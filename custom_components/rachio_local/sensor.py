"""Rachio sensor platform."""
import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATE_WATERING, STATE_IDLE, STATE_SCHEDULED, STATE_PROCESSING

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Rachio sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    sensors = [RachioDeviceStatusSensor(coordinator)]
    for zone in coordinator.zones:
        sensors.extend([
            RachioZoneLastWateredSensor(coordinator, zone),
            RachioZoneStatusSensor(coordinator, zone)
        ])
    for schedule in coordinator.schedules:
        sensors.append(RachioScheduleStatusSensor(coordinator, schedule))
    
    async_add_entities(sensors)

class RachioDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of the Rachio device status sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Rachio Device Status"
        self._attr_unique_id = f"{DOMAIN}_device_status"

    @property
    def state(self):
        """Return the state of the device."""
        return self.coordinator.device_info.get('status', 'Unknown')

    @property
    def extra_state_attributes(self):
        """Return device information."""
        return {
            "device_id": self.coordinator.device_id,
            "name": self.coordinator.device_info.get('name'),
            "model": self.coordinator.device_info.get('model')
        }

class RachioZoneLastWateredSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Rachio zone last watered timestamp sensor."""

    def __init__(self, coordinator, zone):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._zone = zone
        self._attr_name = f"Rachio {zone['name']} Last Watered"
        self._attr_unique_id = f"rachio_zone_{zone['id']}_last_watered"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def state(self):
        """Return the state of the sensor."""
        last_watered = self._zone.get('lastWateredDate')
        if last_watered:
            return datetime.fromtimestamp(last_watered / 1000).isoformat()
        return None

class RachioZoneStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Rachio zone status sensor."""

    def __init__(self, coordinator, zone):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._zone = zone
        self._attr_name = f"Rachio {zone['name']} Status"
        self._attr_unique_id = f"rachio_zone_{zone['id']}_status"

    @property
    def state(self):
        """Return the state of the zone."""
        is_running = any(
            running_zone['id'] == self._zone['id']
            for running_zone in self.coordinator.running_zones
        )
        _LOGGER.debug(f"Zone {self._zone['id']} status - Running: {is_running}")
        return STATE_WATERING if is_running else self._zone.get('status', STATE_IDLE)

    @property
    def extra_state_attributes(self):
        """Return additional zone attributes."""
        running_info = next(
            (zone for zone in self.coordinator.running_zones if zone['id'] == self._zone['id']),
            None
        )
        return {
            "zone_id": self._zone['id'],
            "zone_number": self._zone.get('zoneNumber'),
            "enabled": self._zone.get('enabled', False),
            "running": bool(running_info),
            "remaining_time": running_info.get('remaining_time') if running_info else None,
            "run_type": running_info.get('run_type') if running_info else None,
            "detected_externally": running_info.get('run_type') == 'external' if running_info else False
        }

class RachioScheduleStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Rachio schedule status sensor."""

    def __init__(self, coordinator, schedule):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._schedule = schedule
        self._attr_name = f"Rachio {schedule.get('name', 'Unknown')} Schedule Status"
        self._attr_unique_id = f"rachio_schedule_{schedule.get('id')}_status"

    @property
    def state(self):
        """Return the state of the schedule."""
        is_running = any(
            running_schedule['id'] == self._schedule['id']
            for running_schedule in self.coordinator.running_schedules
        )
        _LOGGER.debug(f"Schedule {self._schedule['id']} status - Running: {is_running}")
        return STATE_WATERING if is_running else self._schedule.get('status', STATE_SCHEDULED)

    @property
    def extra_state_attributes(self):
        """Return additional schedule attributes."""
        running_info = next(
            (sched for sched in self.coordinator.running_schedules if sched['id'] == self._schedule['id']),
            None
        )
        active_schedule_info = self.coordinator._active_schedules.get(self._schedule['id'], {})
        attrs = {
            "schedule_id": self._schedule['id'],
            "schedule_name": self._schedule.get('name'),
            "total_duration": active_schedule_info.get('total_duration') if active_schedule_info else self._schedule.get('totalDuration'),
            "running": bool(running_info),
            "current_zone_id": running_info.get('running_zone_id') if running_info else None,
            "current_zone_name": running_info.get('running_zone_name') if running_info else None,
            "detected_externally": running_info is not None and 'run_type' not in running_info,
            "manually_persisted": bool(active_schedule_info and (not running_info or running_info.get('running_zone_id') is None)),
            "remaining_time": (
                (active_schedule_info.get('total_duration') - 
                 (datetime.now() - active_schedule_info.get('start_time', datetime.now())).total_seconds())
                if active_schedule_info else None
            )
        }
        return attrs
