import disnake
from disnake.ext import commands
import os

from utils.console.logger_util import logger
from utils.discord.role_management.role_check_util import check_trust_access

link_file_path = "link/link.txt"

def format_link(link: str) -> str:
    link = link.strip()
    if not link.startswith(("http://", "https://")):
        link = "https://" + link
    return link


status_link = "https://example.com"
if os.path.exists(link_file_path):
    with open(link_file_path, "r", encoding="utf-8") as f:
        status_link = format_link(f.read())

class VerifyButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Verify",
        style=disnake.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify(self, button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(
            description="**This server is protected by Double Counter, anti alt account and VPN bot. You must verify to access the server.**",
            color=disnake.Color.from_rgb(104, 157, 197)
        )

        embed.add_field(
            name="Server",
            value=inter.guild.name if inter.guild else "Unknown",
            inline=False
        )
        embed.add_field(
            name="Status",
            value=f"[Click me to verify!]({status_link})",
            inline=True
        )
        embed.add_field(
            name="By clicking, you accept our",
            value="[Privacy policy](https://docs.doublecounter.gg/legal)",
            inline=True
        )
        embed.add_field(
            name="Need help?",
            value="[Join our support server](https://discord.gg/doublecounter)",
            inline=False
        )

        embed.set_footer(
            text=f"Click the blue link to verify - https://doublecounter.gg/invite to invite Double Counter"
        )

        await inter.response.send_message(
            "A verification link will be sent shortly below. Please click it to verify.",
            ephemeral=True
        )

        await inter.followup.send(embed=embed, ephemeral=True)

class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VerifyButton())

    @commands.slash_command(
        name="panel",
        description="Send a verification panel/button in that channel"
    )
    async def panel(self, inter: disnake.ApplicationCommandInteraction):
        if not await check_trust_access(inter):
            return

        embed = disnake.Embed(
            description="Click the green button below to verify",
            color=disnake.Color.from_rgb(52, 235, 131)
        )

        await inter.channel.send(
            embed=embed,
            view=VerifyButton()
        )
        await inter.response.send_message("Panel sent!", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        try:
            embed = disnake.Embed(
                description="**This server is protected by Double Counter, anti alt account and VPN bot. You must verify to access the server.**",
                color=disnake.Color.from_rgb(104, 157, 197)
            )

            embed.add_field(
                name="Server",
                value=member.guild.name,
                inline=False
            )
            embed.add_field(
                name="Status",
                value=f"[Click me to verify!]({status_link})",
                inline=True
            )
            embed.add_field(
                name="By clicking, you accept our",
                value="[Privacy policy](https://docs.doublecounter.gg/legal)",
                inline=True
            )
            embed.add_field(
                name="Need help?",
                value="[Join our support server](https://discord.gg/doublecounter)",
                inline=False
            )

            embed.set_footer(
                text=f"Click the blue link to verify - https://doublecounter.gg/invite to invite Double Counter"
            )

            await member.send(embed=embed)
        except Exception as e:
            logger.warning(f"Failed to send verification DM to {member}: {e}")

    @commands.slash_command(
        name="change_link",
        description="Change the verification link"
    )
    async def change_link(self, inter: disnake.ApplicationCommandInteraction, link: str):
        if not await check_trust_access(inter):
            return

        global status_link
        status_link = format_link(link)

        os.makedirs(os.path.dirname(link_file_path), exist_ok=True)

        with open(link_file_path, "w", encoding="utf-8") as f:
            f.write(status_link)

        await inter.response.send_message(f"Status link updated to: {status_link}", ephemeral=True)

def setup(bot):
    bot.add_cog(VerifyCog(bot))
