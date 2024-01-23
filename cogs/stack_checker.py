import traceback
from datetime import datetime

import discord
from discord.ext import commands

"""Stackを計算するコマンド"""


class StackCalc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cs(self, ctx, amount):
        try:
            try:
                if int(amount):
                    if self.bot.stack_check_reverse(amount) == 0:
                        await ctx.send(f"入力した値が0または不正な値です。")
                        return
                    else:
                        await ctx.send(f"{amount}はスタック表記で{self.bot.stack_check_reverse(amount)}です。")
            except ValueError:
                if self.bot.stack_check(amount) == 0:
                    await ctx.send(f"入力した値が0または不正な値です。")
                    return
                else:
                    await ctx.send(f"{amount}は整数値で{self.bot.stack_check(amount)}です。")

        except Exception as e:
            orig_error = getattr(e, "original", e)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            error_message = f'```{error_msg}```'
            ch = self.bot.get_channel(628807266753183754)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = discord.Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:on_check_time_loop\ntime:{time}\nuser:None')
            await ch.send(embed=embed)


def setup(bot):
    bot.add_cog(StackCalc(bot))
