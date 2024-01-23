import datetime
import random

import discord
from discord.ext import commands, tasks


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_change_task.start()
        self.update_special_mayor.start()


    @tasks.loop(seconds=20)
    async def presence_change_task(self):
        await self.bot.wait_until_ready()
        game = discord.Game(f"{self.bot.get_guild(730269755432239116).member_count}人を監視中")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


    @tasks.loop(hours=24)
    async def update_special_mayor(self):
        """
        1, Scorpius 2, Derpy, 3, Jerry
        :return:
        """
        await self.bot.wait_until_ready()
        mayor_data_all = await self.bot.db_select("special")
        mayor_data = mayor_data_all[0]

        def convert_to_int_and_datetime(lst):
            time_S = f"{lst[1]} {lst[2]}"
            converted_list = [int(lst[0]), datetime.datetime.strptime(time_S, "%Y-%m-%d %H:%M:%S")]
            return converted_list

        mayor_data = convert_to_int_and_datetime(mayor_data)
        mayor = ["Scorpius", "Derpy", "Jerry"]

        embed_str = ""
        ch = self.bot.get_channel(937231584006926396)
        embed_element = await ch.fetch_message(937561440859082862)
        if mayor_data[1] <= datetime.datetime.now():
            embed_str += f"現在のSpecial mayor: {mayor[mayor_data[0]]}\n\n終了時刻: {mayor_data[1] + datetime.timedelta(days=5) + datetime.timedelta(hours=4)} (JST)\n\n----------------------------\n\n"
            mayor_data[1] = mayor_data[1] + datetime.timedelta(days=41, hours=8)
            mayor_data[0] += 1
            if mayor_data[0] > 2:
                mayor_data[0] = 0
            message = f"{mayor_data[0]} {mayor_data[1]}"
            await self.bot.db_insert("special", message)

        embed_str += f"次回のSpecial mayor: {mayor[mayor_data[0]]}\n\n開始時刻: {mayor_data[1].strftime('%Y/%m/%d %H:%M:%S')} (JST)\n\n ----------- \n\n"
        mayor_data[1] = mayor_data[1] + datetime.timedelta(days=41, hours=8)
        mayor_data[0] += 1
        if mayor_data[0] > 2:
            mayor_data[0] = 0

        embed_str += f"次々回のSpecial mayor: {mayor[mayor_data[0]]}\n\n開始時刻: {mayor_data[1].strftime('%Y/%m/%d %H:%M:%S')} (JST)"

        color = [0x126132, 0x82fc74, 0xfea283, 0x009497, 0x08fad4, 0x6ed843, 0x8005c0]
        await embed_element.edit(embed=discord.Embed(description=embed_str, color=random.choice(color)))


async def setup(bot):
    await bot.add_cog(Loops(bot))
