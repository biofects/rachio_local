"""Constants for the Rachio Local integration."""

DOMAIN = "rachio_local"
VERSION = "2.5.2"

# Configuration
CONF_API_KEY = "api_key"
DEFAULT_NAME = "Rachio"

# State Constants
STATE_ONLINE = "online"
STATE_OFFLINE = "offline"
STATE_WATERING = "watering"
STATE_NOT_WATERING = "not_watering"
STATE_STANDBY = "standby"
STATE_IDLE = "idle"
STATE_SCHEDULED = "scheduled"
STATE_DISABLED = "disabled"
STATE_PROCESSING = "processing"
STATE_ERROR = "error"
STATE_COMPLETE = "complete"
STATE_PENDING = "pending"
STATE_CONNECTED = "connected"
STATE_DISCONNECTED = "disconnected"
STATE_PAUSED = "paused"
STATE_STOPPED = "stopped"
STATE_RUNNING = "running"

# API base URLs
API_BASE_URL = "https://api.rach.io/1/public"
CLOUD_BASE_URL = "https://cloud-rest.rach.io"

# Controller API Endpoints
PERSON_INFO_ENDPOINT = "person/info"
PERSON_GET_ENDPOINT = "person/{id}"
DEVICE_GET_ENDPOINT = "device/{id}"
DEVICE_CURRENT_SCHEDULE = "device/{id}/current_schedule"
DEVICE_EVENT = "device/{id}/event"
DEVICE_STOP_WATER = "device/stop_water"
ZONE_START = "zone/start"
ZONE_STOP = "zone/stop"
ZONE_GET = "zone/{id}"
SCHEDULE_START = "schedulerule/start"
SCHEDULE_STOP = "schedulerule/stop"
SCHEDULE_SKIP = "schedulerule/skip"

# Smart Hose Timer API Endpoints
VALVE_LIST_BASE_STATIONS_ENDPOINT = "/valve/listBaseStations/{userId}"
VALVE_GET_BASE_STATION_ENDPOINT = "/valve/getBaseStation/{id}"
VALVE_LIST_VALVES_ENDPOINT = "/valve/listValves/{baseStationId}"
VALVE_GET = "valve/getValve/{id}"
VALVE_START = "valve/startWatering"
VALVE_STOP = "valve/stopWatering"
VALVE_DEFAULT_RUNTIME = "valve/setDefaultRuntime"
PROGRAM_LIST = "program/listPrograms/{entityId}"
PROGRAM_LIST_PROGRAMS_ENDPOINT = "/program/listPrograms/{baseStationId}"
PROGRAM_LIST_V2 = "/program/listProgramsV2"
PROGRAM_GET = "program/getProgram/{id}"
PROGRAM_GET_V2 = "program/getProgramV2/{id}"
PROGRAM_CREATE = "program/createProgramV2"
PROGRAM_UPDATE = "program/updateProgramV2"
PROGRAM_DELETE = "program/deleteProgram/{id}"
SUMMARY_VALVE_VIEWS = "summary/getValveDayViews"

# Status Constants
STATUS_ONLINE = "ONLINE"
STATUS_OFFLINE = "OFFLINE"
STATUS_IDLE = "IDLE"
STATUS_RUNNING = "RUNNING"
STATUS_SCHEDULED = "SCHEDULED"

# Device Types
DEVICE_TYPE_CONTROLLER = "CONTROLLER"
DEVICE_TYPE_SMART_HOSE_TIMER = "SMART_HOSE_TIMER"
