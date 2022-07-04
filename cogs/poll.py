from discord.ext import commands
import discord


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = [
            "\U00000030\U0000fe0f\U000020e3",
            "\U00000031\U0000fe0f\U000020e3",
            "\U00000032\U0000fe0f\U000020e3",
            "\U00000033\U0000fe0f\U000020e3",
            "\U00000034\U0000fe0f\U000020e3",
            "\U00000035\U0000fe0f\U000020e3",
            "\U00000036\U0000fe0f\U000020e3",
            "\U00000037\U0000fe0f\U000020e3",
            "\U00000038\U0000fe0f\U000020e3",
            "\U00000039\U0000fe0f\U000020e3",
            "\U0001f51f",
            "\U0001f1e6",
            "\U0001f1e7",
            "\U0001f1e8",
            "\U0001f1e9",
            "\U0001f1ea",
            "\U0001f1eb",
            "\U0001f1ec",
            "\U0001f1ed",
            "\U0001f1ee"
        ]

    @commands.command()
    async def poll(self, ctx, title=None, *args):
        if title is None:
            return await ctx.send("タイトルを指定してください。")
        if len(args) > 20:
            return await ctx.send("選択肢が多すぎます。")
        if len(args) == 0:
            args = [title]
        description = "".join([f"{n}: {arg}\n" for n, arg in zip(self.reactions[:len(args)], args)])
        msg = await ctx.send(embed=discord.Embed(title=title, description=description, colour=discord.Colour.green()))
        for react in self.reactions[:len(args)]:
            await msg.add_reaction(react)   

def setup(bot):
    bot.add_cog(Poll(bot))
