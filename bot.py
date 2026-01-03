# coding=utf-8
import asyncio
import json
import os
import random
import traceback
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

import bs4
import discord
import requests
from discord import Embed
from discord.ext import commands


class DUNGEON_BOT(commands.Bot):

    def __init__(self, prefix):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=prefix,
            help_command=None,
            intents=intents
        )

    async def setup_hook(self):
        # 起動時に1回だけ Cog をロード
        await self.load_cogs()

    async def load_cogs(self):
        for file in os.listdir("./cogs"):
        # .py 以外は除外
            if not file.endswith(".py"):
             continue

        # macOSの ._xxxx.py を除外
            if file.startswith("._"):
              continue

        # __init__.py も除外
            if file == "__init__.py":
             continue

            cog_name = file[:-3]

            try:
                await self.load_extension(f"cogs.{cog_name}")
                print(f"[OK] Loaded cogs.{cog_name}")
            except Exception:
                print(f"[NG] Failed to load cogs.{cog_name}")
                traceback.print_exc()

    async def on_ready(self):
        color = [
            0x126132, 0x82fc74, 0xfea283,
            0x009497, 0x08fad4, 0x6ed843, 0x8005c0
        ]

        channel = self.get_channel(818216385845919755)
        if channel:
            await channel.send(
                embed=discord.Embed(
                    description="起動しました",
                    color=random.choice(color)
                )
            )

        print("Ready")

    async def change_message(self, ch_id: int, msg_id: int, **kwargs) -> discord.Message:
        """メッセージを取得して編集する"""
        ch = self.get_channel(ch_id)
        msg = await ch.fetch_message(msg_id)
        content = kwargs.pop("content", msg.id)
        embed = kwargs.pop("embed", msg.embeds[0] if msg.embeds else None)
        if embed is None:
            return await msg.edit(content=content)
        else:
            return await msg.edit(content=content, embed=embed)

    async def dm_send(self, user_id: int, content) -> bool:
        """
        指定した対象にdmを送るメソッド
        :param user_id: dmを送る対象のid
        :param content: dmの内容
        :return: dmを送信できたかのbool値
        """

        try:
            user = self.get_user(int(user_id))
        except ValueError as e:
            ch = self.get_channel(628807266753183754)
            await ch.send(user_id)
        try:
            if isinstance(content, discord.Embed):
                await user.send(embed=content)
            else:
                await user.send(content)
        except Exception:
            ch = self.get_channel(769431013151473684)
            await ch.send(user.mention)
            if isinstance(content, discord.Embed):
                await ch.send(embed=content)
            else:
                await ch.send(content)
        else:
            return True

    @staticmethod
    def mcid_to_uuid(mcid) -> Union[str, bool]:
        """
        MCIDをUUIDに変換する関数
        uuidを返す
        """
        url = f"https://api.mojang.com/users/profiles/minecraft/{mcid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            try:
                player_data_dict = json.loads(soup.decode("utf-8"))
            except json.decoder.JSONDecodeError:  # mcidが存在しないとき
                return False
            uuid = player_data_dict["id"]
            return uuid
        except requests.exceptions.HTTPError:
            return False

    @staticmethod
    def uuid_to_mcid(uuid) -> str:
        """
        UUIDをMCIDに変換する関数
        mcid(\なし)を返す
        """
        url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            sorp = bs4.BeautifulSoup(res.text, "html.parser")
            player_data_dict = json.loads(sorp.decode("utf-8"))
            mcid = player_data_dict["name"]
            return mcid
        except requests.exceptions.HTTPError:
            return "Undefined"

    @staticmethod
    def stack_check(value) -> int:
        """
        [a lc + b st + c]がvalueで来ることを想定する(関数使用前に文の構造確認を取る)
        少数出来た場合、少数で計算して最後にintぐるみをして値を返す
        :param value: [a lc + b st + c]の形の価格
        :return: 価格をn個にしたもの(少数は丸め込む)
        """
        value = str(value).replace("椎名", "").lower()
        lc, st, c = 0, 0, 0
        if "lc" in value:
            lc = float(value.split("lc")[0])
            value = value.split("lc")[1]
        if "st" in value:
            st = float(value.split("st")[0])
            value = value.split("st")[1]
        c = float(value.replace("個", ""))
        result = int(lc * 3456 + st * 64 + c)
        return max(result, 0)

    @staticmethod
    def stack_check_reverse(value: int) -> Union[int, str]:
        """
        :param value: int型の価格
        :return:　valueをストックされた形に直す
        """
        if value <= 0:
            return 0
        elif value <= 63:
            return value
        else:
            k, j = divmod(value, 54 * 64)
            i, j = divmod(j, 64)
            calc_result = []
            if k != 0:
                calc_result.append(f"{k}LC")
            if i != 0:
                calc_result.append(f"{i}st")
            if j != 0:
                calc_result.append(f"{j}個")
            return "+".join(calc_result)

    @staticmethod
    def edit_embed(target_embed, title, description):
        embed = target_embed.embeds[0]
        embed.description = description
        embed.title = title
        return embed

    async def check_catacombs_level(ctx, uuid):

        api = await bot.db_select("api")
        api_key = api[0][0]

        url = f"https://api.hypixel.net/v2/skyblock/profiles?key={api_key}&uuid={uuid}"
        response = requests.get(url)
        jsonData = response.json()

        if jsonData.get("success"):
            catacombs_exp = 0
            for profile in jsonData["profiles"]:

                if "dungeons" in profile.get("members", {}).get(uuid, {}):
                    try:
                        dungeon_types = profile["members"][uuid]["dungeons"]["dungeon_types"]
                    except KeyError:
                        continue
                    if "catacombs" in dungeon_types and "experience" in dungeon_types["catacombs"]:
                        catacombs_exp = max(catacombs_exp, int(dungeon_types["catacombs"]["experience"]))

            catacombs_level_table_totality = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940,
                                              12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140,
                                              259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640,
                                              3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640,
                                              23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640,
                                              139559640, 177559640, 225559640, 285559640, 360559640, 453559640,
                                              569809640]

            for i in range(70):
                catacombs_level_table_totality.append(catacombs_level_table_totality[-1]+200000000)

            for i in range(len(catacombs_level_table_totality)):
                if catacombs_exp < catacombs_level_table_totality[i]:
                    diff = catacombs_level_table_totality[i] - catacombs_level_table_totality[i - 1]
                    now_progress = i + float((catacombs_exp - catacombs_level_table_totality[i - 1]) / diff)
                    to_50_progress_percent = Decimal((catacombs_exp / 569809640) * 100).quantize(Decimal('0.0001'),
                                                                                                 rounding=ROUND_HALF_UP)
                    return Decimal(now_progress).quantize(Decimal('0.01'),
                                                          rounding=ROUND_HALF_UP), to_50_progress_percent

        return False

    @staticmethod
    def calc_skill_level(xp, frag):
        skill_xp_table = [
            50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925,
            14925, 32425, 47425, 67425, 97425, 147425, 222425, 322425,
            522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425,
            4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425,
            13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425,
            27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425,
            47472425, 51172425, 55172425, 59472425, 64072425, 68972425, 74172425,
            79672425, 85472425, 91572425, 97972425, 104672425, 111672425
        ]

        skill_xp_table_other = [
            50, 150, 275, 435, 635, 885, 1200, 1600, 2100, 2725,
            3510, 4510, 5760, 7325, 9325, 11825, 14950, 18950, 23950,
            30200, 38050, 47850, 60100, 75400, 94450
        ]

        table = skill_xp_table if frag else skill_xp_table_other
        max_level = len(table) if frag else 25
        for i, xp_threshold in enumerate(table):
            if xp < xp_threshold:
                return i + 1
        return max_level

    @staticmethod
    def pickup(hairetu, target_value):
        result = []
        for sublist in hairetu:
            if target_value in sublist:
                result.append(sublist[0])
        return result

    async def db_select(ctx, table_name):
        message_id_dict = {"player_data":1154408467474432100,"special":1137367878316871682,"api":1153792122651148298,"mmorpg":1188454119036420197,"odd":1265682766381580350}
        message = await discord.utils.get(bot.get_guild(730269755432239116).channels, name=table_name).fetch_message(message_id_dict[table_name])
        content = message.content
        content_array = content.split('\n')
        for i in range(len(content_array)):
            content_array[i] = content_array[i].split(" ")
        return content_array

    async def db_insert(ctx, table_name, data):
        message_id_dict = {"player_data":1154408467474432100,"special":1137367878316871682,"api":1153792122651148298,"mmorpg":1188454119036420197,"odd":1265682766381580350}
        message = await discord.utils.get(bot.get_guild(730269755432239116).channels, name=table_name).fetch_message(message_id_dict[table_name])
        await message.edit(content=data)

    async def on_command_error(self, ctx, error):
        """すべてのコマンドで発生したエラーを拾う"""
        if isinstance(error, commands.CommandInvokeError):  # コマンド実行時にエラーが発生したら
            orig_error = getattr(error, "original", error)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            error_message = f'```{error_msg}```'
            ch = ctx.guild.get_channel(769236872538357801)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:{ctx.channel}\ntime:{time}\nuser:{ctx.author.display_name}')
            await ch.send(embed=embed)


if __name__ == '__main__':
    bot = DUNGEON_BOT(prefix="!")
    bot.run("ODI2MTAwOTg5MjM2NDc3OTgy.GSpnTS.5Oc66TGGTah1UwRG20ebXSGVEZ8e8qi3LcNyL4")
