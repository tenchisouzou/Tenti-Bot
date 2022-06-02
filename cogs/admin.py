import asyncio
import io
import os
import subprocess
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands
import discord


def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self._load_cogs()
        print("loaded")

    def _load_cogs(self):
        for cog in os.listdir("./cogs"):
            if not cog.endswith(".py") or cog == "admin.py":
                continue
            try:
                self.bot.load_extension(f"cogs.{cog[:-3]}")
            except discord.ExtensionError:
                self.bot.reload_extension(f"cogs.{cog[:-3]}")

    async def cog_check(self, ctx):
        return ctx.author.is_owner()

    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            result = await self.bot.loop.run_in_executor(None, process.communicate)
        return [output.decode() for output in result]

    @commands.command(pass_context=True, hidden=True)
    async def eval(self, ctx, *, body: str):
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }
        env.update(globals())
        body = cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except Exception:
                pass
            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")

    @commands.command(name="reload")
    async def _reload(self, ctx):
        msg = await ctx.send("reloading")
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.bot.unload_extension(f"cogs.{cog[:-3]}")
                except discord.ExtensionError:
                    pass
                self._load_cogs()
        await msg.edit(content="reloaded")
        print("--------------------------------------------------")


def setup(bot):
    bot.add_cog(Admin(bot))
