from discord.ext import commands
import os
import img2pdf
from PIL import Image
import discord


class ImgToPDF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def img2pdf(self, ctx):
        if len(ctx.message.attachments) == 0:
            return await ctx.send("コマンドと一緒に画像を送信してください。")
        for attachment in ctx.message.attachments:
            if "image" not in attachment.content_type:
                continue
            msg = await ctx.send("画像変換中・・・")
            await attachment.save(str(ctx.message.id) + "." + attachment.filename.split(".")[-1])
            with open(f"{ctx.message.id}.pdf","wb") as f:
                f.write(img2pdf.convert(str(ctx.message.id) + "." + attachment.filename.split(".")[-1]))
            await msg.delete()
            await ctx.send(files=[discord.File(str(ctx.message.id) + ".pdf")])
            os.remove(str(ctx.message.id) + "." + attachment.filename.split(".")[-1])
            os.remove(str(ctx.message.id) + ".pdf")


def setup(bot):
    bot.add_cog(ImgToPDF(bot))
