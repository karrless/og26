from pathlib import Path

import openpyxl

from core.db.repositories import RoomAssignmentRepository

ROOMS_DIR = Path(__file__).parent / "rooms"


def _read_xlsx(path: Path) -> list[tuple[int, str, str]]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = wb.active
    result = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # пропускаем заголовок
        if not row or row[1] is None:
            continue
        _, cipher, comfort, room_number = row[:4]
        result.append((int(cipher), str(comfort).strip(), str(room_number).strip()))
    return result


async def seed_rooms(session) -> int:
    all_entries: dict[int, tuple[str, str]] = {}

    for path in sorted(ROOMS_DIR.glob("*.xlsx")):
        for cipher, comfort, room_number in _read_xlsx(path):
            if cipher in all_entries:
                print(f"Дубликат шифра {cipher} (файл {path.name})")
                continue
            all_entries[cipher] = (comfort, room_number)

    repo = RoomAssignmentRepository(session)
    await repo.clear_all()
    for cipher, (comfort, room_number) in all_entries.items():
        await repo.create(cipher=cipher, comfort=comfort, room_number=room_number)
    await session.commit()

    return len(all_entries)