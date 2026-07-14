from dataclasses import dataclass

from core.content.texts import FORM_ASK_FIO, FORM_VK_FAILED, FORM_YES_NO_FAILED, FORM_NUMBER_FAILED
from core.services.sheets_service import SheetsService
from core.services.vk_resolver import resolve_vk_id


class FormValidationError(Exception):
    pass


@dataclass
class FormData:
    fio: str
    vk_id: str
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
            raise FormValidationError(FORM_ASK_FIO)
        return text

    @staticmethod
    async def validate_vk_link(text: str) -> str:
        try:
            vk_id = await resolve_vk_id(text)
        except Exception as e:
            raise FormValidationError(FORM_VK_FAILED)
        if vk_id is None:
            raise FormValidationError(FORM_VK_FAILED)
        return vk_id

    @staticmethod
    async def resolve_own_vk_id(peer_id: int) -> str:
        result = await resolve_vk_id(str(peer_id))
        return result or f"@id{peer_id}"

    @staticmethod
    async def validate_yes_no(text: str) -> str:
        text = text.strip().lower()
        if text in ['да', 'нет']:
            return text
        raise FormValidationError(FORM_YES_NO_FAILED)

    @staticmethod
    def validate_unique_number(text: str) -> str:
        text = text.strip()
        if not text:
            raise FormValidationError(FORM_NUMBER_FAILED)
        return text  # TODO: реальная валидация формата

    async def submit(self, data: FormData) -> bool:
        return await self.sheets_service.append_form(
            direction=data.direction,
            fio=data.fio,
            vk_id=data.vk_id,
            number=data.number,
            yes_no=data.yes_no,
        )