from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

MOVE_KEYS = {
    # num keys
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),

    # WASD keys
    tcod.event.K_w: (0, -1),
    tcod.event.K_s: (0, 1),
    tcod.event.K_a: (-1, 0),
    tcod.event.K_d: (1, 0)
}


class EventHandler(tcod.event.EventDispatch[Action]):

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = MovementAction(dx, dy)

        # No valid key was pressed
        return action

    def __str__(self) -> str:
        return "EventHandler"
