import disnake
from disnake import ApplicationCommandInteraction
from config.config import ADMIN


def has_trust_user(member: disnake.Member) -> bool:
    return member.id == ADMIN


async def check_trust_access(inter: ApplicationCommandInteraction) -> bool:
    if not has_trust_user(inter.author):
        await inter.response.send_message(
            "У вас нет доступа к данной команде.",
            ephemeral=True
        )
        return False
    return True
