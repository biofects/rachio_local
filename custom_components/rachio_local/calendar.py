"""
Home Assistant Calendar entity for Rachio Smart Hose Timer
Shows past and future program/valve runs, with skip annotations.
"""

from datetime import timedelta
import logging
import json
import re
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.util import dt as dt_util
from homeassistant.helpers.storage import Store
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Summary prefix added to skipped runs, e.g. "Rain Skip: Back Lawn - Back Sprinklers"
_SKIP_PREFIX_RE = re.compile(r"^(?:\w+ Skip|Skipped): ")


def _skip_reason(skip):
    """Return a short reason ("Rain", "Manual", ...) for a valve run's skip dict, or None."""
    if not skip:
        return None
    for key in skip:
        if key.endswith("OverrideTrigger"):
            reason = key[: -len("OverrideTrigger")]
            return reason[:1].upper() + reason[1:]
    return "Unknown"


def _skip_summary(summary, reason):
    """Prefix a summary so skipped runs stand out on the calendar."""
    return f"{reason} Skip: {summary}" if reason and reason != "Unknown" else f"Skipped: {summary}"


def _skip_details(skip, reason):
    """Describe why a run was skipped, including rain amounts when available."""
    detail = f"Skipped ({reason})"
    rain = skip.get("rainOverrideTrigger") or {}
    amounts = []
    if rain.get("predictedPrecipMm") is not None:
        amounts.append(f"predicted {rain['predictedPrecipMm']} mm")
    if rain.get("observedPrecipMm") is not None:
        amounts.append(f"observed {rain['observedPrecipMm']} mm")
    if amounts:
        detail += f": {', '.join(amounts)}"
    return detail


def _is_skipped(event):
    return bool(_SKIP_PREFIX_RE.match(event.summary or ""))


def _event_key(event):
    """Dedupe key that ignores the skip prefix, so a run marked skipped replaces its unmarked copy."""
    return (event.start, _SKIP_PREFIX_RE.sub("", event.summary or ""))

async def async_setup_entry(hass, config_entry, async_add_entities):
    devices = hass.data[DOMAIN][config_entry.entry_id]["devices"]
    entities = []
    from .smart_hose_timer import RachioSmartHoseTimerHandler
    for device in devices.values():
        handler = device.get("handler")
        if isinstance(handler, RachioSmartHoseTimerHandler):
            entities.append(RachioSmartHoseTimerCalendar(handler))
    if entities:
        async_add_entities(entities, update_before_add=True)

