import asyncio
from dataclasses import dataclass
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

BLOCK_WIDTH = 4          # ФИО, ID, НОМЕР, Да/Нет
HEADER_ROW = 1
DATA_START_ROW = 3       # 1 - направление, 2 - подзаголовки, дальше данные


@dataclass
class Block:
    sheet: gspread.Worksheet
    start_col: int  # 1-based


class SheetsService:
    def __init__(self):
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
        self._client = gspread.authorize(creds)
        self._spreadsheet = self._client.open_by_key(SPREADSHEET_ID)

    def _find_block_sync(self, direction: str) -> Optional[Block]:
        for sheet in self._spreadsheet.worksheets():
            header_row = sheet.row_values(HEADER_ROW)
            for idx, value in enumerate(header_row, start=1):
                if value.strip() == direction.strip():
                    return Block(sheet=sheet, start_col=idx)
        return None

    def _find_empty_row_sync(self, block: Block) -> int:
        col_values = block.sheet.col_values(block.start_col)
        row = DATA_START_ROW
        while row <= len(col_values) and col_values[row - 1].strip():
            row += 1
        return row

    def _append_sync(self, direction: str, fio: str, vk_id: int, number: str, yes_no: str) -> bool:
        block = self._find_block_sync(direction)
        if block is None:
            return False
        row = self._find_empty_row_sync(block)
        start_a1 = gspread.utils.rowcol_to_a1(row, block.start_col)
        end_a1 = gspread.utils.rowcol_to_a1(row, block.start_col + BLOCK_WIDTH - 1)
        block.sheet.update(f"{start_a1}:{end_a1}", [[fio, str(vk_id), number, yes_no]])
        return True

    async def append_form(self, direction: str, fio: str, vk_id: int, number: str, yes_no: str) -> bool:
        return await asyncio.to_thread(self._append_sync, direction, fio, vk_id, number, yes_no)

    def _find_cipher_sync(self, cipher: str) -> bool:
        for sheet in self._spreadsheet.worksheets():
            header_row = sheet.row_values(HEADER_ROW)
            block_starts = [idx for idx, value in enumerate(header_row, start=1) if value.strip()]
            for start_col in block_starts:
                number_col = start_col + 2  # ФИО, ID, НОМЕР, Да/Нет
                for value in sheet.col_values(number_col)[DATA_START_ROW - 1:]:
                    if value.strip() == cipher.strip():
                        return True
        return False

    async def find_cipher(self, cipher: str) -> bool:
        return await asyncio.to_thread(self._find_cipher_sync, cipher)