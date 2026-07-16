import re
from typing import Optional

from vkbottle.api import API
from vkbottle_types.codegen.objects import UsersFields, UsersUserFull

from config import VK_API1

_api = API(VK_API1)

_LINK_RE = re.compile(
    r"(?:https?://)?(?:www\.)?vk\.(?:com|ru)/([a-zA-Z0-9_.]+)"
)
_DEFAULT_DOMAIN_RE = re.compile(r"^id\d+$")


async def resolve_vk_id(raw: str) -> Optional[str]:
    raw = raw.strip()
    match = _LINK_RE.search(raw)
    value = (match.group(1) if match else raw).lstrip("@").strip("/")

    if value.startswith("id") and value[2:].isdigit():
        value = value[2:]

    if not value.isdigit():
        result = await _api.utils.resolve_screen_name(value)

        if not isinstance(result, list) and result is not None:
            if result.type and result.type.value == "user":
                value = str(result.object_id)

    users = await _api.users.get(user_ids=[value], fields=[UsersFields.DOMAIN])

    if not users:
        return None

    user = users[0]
    domain = user.domain

    if domain and not _DEFAULT_DOMAIN_RE.match(domain):
        return f"@{domain}"
    return f"@id{user.id}"

async def get_vk_user(vk_id: int) -> Optional[UsersUserFull]:
    users = await _api.users.get(
        user_ids=[vk_id],
        fields=[
            UsersFields.DOMAIN,
        ]
    )

    if not users:
        return None

    return users[0]