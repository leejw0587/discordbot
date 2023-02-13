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

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        react = ['시발', '개창', '따잇', '꺄웃', '끼얏호', '료낏짜']

        if "인생" in message.content:
            msg = random.choice(react)
            return await message.channel.send(msg)

        elif "얼굴" in message.content or "면상" in message.content:
            if message.author.id == 612252642734899210:  # 우지환
                msg = f"모공 {random.randint(3, 1000)}미터"
            elif message.author.id == 476971304059142145:  # 박제희
                msg = "외국인"
            elif message.author.id == 682994068103757840:  # 박경덕
                msg = "아 어쩌라고"
            elif message.author.id == 822839709109059604:  # 이동건
                msg = "강남"
            elif message.author.id == 389354491410907157:  # 정인철
                msg = f"입술 {random.randint(3, 1000)}미터"
            elif message.author.id == 424546094182039552:  # 이지원
                msg = "거인"
            else:
                msg = random.choice(react)
            return await message.channel.send(msg)

        elif "키" in message.content:
            if message.author.id == 822839709109059604:  # 이동건
                msg = "166cm"
                return await message.channel.send(msg)

        elif "몸무게" in message.content:
            if message.author.id == 822839709109059604:  # 이동건
                msg = "70kg"
                return await message.channel.send(msg)

        elif "몸매" in message.content:
            if message.author.id == 822839709109059604:  # 이동건
                msg = "166cm에 70kg"
                return await message.channel.send(msg)

        else:
            pass

    @commands.hybrid_command(
        name="help",
        description="실행 가능한 모든 커맨드를 표시합니다."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="명령어 목록: ", color=discord.Color.purple())
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
            color=discord.Color.random()
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
            color=discord.Color.gold()
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