class RachioSmartHoseTimerCalendar(CalendarEntity):
    _STORAGE_VERSION = 1
    _STORAGE_KEY_TEMPLATE = f"{{domain}}_calendar_events_{{device_id}}.json"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._handler.device_id)},
            "name": self._handler.name,
            "model": self._handler.model,
            "manufacturer": "Rachio",
        }
    def __init__(self, handler):
        self._handler = handler
        self._attr_name = f"{handler.name} Schedule"
        self._attr_unique_id = f"{handler.device_id}_calendar"
        self._events = []
        self._persisted_events = []
        self._store = None

    @property
    def event(self):
        """Return the next upcoming event that will actually water."""
        now = dt_util.utcnow()
        for event in self._events:
            if event.start >= now and not _is_skipped(event):
                return event
        return None

    async def async_update(self):
        # Load persisted events if not already loaded
        if self._store is None:
            self._store = Store(
                self._handler.hass,
                self._STORAGE_VERSION,
                self._STORAGE_KEY_TEMPLATE.format(domain=DOMAIN, device_id=self._handler.device_id),
            )
            data = await self._store.async_load()
            if data:
                self._persisted_events = [self._deserialize_event(e) for e in data.get("events", [])]
        
        # Build new events from API
        new_events = self._build_events()
        now = dt_util.utcnow()
        
        # Separate past and future events from API
        past_new_events = [e for e in new_events if e.start < now]
        future_new_events = [e for e in new_events if e.start >= now]
        
        # Merge persisted past events with new past events (avoid duplicates by start time and summary)
        all_past_events = { _event_key(e): e for e in self._persisted_events }
        for e in past_new_events:
            all_past_events[_event_key(e)] = e
        
        # Only keep past events from the last 180 days
        cutoff = now - timedelta(days=180)
        self._persisted_events = [e for e in all_past_events.values() if e.end >= cutoff]
        
        # Save only past events to persistent storage
        await self._store.async_save({
            "events": [self._serialize_event(e) for e in self._persisted_events]
        })
        
        # Combine persisted past events with fresh future events from API for the full event list
        self._events = self._persisted_events + future_new_events
        # Sort by start time
        self._events.sort(key=lambda e: e.start)

    def _serialize_event(self, event):
        return {
            "summary": event.summary,
            "start": event.start.isoformat() if hasattr(event.start, 'isoformat') else event.start,
            "end": event.end.isoformat() if hasattr(event.end, 'isoformat') else event.end,
            "description": event.description,
        }

    def _deserialize_event(self, data):
        return CalendarEvent(
            summary=data["summary"],
            start=dt_util.parse_datetime(data["start"]),
            end=dt_util.parse_datetime(data["end"]),
            description=data.get("description"),
        )

    def _build_events(self):
        events = []
        valve_name_map = {z.get("id"): z.get("name") for z in getattr(self._handler, "zones", [])}
        now = dt_util.utcnow()

        # --- PAST EVENTS: Prefer valve_day_views, fallback to program_run_summaries/valve_run_summaries if empty ---
        day_views = getattr(self._handler, "valve_day_views", [])
        _LOGGER.debug(f"Building calendar events. valve_day_views count: {len(day_views)}, valve_name_map: {valve_name_map}")
        
        # Track future program runs we've already added (to avoid duplicates)
        # Key: (program_id, start_time) -> True
        future_programs_added = set()
        
        used_fallback = False
        if day_views:
            #_LOGGER.debug(f"Using valve_day_views for events (found {len(day_views)} days)")
            for day in day_views:
                #_LOGGER.debug(f"Processing day: {day.get('date')}, program runs: {len(day.get('valveProgramRunSummaries', []))}, quick runs: {len(day.get('valveQuickRunSummaries', []))}")
                
                # Process program runs
                for vprs in day.get("valveProgramRunSummaries", []):
                    program_name = vprs.get("programName", vprs.get("programId", "Program"))
                    program_id = vprs.get("programId")
                    #_LOGGER.debug(f"Processing program: {program_name} (ID: {program_id}), valve runs: {len(vprs.get('valveRunSummaries', []))}")
                    
                    # Get the program start time from the first valve run
                    valve_runs = vprs.get("valveRunSummaries", [])
                    if not valve_runs:
                        continue
                    
                    first_valve = valve_runs[0]
                    program_start = dt_util.parse_datetime(first_valve.get("start")) if isinstance(first_valve.get("start"), str) else first_valve.get("start")
                    
                    # Calculate total program duration
                    total_duration = vprs.get("totalRunDurationSeconds", 0)
                    if not total_duration:
                        total_duration = sum(v.get("durationSeconds", 0) for v in valve_runs)
                    
                    program_end = program_start + timedelta(seconds=total_duration)
                    
                    # Determine if this is a past or future run
                    is_future = program_start >= now
                    
                    if is_future:
                        # For future runs, create a single program-level event
                        program_key = (program_id, program_start)
                        if program_key not in future_programs_added:
                            future_programs_added.add(program_key)
                            
                            # Get valve list for description
                            valve_ids = [v.get("valveId") for v in valve_runs if v.get("valveId")]
                            valve_names = [valve_name_map.get(vid, vid) for vid in valve_ids]
                            
                            desc = [f"Program: {program_name}"]
                            if program_id:
                                desc.append(f"Program ID: {program_id}")
                            if valve_names:
                                desc.append(f"Valves: {', '.join(valve_names)}")

                            # The program is skipped only if every valve run is skipped
                            summary = program_name
                            skipped_runs = [v for v in valve_runs if v.get("skip")]
                            if skipped_runs:
                                skip = skipped_runs[0]["skip"]
                                reason = _skip_reason(skip)
                                if len(skipped_runs) == len(valve_runs):
                                    summary = _skip_summary(program_name, reason)
                                    desc.insert(0, _skip_details(skip, reason))
                                else:
                                    skipped_names = [valve_name_map.get(v.get("valveId"), v.get("valveId")) for v in skipped_runs]
                                    desc.append(f"Partially skipped ({reason}): {', '.join(skipped_names)}")

                            events.append(CalendarEvent(
                                summary=summary,
                                start=program_start,
                                end=program_end,
                                description=" | ".join(desc)
                            ))
                    else:
                        # For past runs, create individual valve events
                        for valve in valve_runs:
                            valve_id = valve.get("valveId")
                            valve_name = valve.get("valveName", valve_id)
                            v_start = dt_util.parse_datetime(valve.get("start")) if isinstance(valve.get("start"), str) else valve.get("start")
                            v_end = v_start + timedelta(seconds=valve.get("durationSeconds", 0))
                            
                            desc = [f"Program: {program_name}", f"Valve: {valve_name}"]
                            if program_id:
                                desc.append(f"Program ID: {program_id}")
                            if valve_id:
                                desc.append(f"Valve ID: {valve_id}")
                            if valve.get("flowDetected"):
                                desc.append("Flow Detected")
                            summary = f"{program_name} - {valve_name}"
                            if valve.get("skip"):
                                reason = _skip_reason(valve["skip"])
                                summary = _skip_summary(summary, reason)
                                desc.insert(0, _skip_details(valve["skip"], reason))
                            events.append(CalendarEvent(
                                summary=summary,
                                start=v_start,
                                end=v_end,
                                description=" | ".join(desc)
                            ))
                # Quick runs
                for qrs in day.get("valveQuickRunSummaries", []):
                    for valve in qrs.get("valveRunSummaries", []):
                        valve_id = valve.get("valveId")
                        valve_name = valve.get("valveName", valve_id)
                        v_start = dt_util.parse_datetime(valve.get("start")) if isinstance(valve.get("start"), str) else valve.get("start")
                        v_end = v_start + timedelta(seconds=valve.get("durationSeconds", 0))
                        
                        # Only create events for past quick runs
                        if v_start >= now:
                            continue
                        
                        desc = [f"Manual Run", f"Valve: {valve_name}"]
                        if valve_id:
                            desc.append(f"Valve ID: {valve_id}")
                        if valve.get("flowDetected"):
                            desc.append("Flow Detected")
                        events.append(CalendarEvent(
                            summary=f"Manual Run - {valve_name}",
                            start=v_start,
                            end=v_end,
                            description=" | ".join(desc)
                        ))
                # Manual runs (if present)
                for mrs in day.get("valveManualRunSummaries", []):
                    for valve in mrs.get("valveRunSummaries", []):
                        valve_id = valve.get("valveId")
                        valve_name = valve.get("valveName", valve_id)
                        v_start = dt_util.parse_datetime(valve.get("start")) if isinstance(valve.get("start"), str) else valve.get("start")
                        v_end = v_start + timedelta(seconds=valve.get("durationSeconds", 0))
                        
                        # Only create events for past manual runs
                        if v_start >= now:
                            continue
                        
                        desc = [f"Manual Run", f"Valve: {valve_name}"]
                        if valve_id:
                            desc.append(f"Valve ID: {valve_id}")
                        if valve.get("flowDetected"):
                            desc.append("Flow Detected")
                        events.append(CalendarEvent(
                            summary=f"Manual Run - {valve_name}",
                            start=v_start,
                            end=v_end,
                            description=" | ".join(desc)
                        ))
        else:
            # Fallback: use program_run_summaries and valve_run_summaries for past events
            used_fallback = True
            program_runs = getattr(self._handler, "program_run_summaries", {})
            for program_id, runs in program_runs.items():
                for key in ("previous_run",):
                    run = runs.get(key)
                    if not run:
                        continue
                    start = run["start"]
                    duration = run.get("duration_seconds", 0)
                    end = start + timedelta(seconds=duration)
                    summary = program_id
                    events.append(CalendarEvent(
                        summary=summary,
                        start=start,
                        end=end,
                        description=f"Program ID: {program_id}"
                    ))
            # Also add quick/manual runs from valve_run_summaries
            valve_run_summaries = getattr(self._handler, "valve_run_summaries", {})
            for valve_id, runs in valve_run_summaries.items():
                for key in ("previous_run",):
                    run = runs.get(key)
                    if run and run.get("source") == "quick_run":
                        start = run["start"]
                        duration = run.get("duration_seconds", 0)
                        end = start + timedelta(seconds=duration)
                        valve_name = valve_name_map.get(valve_id, valve_id)
                        events.append(CalendarEvent(
                            summary=f"User Started: {valve_name}",
                            start=start,
                            end=end,
                            description=f"Valve: {valve_id} ({valve_name}) | Manual Run"
                        ))

        # Note: All events (past and future) are now sourced from valve_day_views above.
        # Past events show individual valve runs, future events show program-level runs.
        # We no longer need to process program_run_summaries separately since valve_day_views
        # contains all the scheduled runs within the configured time window.

        # Sort events by start time
        events.sort(key=lambda e: e.start)
        return events

    async def async_get_events(self, hass, start_date, end_date):
        """Return calendar events in a date range."""
        await self.async_update()
        return [e for e in self._events if e.start >= start_date and e.start <= end_date]
