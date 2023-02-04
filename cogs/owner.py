import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="load",
        description="cog를 로드합니다. (관리자 전용)",
    )
    @app_commands.describe(cog="로드할 cog 이름")
    @checks.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not load the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Load",
            description=f"Successfully loaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="cog를 언로드합니다. (관리자 전용)",
    )
    @app_commands.describe(cog="언로드할 cog 이름")
    @checks.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not unload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Unload",
            description=f"Successfully unloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="cog를 리로드합니다. (관리자 전용)",
    )
    @app_commands.describe(cog="리로드할 cog 이름")
    @checks.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not reload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Reload",
            description=f"Successfully reloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="봇을 강제종료합니다. (관리자 전용)",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="입력한 메시지를 봇이 대신 말해줍니다. (관리자 전용)",
    )
    @app_commands.describe(message="보낼 메시지")
    @checks.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.channel.send(message)

    @commands.hybrid_command(
        name="embed",
        description="봇이 embed 형태로 메시지를 보내줍니다. (관리자 전용)",
    )
    @app_commands.describe(message="보낼 메시지")
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(
            description=message,
            color=0x9C84EF
        )
        await context.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
