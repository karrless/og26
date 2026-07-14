from dataclasses import dataclass
from typing import Callable, Generic, Sequence, TypeVar

from vkbottle import KeyboardButtonColor

from core.content.keyboards import Button, MAX_ROWS_DEFAULT

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: Sequence[T]
    page: int
    total_pages: int
    has_prev: bool
    has_next: bool


class Paginator(Generic[T]):
    def __init__(self, items: Sequence[T], columns: int = 1, reserved_rows: int = 2, max_rows: int = MAX_ROWS_DEFAULT):
        """reserved_rows — сколько строк уйдёт под навигацию + (опционально) отмену,
        считает вызывающий код (обычно 1 под нав-кнопки + 1 под отмену)."""
        self.items = list(items)
        self.columns = columns
        rows_for_items = max(1, max_rows - reserved_rows)
        self.page_size = rows_for_items * columns
        self.total_pages = max(1, (len(self.items) + self.page_size - 1) // self.page_size)

    def get_page(self, page: int) -> Page[T]:
        page = max(1, min(page, self.total_pages))
        start = (page - 1) * self.page_size
        return Page(
            items=self.items[start:start + self.page_size],
            page=page,
            total_pages=self.total_pages,
            has_prev=page > 1,
            has_next=page < self.total_pages,
        )


def build_paginated_keyboard(
        page: Page[T],
        to_button: Callable[[T], Button],

        prefix: str,
        columns: int = 1,

) -> list[list[Button]]:
    rows: list[list[Button]] = []
    row: list[Button] = []
    for item in page.items:
        row.append(to_button(item))
        if len(row) == columns:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    nav: list[Button] = []
    if page.has_prev:
        nav.append(Button("« Назад", f"{prefix}:page:{page.page - 1}", KeyboardButtonColor.SECONDARY))
    if page.has_next:
        nav.append(Button("Вперёд »", f"{prefix}:page:{page.page + 1}", KeyboardButtonColor.SECONDARY))
    if nav:
        rows.append(nav)
    return rows