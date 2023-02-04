import platform
import random
import json
import time
import datetime
import asyncio
import typing

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="실행 가능한 모든 커맨드를 표시합니다."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="명령어 목록: ", color=0x9C84EF)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="봇의 레이턴시를 확인합니다.",
    )
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="name",
        description="봇의 닉네임을 설정합니다."
    )
    async def name(self, context: Context, name: str) -> None:
        me = context.guild.me
        name = f"[🔧] {name}"
        await me.edit(nick=name)

        embed = discord.Embed(
            title="이름",
            description=f"봇의 이름을 `{name}`(으)로 설정하였습니다.",
            color=0x9C84EF
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
