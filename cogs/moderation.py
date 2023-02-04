import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager, log


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="nick",
        description="유저의 닉네임을 서버 형식에 맞게 변경합니다. (관리자 전용)",
    )
    @checks.is_owner()
    @app_commands.describe(user="대상 유저", nickname="변경할 닉네임")
    async def nick(self, context: Context, user: discord.User, *, nickname: str = None) -> None:
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        result = []

        for i in nickname:
            for j in range(2):
                result.append(i)

        nickname = ''.join(result)

        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="닉네임 변경 완료!",
                description=f"`{member}`의 닉네임을 `{nickname}`(으)로 설정하였습니다!",
                color=discord.Color.green()
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="오류가 발생하였습니다. 다시 시도해주세요.",
                color=discord.Color.red()
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="purge",
        description="메시지를 청소합니다. (관리자 전용)"
    )
    @checks.is_owner()
    async def purge(self, context: Context, amount: int):
        await context.send(f"`{amount}`개의 메시지를 삭제합니다...", delete_after=5)
        await context.channel.purge(limit=amount+1)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
