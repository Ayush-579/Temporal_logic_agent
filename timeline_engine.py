from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class TimelineEngine:
    """
    Simple temporal logic engine tailored to the ZCPP-style rules.
    Encodes dependencies instead of using heavy logic libraries.
    """

    def __init__(self):
        # For Task 4, you can hard-code the key dependencies/spec
        self.events: Dict[str, Dict[str, Any]] = {
            # Hidden-trap analog:
            "12": {
                "description": "Topic 12: effective upon Presidential certification",
                "depends_on": "CERT",
                "offset_days": 0,
            },
            "22": {
                "description": "Topic 22: effective 45 days after Topic 12 takes effect",
                "depends_on": "12",
                "offset_days": 45,
            },
            # Global protocol:
            "PROTO": {
                "description": "Protocol: effective 45 days after Presidential certification",
                "depends_on": "CERT",
                "offset_days": 45,
            },
        }
        # Certification event is currently unknown / not occurred
        self.certification_date: Optional[datetime] = None

    def set_certification_date(self, date_str: Optional[str]) -> None:
        """Set Presidential certification date (YYYY-MM-DD) or None if it has not occurred."""
        if date_str is None:
            self.certification_date = None
        else:
            self.certification_date = datetime.fromisoformat(date_str)

    def effective_date(self, key: str) -> Optional[datetime]:
        """Compute effective date for a rule by following dependency chain."""
        if key == "CERT":
            return self.certification_date
        if key not in self.events:
            return None

        dep = self.events[key]["depends_on"]
        base = self.effective_date(dep)
        if base is None:
            return None

        offset = self.events[key]["offset_days"]
        return base + timedelta(days=offset)

    def is_active_on(self, key: str, date_str: str) -> Dict[str, Any]:
        """Return whether rule 'key' is active on date Y."""
        query_date = datetime.fromisoformat(date_str)
        eff = self.effective_date(key)
        if eff is None:
            return {
                "active": False,
                "effective_date": None,
                "reason": f"{key} depends on an event that has not occurred (e.g., certification).",
            }
        return {
            "active": query_date >= eff,
            "effective_date": eff.date().isoformat(),
            "reason": f"{key} becomes effective on {eff.date().isoformat()}.",
        }

    def deadline_from_event(self, offset_days: int, event_date: str) -> str:
        """Compute 'What's the deadline for action A if event B occurred on date C?'"""
        dt = datetime.fromisoformat(event_date)
        return (dt + timedelta(days=offset_days)).date().isoformat()
