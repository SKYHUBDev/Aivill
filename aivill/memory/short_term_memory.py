"""
Short-term memory module - stores recent events and context.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import deque


class ShortTermMemory:
    """
    Stores recent events and context for immediate decision-making.
    
    Attributes:
        events: Recent events in chronological order
        max_events: Maximum number of events to store
        context_window: Time window for context consideration
    """
    
    def __init__(self, max_events: int = 50, context_window_minutes: int = 30):
        self.max_events = max_events
        self.context_window_minutes = context_window_minutes
        self.events: deque = deque(maxlen=max_events)
        self.current_situation: Dict[str, Any] = {}
    
    def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event to short-term memory."""
        event_entry = {
            **event,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event_entry)
    
    def get_recent_events(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent events."""
        return list(self.events)[-count:]
    
    def get_events_in_window(self) -> List[Dict[str, Any]]:
        """Get events within the context window."""
        cutoff_time = datetime.now() - timedelta(minutes=self.context_window_minutes)
        relevant_events = []
        
        for event in self.events:
            event_time = datetime.fromisoformat(event.get("timestamp", ""))
            if event_time >= cutoff_time:
                relevant_events.append(event)
        
        return relevant_events
    
    def get_event_count(self) -> int:
        """Get the number of events in memory."""
        return len(self.events)
    
    def update_situation(self, situation: Dict[str, Any]) -> None:
        """Update the current situation context."""
        self.current_situation = {
            **situation,
            "updated_at": datetime.now().isoformat()
        }
    
    def get_situation(self) -> Dict[str, Any]:
        """Get the current situation."""
        return self.current_situation
    
    def clear(self) -> None:
        """Clear all short-term memory."""
        self.events.clear()
        self.current_situation = {}
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of the current context."""
        recent = self.get_recent_events(5)
        return {
            "event_count": len(self.events),
            "recent_events": [e.get("event_type", "unknown") for e in recent],
            "current_situation": self.current_situation.get("type", "none"),
            "context_window_minutes": self.context_window_minutes
        }
    
    def find_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Find all events of a specific type."""
        return [e for e in self.events if e.get("event_type") == event_type]
    
    def get_last_event_of_type(self, event_type: str) -> Optional[Dict[str, Any]]:
        """Get the most recent event of a specific type."""
        for event in reversed(self.events):
            if event.get("event_type") == event_type:
                return event
        return None
