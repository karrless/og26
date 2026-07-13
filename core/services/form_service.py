from dataclasses import dataclass

from core.services.sheets_service import SheetsService
from core.services.vk_resolver import resolve_vk_id


class FormValidationError(Exception):
    pass


@dataclass
class FormData:
    fio: str
    vk_id: int
    number: str
    yes_no: str
    direction: str


class FormService:
    def __init__(self, sheets_service: SheetsService):
        self.sheets_service = sheets_service

    @staticmethod
    def validate_fio(text: str) -> str:
        text = text.strip()
        if len(text.split()) < 2:
            raise FormValidationError("Введите ФИО полностью (имя и фамилия).")
        return text

    @staticmethod
    async def validate_vk_link(text: str) -> int:
        vk_id = await resolve_vk_id(text)
        if vk_id is None:
            raise FormValidationError("Не удалось распознать ссылку/ID ВКонтакте, попробуйте ещё раз.")
        return vk_id

    @staticmethod
    def validate_unique_number(text: str) -> str:
        text = text.strip()
        if not text:
            raise FormValidationError("Номер не может быть пустым.")
        return text  # TODO: реальная валидация формата

    async def submit(self, data: FormData) -> bool:
        return await self.sheets_service.append_form(
            direction=data.direction,
            fio=data.fio,
            vk_id=data.vk_id,
            number=data.number,
            yes_no=data.yes_no,
        )