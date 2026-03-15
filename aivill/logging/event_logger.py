"""
Event logging system - tracks all game events.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class EventLogger:
    """
    Logs all game events to a JSONL file.
    
    Provides structured event logging with timestamps,
    event types, and associated data.
    """
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.log_file.exists():
            self.log_file.touch()
        
        self.event_count = 0
        self.session_events: list[Dict[str, Any]] = []
    
    def log_event(self, event: Dict[str, Any]) -> None:
        """
        Log an event to the log file.
        
        Args:
            event: Event data to log
        """
        event_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_count": self.event_count,
            **event
        }
        
        self.event_count += 1
        self.session_events.append(event_entry)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_entry, ensure_ascii=False) + "\n")
        except IOError as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def log_game_event(
        self,
        event_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log a game event with standard formatting."""
        self.log_event({
            "event_type": event_type,
            "data": data or {}
        })
    
    def log_villain_decision(
        self,
        decision: Dict[str, Any]
    ) -> None:
        """Log a villain decision."""
        self.log_event({
            "event_type": "villain_decision",
            "decision": decision
        })
    
    def log_player_action(
        self,
        player_id: str,
        action: Dict[str, Any]
    ) -> None:
        """Log a player action."""
        self.log_event({
            "event_type": "player_action",
            "player_id": player_id,
            "action": action
        })
    
    def log_strategy_change(
        self,
        old_strategy: str,
        new_strategy: str,
        reason: str
    ) -> None:
        """Log a strategy change."""
        self.log_event({
            "event_type": "strategy_change",
            "old_strategy": old_strategy,
            "new_strategy": new_strategy,
            "reason": reason
        })
    
    def log_personality_change(
        self,
        trait: str,
        old_value: float,
        new_value: float,
        reason: str
    ) -> None:
        """Log a personality trait change."""
        self.log_event({
            "event_type": "personality_change",
            "trait": trait,
            "old_value": old_value,
            "new_value": new_value,
            "reason": reason
        })
    
    def log_outcome(
        self,
        action: str,
        outcome: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log an action outcome."""
        self.log_event({
            "event_type": "outcome",
            "action": action,
            "outcome": outcome,
            "success": success,
            "details": details or {}
        })
    
    def get_session_events(self) -> list[Dict[str, Any]]:
        """Get all events from the current session."""
        return self.session_events
    
    def get_events_by_type(
        self,
        event_type: str,
        limit: int = 50
    ) -> list[Dict[str, Any]]:
        """Get events of a specific type."""
        events = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if event.get("event_type") == event_type:
                            events.append(event)
                            if len(events) >= limit:
                                break
                    except json.JSONDecodeError:
                        continue
        except IOError:
            pass
        
        return events
    
    def get_event_count(self) -> int:
        """Get total number of logged events."""
        return self.event_count
    
    def get_recent_events(
        self,
        count: int = 10
    ) -> list[Dict[str, Any]]:
        """Get the most recent events."""
        return self.session_events[-count:]
    
    def export_session_log(self, output_path: Path) -> None:
        """Export the current session log to a file."""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.session_events, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not export log: {e}")
