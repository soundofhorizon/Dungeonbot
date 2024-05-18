import traceback
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

import discord
import requests
from discord.ext import commands


class NetWorthCalc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nw(self, ctx):

        def check(m):
            if m.author.bot:
                return
            return m.channel == ctx.channel and m.author == ctx.author

        def format_BMK(m) -> str:
            if m >= 1000000000:
                m = f"{Decimal(str(float(m/1000000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}B"
            elif m >= 1000000:
                m = f"{Decimal(str(float(m/1000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}M"
            elif m >= 1000:
                m = f"{Decimal(str(float(m/1000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}K"
            return m

        try:
            show_embed_description = "Fetching... \nPlease wait..."
            embed = discord.Embed(
                description=show_embed_description,
                color=0x61c1a9)
            show_embed = await ctx.send(embed=embed)

            api = await self.bot.db_select("api")
            api_key = api[0][0]

            uuid_list = await self.bot.db_select("player_data")
            uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
            uuid = ""
            for i,j in uuid_list:
                if j == ctx.author.id:
                    uuid = i[1:]
                    break

            frag = True
            print(api_key, uuid)
            while frag:
                try:
                    response = requests.get(
                        f'https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}', timeout=3.0)
                    frag = False
                except requests.exceptions.ReadTimeout:
                    continue
            jsonData = response.json()

            profile_option = []
            description = ""
            for j in range(len(jsonData["profiles"])):
                description += f'{j+1}: {jsonData["profiles"][j]["cute_name"]}\n'
            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "番号でprofileを選択してください。", description))
            try:
                user_select_input = await self.bot.wait_for("message", check=check)
                user_select_input = user_select_input.content
                if int(user_select_input) <= 0 or len(jsonData["profiles"])+1 < int(user_select_input):
                    await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "指定した番号が範囲外です。\nSession closed."))
                    return
            except ValueError:
                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "検索したいprofileを「番号」で入力してください。\nSession closed."))
                return
            await ctx.channel.purge(limit=1)
            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "計算中…", "please wait..."))
            user_select_input = int(user_select_input) - 1
            send_body = {"data": jsonData["profiles"][user_select_input]["members"][str(uuid)]}

            # golden dragonだけ別カウントをする。
            golden_drag_count = 0
            lv200_golden_drag = 0
            lv100_golden_drag = 0
            for j in jsonData["profiles"][user_select_input]["members"][str(uuid)]["pets"]:
                if j["type"] == "GOLDEN_DRAGON":
                    if j["exp"] >= 210255385:
                        lv200_golden_drag += 1
                    elif j["exp"] >= 25353230:
                        lv100_golden_drag += 1
                    else:
                        golden_drag_count += 1
            frag = True
            while frag:
                try:
                    response = requests.post(
                        f'https://skyblock.acebot.xyz/api/networth/categories', json=send_body, timeout=10.0)
                    frag = False
                except requests.exceptions.ReadTimeout:
                    continue
            resp = response.json()

            description = ""
            networth_total = 0
            try:
                for i in resp["data"]["categories"]:
                    networth_temp = int(resp["data"]["categories"][i]["total"])
                    for j in resp["data"]["categories"][i]["top_items"]:
                        try:
                            if j["recomb"]:
                                networth_temp += 5000000
                            if "➎" in j["name"]:
                                networth_temp += 200000000
                            elif "➍" in j["name"]:
                                networth_temp += 100000000
                            elif "➌" in j["name"]:
                                networth_temp += 60000000
                            elif "➋" in j["name"]:
                                networth_temp += 30000000
                            elif "➊" in j["name"]:
                                networth_temp += 10000000
                        except KeyError:
                            continue
                    if i == "pets":
                        networth_temp += lv200_golden_drag * 1200000000
                        networth_temp += lv100_golden_drag * 700000000
                        networth_temp += golden_drag_count * 500000000
                    networth_total += networth_temp
                    # 名前を見やすいようにする。
                    title = ""
                    if i == "storage":
                        title = "Storage"
                    elif i == "inventory":
                        title = "Inventory"
                    elif i == "enderchest":
                        title = "Enderchest"
                    elif i == "armor":
                        title = "Armor"
                    elif i == "wardrobe_inventory":
                        title = "Wardrobe"
                    elif i == "pets":
                        title = "Pet"
                    elif i == "talismans":
                        title = "Talisman"
                    description += f'\n**{title}: {format_BMK(networth_temp)}**\n'
                    show_count = 0
                    for j in resp["data"]["categories"][i]["top_items"]:
                        show_count += 1
                        description += f"|  {j['name']} (**{format_BMK(j['price'])}**)\n"
                        if show_count >= 6:
                            description += f'|  ... more **{len(resp["data"]["categories"][i]["top_items"]) - 6}** items\n'
                            break

                # total
                description += f"\nTotal: **{format_BMK(networth_total)}**"
                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "計算結果", description))
            except:
                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "API off (disable) / profileが違う\nなどの理由によりnetworthの計算ができません。\n再度お試しください。"))
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

    @commands.command()
    async def mmo_init(self, ctx):
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        player_data = ""
        for i in uuid_list:
            player_data += f"{i[1]} 0 1 0 100000000000000 150 0 0\n"
        await self.bot.db_insert("mmorpg", player_data)

def setup(bot):
    bot.add_cog(NetWorthCalc(bot))
