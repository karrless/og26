from dataclasses import dataclass


@dataclass
class Button:
    text: str
    action: str


YES_NO_KEYBOARD = [
    [Button("Да", "form:yes_no:yes"), Button("Нет", "form:yes_no:no")],
]

DIRECTIONS: list[str] = []