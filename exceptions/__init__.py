from discord.ext import commands


class UserNotOwner(commands.CheckFailure):
    def __init__(self, message="해당 유저는 관리자가 아닙니다!"):
        self.message = message
        super().__init__(self.message)
