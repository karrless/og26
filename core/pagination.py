from dataclasses import dataclass
from typing import Callable, Generic, Sequence, TypeVar

from core.content.keyboards import Button

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: Sequence[T]
    page: int
    total_pages: int
    has_prev: bool
    has_next: bool


class Paginator(Generic[T]):
    def __init__(self, items: Sequence[T], page_size: int = 6):
        self.items = list(items)
        self.page_size = page_size
        self.total_pages = max(1, (len(self.items) + page_size - 1) // page_size)

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
        nav.append(Button("« Назад", f"{prefix}:page:{page.page - 1}"))
    if page.has_next:
        nav.append(Button("Вперёд »", f"{prefix}:page:{page.page + 1}"))
    if nav:
        rows.append(nav)
    return rows