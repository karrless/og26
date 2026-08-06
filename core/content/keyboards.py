from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.content.texts import FORM_BUTTON, CANCEL_BUTTON, FAQ_BUTTON, BACK_BUTTON, OWN_QUESTION_BUTTON, FAQ_ASK_VK_URL, \
    TG_OWN_QUESTION_BUTTON

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
    action: str = ""
    color: ButtonColor | None = None
    url: Optional[str] = None


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

ASK_QUESTION_LINK_KEYS = [
    Button(TG_OWN_QUESTION_BUTTON, url=FAQ_ASK_VK_URL)
]

YES_NO_KEYBOARD = [
    [Button("Да", "form:yes_no:Да", ButtonColor.PRIMARY),
     Button("Нет", "form:yes_no:Нет", ButtonColor.PRIMARY)],
]

DIRECTIONS: dict[str, str] = {
    # ГРФ
    'Геологические технологии': 'Геологические технологии',
    # ГФ
    'Экология и природопользование': 'Экология',
    'Техносферная безопасность': 'Техносферная безопасность',
    'Технологии горного производства (Горные работы)': 'Горные работы',
    # ИБИО
    'Информационные технологии': 'Информационное',
    # ФПМС
    'Автоматизация': 'Автоматизация',
    'Химические технологии': 'Химические технологии',
    # НГФ
    'Нефтегазовые технологии': 'Нефтегазовые технологии',
    # ММФ
    'Технологии приборостроения': 'Технологии приборостроения',
    'Машиностроение': 'Машиностроение',
    'Метрология': 'Метрология',
    'Технология художественной обработки материалов': 'Худож. обработка материалов',
    'Транспортные технологии': 'Транспортные технологии',
    # СФ
    'Архитектура': 'Архитектура',
    'Землеустройство и кадастры ': 'Землеустройство и кадастры ',
    'Строительство': 'Строительство',
    'Инженерная геодезия ': 'Инженерная геодезия ',
    'Технологии строительства': 'Технологии строительства',
    # ЭФ
    'Системный анализ и управление': 'Системный анализ и управление',
    'Отраслевая экономика': 'Отраслевая экономика',
    'Управление и организация в МСК': 'Управление и организация в МСК',
    # ЭНФ
    'Электроника и радиоэлектронные системы': 'Электроника',
    'Электроэнергетика и теплоэнергетика': 'Электро- и теплоэнергетика',
    # Материалы/Обогащение/Тех.обеспечение
    'Технологии материалов': 'Технологии материалов',
    'Технологии горного производства (Экология. Обогащение)': 'Горное произв. (Экология)',
    'Технологии горного производсива (технологическое обеспечение горных работ)': 'Горное произв. (тех. обеспечение)',
}

for _full, _alias in DIRECTIONS.items():
    assert len(_alias) <= 40, f"Алиас длиннее 40 символов: {_alias!r} (для {_full!r})"