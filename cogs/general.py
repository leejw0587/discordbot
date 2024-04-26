import platform
import random
import json
import time
import datetime
import asyncio
import typing
import requests
import re

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
        if message.author == self.bot.user or message.author.bot:
            return

        react = ['시발', '개창', '따잇', '꺄웃', '끼얏호', '료낏짜']

        if "인생" in message.content:
            msg = random.choice(react)
            return await message.channel.send(msg)

        elif "얼굴" in message.content or "면상" in message.content:
            msg = random.choice(react)
            return await message.channel.send(msg)

        # else:
        #     if message.channel.id == 1081478211403272264:
        #         async with message.channel.typing():
        #             response = openai.ChatCompletion.create(
        #                 model="gpt-3.5-turbo",
        #                 messages=[
        #                     {"role": "system",
        #                      "content": "You are a friendly chatbot. Your name is '우지한'."},
        #                     {"role": "user", "content": message.content},
        #                 ]
        #             )
        #             botAnswer = response['choices'][0]['message']['content']
        #             return await message.channel.send(botAnswer)

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

    # @commands.hybrid_command(
    #     name="급식",
    #     description="급식을 알려줍니다."
    # )
    # async def 급식(self, context: Context, date: typing.Literal['오늘', '내일', '모레']):
    #     today = datetime.datetime.today()

    #     if date == '오늘':
    #         date = today.strftime('%Y%m%d')
    #         date_frmt = today.strftime('%Y-%m-%d')
    #     elif date == '내일':
    #         tomorrow = today + datetime.timedelta(days=1)
    #         date = tomorrow.strftime('%Y%m%d')
    #         date_frmt = tomorrow.strftime('%Y-%m-%d')
    #     elif date == '모레':
    #         tomorrow = today + datetime.timedelta(days=2)
    #         date = tomorrow.strftime('%Y%m%d')
    #         date_frmt = tomorrow.strftime('%Y-%m-%d')

    #     try:
    #         url = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=585fb4c9578b448496b2977b7e51fa24&Type=json&pIndex=1&pSize=10&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240061" + \
    #             "&MLSV_YMD=" + date
    #         response = requests.get(url)
    #         contents = response.text

    #         json_data = json.loads(contents)
    #         json_data = json_data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']

    #         message = json_data.split("<br/>")

    #         embed = discord.Embed(
    #             title=f"`{date_frmt}` 급식 정보",
    #             description="\n".join(message),
    #             color=discord.Color.greyple()
    #         )
    #         await context.send(embed=embed)
    #     except:
    #         embed = discord.Embed(
    #             title="Error!",
    #             description=f"`{date_frmt}`의 급식 정보를 찾을 수 없습니다.",
    #             color=discord.Color.red()
    #         )
    #         await context.send(embed=embed)

    @commands.hybrid_command(
        name="수온",
        description="한강 수온을 알려줍니다."
    )
    async def 수온(self, context: Context):
        url = "http://openapi.seoul.go.kr:8088/79616975466c656532375648526c4c/json/WPOSInformationTime/1/5/"
        response = requests.get(url)
        contents = response.text

        json_data = json.loads(contents)
        temp = json_data['WPOSInformationTime']['row'][4]['W_TEMP']
        date = json_data['WPOSInformationTime']['row'][4]['MSR_DATE']

        tempInt = float(temp)
        if tempInt <= 10:
            infoMsg = "차갑네요."
        elif tempInt <= 16:
            infoMsg = "조금 차갑네요."
        elif tempInt <= 26:
            infoMsg = "미지근하네요."
        elif tempInt >= 27:
            infoMsg = "따뜻하네요."
        else:
            infoMsg = ""

        embed = discord.Embed(
            title="현재 한강 수온",
            description=f"**온도: {temp}°C**\n{infoMsg}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1070947782472503296/1091948893824110662/istockphoto-481251608-612x612.jpg")
        embed.timestamp = datetime.datetime.utcnow()
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
