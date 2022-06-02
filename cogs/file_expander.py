from discord.ext import commands
import os
import pdf2image
import discord


class FileExpander(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments is None:
            return
        for attachment in message.attachments:
            if attachment.content_type != "application/pdf":
                continue
            await attachment.save(f"{message.id}.pdf")
            raw_images = pdf2image.convert_from_path(f"{message.id}.pdf")
            all_images = [raw_images[idx:idx + 10] for idx in range(0,len(raw_images), 10)]
            count = 1
            for image_container in all_images:
                files = []
                for image in image_container:
                    image.save(f"{message.id}-{count}.jpg")
                    files.append(discord.File(f"{message.id}-{count}.jpg"))
                    os.remove(f"{message.id}-{count}.jpg")
                    count += 1
                await message.channel.send(content=f"{count-len(files)}~{count-1}ページ", files=files)
            os.remove(f"{message.id}.pdf")


def setup(bot):
    bot.add_cog(FileExpander(bot))
