from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.content.texts import FORM_BUTTON, CANCEL_BUTTON, FAQ_BUTTON, BACK_BUTTON, OWN_QUESTION_BUTTON

MAX_ROWS_DEFAULT = 10
MAX_ROWS_INLINE = 6
MAX_BUTTONS_PER_ROW = 4


class ButtonColor(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    POSITIVE = "positive"
    NEGATIVE = "negative"


@dataclass
class Button:
    text: str
    action: str
    color: ButtonColor | None = None


MENU_KEYBOARD = [
    [Button(FORM_BUTTON, "form:start", ButtonColor.POSITIVE)],
    [Button(FAQ_BUTTON, "faq:start")]
]

CANCEL_KEYS = [
    Button(CANCEL_BUTTON, "cancel", ButtonColor.SECONDARY)
]

BACK_KEYS = [
    Button(BACK_BUTTON, "back", ButtonColor.SECONDARY)
]

OWN_QUESTION_KEYS = [
    Button(OWN_QUESTION_BUTTON, 'own_question', ButtonColor.SECONDARY)
]

YES_NO_KEYBOARD = [
    [Button("Да", "form:yes_no:Да", ButtonColor.PRIMARY),
     Button("Нет", "form:yes_no:Нет", ButtonColor.PRIMARY)],
]

DIRECTIONS: dict[str, str] = {
    # ГРФ
    'Геологические технологии': 'Геологические технологии',
    # ГФ
    'Экологическое': 'Экологическое',
    'Техносферная безопасность': 'Техносферная безопасность',
    'Технологии горного производства (Горные работы)': 'Горные работы',
    # ИБИО
    'Информационное': 'Информационное',
    # ФПМС
    'Автоматизация': 'Автоматизация',
    'Химические технологии': 'Химические технологии',
    # НГФ
    'Нефтегазовые технологии': 'Нефтегазовые технологии',
    # ММФ
    'Технологии приборостроения': 'Технологии приборостроения',
    'Машиностроение': 'Машиностроение',
    'Метрологическое': 'Метрологическое',
    'Технология художественной обработки материалов': 'Худож. обработка материалов',
    'Транспортно-технологическое': 'Транспортно-технологическое',
    # СФ
    'Архитектура': 'Архитектура',
    'Кадастровое': 'Кадастровое',
    'Строительство': 'Строительство',
    'Геодезическое': 'Геодезическое',
    'Технологии строительства': 'Технологии строительства',
    # ЭФ
    'Управление в технических системах': 'Управление в тех. системах',
    'Отраслевая экономика': 'Отраслевая экономика',
    'Управление и организация в МСК': 'Управление и организация в МСК',
    # ЭНФ
    'Радиоэлектроника': 'Радиоэлектроника',
    'Электроэнергетическое': 'Электроэнергетическое',
    # Материалы/Обогащение/Тех.обеспечение
    'Технологии материалов': 'Технологии материалов',
    'Технологии горного производства (Экология. Обогащение)': 'Горное произв. (Экология)',
    'Технологии горного производсива (технологическое обеспечение горных работ)': 'Горное произв. (тех. обеспечение)',
}

for _full, _alias in DIRECTIONS.items():
    assert len(_alias) <= 40, f"Алиас длиннее 40 символов: {_alias!r} (для {_full!r})"