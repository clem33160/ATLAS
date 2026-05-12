from __future__ import annotations


def list_upcoming_events(api_list_fn, calendar_id: str, limit: int = 20) -> list[dict]:
    return api_list_fn(calendar_id, limit)


def map_events_to_jobs(events: list[dict]) -> list[dict]:
    return [{"job_title": e.get("summary", ""), "when": e.get("start", ""), "location": e.get("location", ""), "source": "google_calendar"} for e in events]
