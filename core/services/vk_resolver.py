import re
from typing import Optional

from vkbottle.api import API

from config import VK_TOKEN

_api = API(VK_TOKEN)
_LINK_RE = re.compile(r"vk\.com/([a-zA-Z0-9_.]+)")


async def resolve_vk_id(raw: str) -> Optional[int]:
    raw = raw.strip()

    if raw.isdigit():
        return int(raw)

    match = _LINK_RE.search(raw)
    screen_name = match.group(1) if match else raw.lstrip("@")

    if screen_name.startswith("id") and screen_name[2:].isdigit():
        return int(screen_name[2:])

    result = await _api.utils.resolve_screen_name(screen_name)
    if result is not None and result.type and result.type.value == "user":
        return result.object_id
    return None