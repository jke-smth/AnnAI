from enum import Enum
from typing import Callable, Dict, List, Optional, Any


class PanelState(Enum):
    IDLE = "idle"
    INIT_TRIGGER = "init_trigger"
    INIT_STAGE = "init_stage"
    END_TRIGGER = "end_trigger"
    END_STAGE = "end_stage"
    STOPPED = "stopped"

# panel state to color map

# my colors:
# - idle: gray
# - init_trigger: ffee83
# - init_stage: f0b541
# - end_trigger: ffc2a1
# - end_stage: ffae70
# - stopped: black

# Todo: need to change these to qcolor names or hex strings with # prefix, and update the default_color_map accordingly. For now, we can assume the LED widget can handle these color formats directly.
default_color_map = {
    PanelState.IDLE: "#808080",
    PanelState.INIT_TRIGGER: "#ffee83",
    PanelState.INIT_STAGE: "#f0b541",
    PanelState.END_TRIGGER: "#ffc2a1",
    PanelState.END_STAGE: "#92e8c0",
    PanelState.STOPPED: "#e64539",
}


class BaseStateMachine:
    """A small state machine with observer support and color mapping.

    Observers are callables that accept a single `PanelState` argument.
    Use `attach_led()` to bind a widget that exposes `set_color(color_str)`.
    """

    def __init__(self, logger: Any = None, color_map: Optional[Dict[PanelState, str]] = None):
        self.state = PanelState.IDLE
        self.logger = logger
        self._observers: List[Callable[[PanelState], None]] = []
        # default color mapping (can be overridden by passing color_map)
        self._color_map: Dict[PanelState, str] = color_map or default_color_map 
        

    def _log(self, msg: str) -> None:
        if self.logger:
            try:
                self.logger.info(msg)
            except Exception:
                pass

    def advance(self) -> None:
        if self.state == PanelState.IDLE:
            self._set_state(PanelState.INIT_TRIGGER)

        elif self.state == PanelState.INIT_TRIGGER:
            self._set_state(PanelState.INIT_STAGE)

        elif self.state == PanelState.INIT_STAGE:
            self._set_state(PanelState.END_TRIGGER)

        elif self.state == PanelState.END_TRIGGER:
            self._set_state(PanelState.END_STAGE)

        elif self.state == PanelState.END_STAGE:
            self._set_state(PanelState.IDLE)
        
    def stop(self) -> None:
        self._set_state(PanelState.STOPPED)

    def reset(self) -> None:
        self._set_state(PanelState.IDLE)

    def _set_state(self, new_state: PanelState) -> None:
        old = self.state
        self.state = new_state
        self._log(f"{old.value} → {new_state.value}")
        self._notify_observers(new_state)

    def trigger(self) -> bool:
        if self.state != PanelState.IDLE:
            self._log("Invalid trigger")
            return False

        self.advance()
        return True

    def get_state(self) -> PanelState:
        return self.state

    # Observer management
    def register_observer(self, callback: Callable[[PanelState], None]) -> None:
        if callback not in self._observers:
            self._observers.append(callback)

    def unregister_observer(self, callback: Callable[[PanelState], None]) -> None:
        try:
            self._observers.remove(callback)
        except ValueError:
            pass

    def _notify_observers(self, state: PanelState) -> None:
        for cb in list(self._observers):
            try:
                cb(state)
            except Exception:
                # observer errors should not break the state machine
                pass

    # Color mapping utilities
    def get_color_for_state(self, state: Optional[PanelState] = None) -> str:
        s = state or self.state
        return self._color_map.get(s, "gray")

    def set_color_map(self, color_map: Dict[PanelState, str]) -> None:
        self._color_map = dict(color_map)

    def attach_led(self, led_widget: Any, transform: Optional[Callable[[str], str]] = None) -> Callable[[], None]:
        """Attach a LED-like widget to the machine.

        The `led_widget` must implement `set_color(color_str)`.
        Returns an `unregister()` callable to detach the widget.
        """

        def _observer(state: PanelState) -> None:
            color = self.get_color_for_state(state)
            if transform:
                try:
                    color = transform(color)
                except Exception:
                    pass
            try:
                # prefer public API `set_color` to update the widget
                if hasattr(led_widget, "set_color"):
                    led_widget.set_color(color)
            except Exception:
                pass

        self.register_observer(_observer)

        def _unregister() -> None:
            self.unregister_observer(_observer)

        # Initialize LED to current state color
        try:
            _observer(self.state)
        except Exception:
            pass

        return _unregister


class PanelStateMachine(BaseStateMachine):
    """Convenience subclass for panel-specific machines.

    Example usage:
      sm = PanelStateMachine(panel_name="chat")
      unregister = sm.attach_led(my_led_widget)
"""

    def __init__(self, panel_name: str = "panel", logger: Any = None, color_map: Optional[Dict[PanelState, str]] = None):
        super().__init__(logger=logger, color_map=color_map)
        self.panel_name = panel_name

    def __repr__(self) -> str:
        return f"<PanelStateMachine {self.panel_name} state={self.state.value}>"
