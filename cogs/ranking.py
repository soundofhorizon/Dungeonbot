import json
import math
import traceback
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

import discord
import requests
from discord.ext import commands
from senitherweight import SenitherWeight

"""各種ランキング"""


class Ranking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx, mode: str, arg1: Optional[str]):
        catacombs_level_table_totality = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940,
                                          12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140,
                                          259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640,
                                          3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640,
                                          23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640,
                                          139559640, 177559640, 225559640, 285559640, 360559640, 453559640,
                                          569809640]

        for i in range(70):
            catacombs_level_table_totality.append(catacombs_level_table_totality[-1]+200000000)

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

            if mode.startswith(("slayer", "dungeon", "jacob", "money", "skill", "pets", "weight", "networth")):
                # 各種保存用dict
                bank_amount_dict = {}
                jacob_gold_dict = {}
                slayer_slain_dict = {}
                dungeon_round_dict = {}
                skill_xp_dict = {}
                cata_dict = {}
                pet_dict = {}
                weight_dict = {}
                networth_dict = {}
                title = ""
                skill_all_avg = 0
                weight_all_avg = 0
                cata_to50_percent = ""
                for i in uuid_list:
                    uuid = i[0][1:]
                    print(uuid)
                    frag = True
                    while frag:
                        try:
                            response = requests.get(
                                f'https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}', timeout=3.0)
                            frag = False
                        except requests.exceptions.ReadTimeout:
                            continue
                    jsonData = response.json()

                    if mode == "networth":
                        title = "Networth ランキング"

                        for j in range(len(jsonData["profiles"])):
                            send_body = {"data": jsonData["profiles"][j]["members"][str(uuid)]}
                            # golden dragonだけ別カウントをする。
                            golden_drag_count = 0
                            lv200_golden_drag = 0
                            lv100_golden_drag = 0
                            try:
                                for j in jsonData["profiles"][j]["members"][str(uuid)]["pets"]:
                                    if j["type"] == "GOLDEN_DRAGON":
                                        if j["exp"] >= 210255385:
                                            lv200_golden_drag += 1
                                        elif j["exp"] >= 25353230:
                                            lv100_golden_drag += 1
                                        else:
                                            golden_drag_count += 1
                            except KeyError:
                                continue
                            frag = True
                            while frag:
                                try:
                                    response = requests.post(
                                        f'https://skyblock.acebot.xyz/api/networth/categories', json=send_body, timeout=10.0)
                                    frag = False
                                except requests.exceptions.ReadTimeout:
                                    continue
                            resp = response.json()
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
                            except KeyError:
                                continue
                            # total
                            if f"{self.bot.uuid_to_mcid(uuid)}" not in networth_dict.keys() or networth_total > networth_dict[f"{self.bot.uuid_to_mcid(uuid)}"]:
                                networth_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = networth_total
                    if mode == "weight":
                        try:
                            senither = SenitherWeight(api_key)
                            jsonData = await senither.get_weight(uuid)

                            title = "Skyblock Weightランキング"
                            weight_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = round(
                                float(jsonData["total"]), 2)
                            weight_all_avg += float(jsonData["total"])
                        except json.decoder.JSONDecodeError:
                            continue
                    elif mode == "dungeon" and arg1 == "secret":
                        frag = True
                        while frag:
                            try:
                                response = requests.get(
                                    f'https://sky.shiiyu.moe/api/v2/dungeons/{self.bot.uuid_to_mcid(uuid)}',
                                    timeout=5.0)
                                frag = False
                            except requests.exceptions.ReadTimeout:
                                continue
                        jsonData = response.json()
                        rounds = 0
                        for j in jsonData["profiles"]:
                            if "secrets_found" in jsonData["profiles"][j]["dungeons"]:
                                try:
                                    rounds = int(jsonData["profiles"][j]["dungeons"]["secrets_found"])
                                    pass
                                except KeyError:
                                    continue
                        dungeon_round_dict[self.bot.uuid_to_mcid(uuid)] = rounds
                    else:
                        frag = True
                        while frag:
                            try:
                                response = requests.get(
                                    f'https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}', timeout=3.0)
                                frag = False
                            except requests.exceptions.ReadTimeout:
                                continue
                        jsonData = response.json()
                        # データを取得
                        if mode == "slayer":
                            try:
                                if arg1.startswith(("zombie", "wolf", "spider", "enderman", "blaze")):
                                    title = f"{arg1}スレイヤー累計討伐数ランキング"
                                    slayer_slain = 0
                                    for j in range(len(jsonData["profiles"])):
                                        if "slayer_bosses" in jsonData["profiles"][j]["members"][uuid]:
                                            try:
                                                temp = 0
                                                if arg1 == "zombie":
                                                    for k in range(5):
                                                        temp += \
                                                            jsonData["profiles"][j]["members"][uuid]["slayer_bosses"][
                                                                arg1][f"boss_kills_tier_{k}"]
                                                else:
                                                    for k in range(4):
                                                        temp += \
                                                            jsonData["profiles"][j]["members"][uuid]["slayer_bosses"][
                                                                arg1][f"boss_kills_tier_{k}"]
                                                if int(slayer_slain) < temp:
                                                    slayer_slain = temp
                                            except KeyError:
                                                continue
                                    slayer_slain_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = slayer_slain
                                else:
                                    await show_embed.edit(
                                        embed=self.bot.edit_embed(show_embed, "Error",
                                                                  "検索できるSlayerのワードは'zombie', 'wolf', 'spider', 'enderman', 'blaze'の5つです"))
                                    return
                            except IndexError:
                                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error",
                                                                                "検索キーワードが入力されていません。検索できるSlayerのワードは'zombie', 'wolf', 'spider', 'enderman', 'blaze'の5つです"))
                                return

                        elif mode == "skill":
                            try:
                                if arg1.startswith(('farming', 'combat', 'mining', 'foraging', 'fishing',
                                                    'enchanting', 'alchemy', 'carpentry', 'taming',
                                                    'runecrafting')):
                                    title = f"Skill-{arg1.upper()}ランキング"
                                    skill_xp = 0
                                    for j in range(len(jsonData["profiles"])):
                                        if f"experience_skill_{arg1}" in jsonData["profiles"][j]["members"][uuid]:
                                            try:
                                                if int(skill_xp) < int(jsonData["profiles"][j]["members"][uuid][
                                                                           f"experience_skill_{arg1}"]):
                                                    skill_xp = int(jsonData["profiles"][j]["members"][uuid][
                                                                       f"experience_skill_{arg1}"])
                                            except KeyError:
                                                continue
                                    skill_xp_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = skill_xp

                                elif arg1 == "avg":
                                    title = f"SkillAverageランキング"
                                    skill_list = ['farming', 'combat', 'mining', 'foraging', 'fishing',
                                                  'enchanting', 'alchemy', 'taming']
                                    total_xp_lv = 0
                                    for j in range(len(jsonData["profiles"])):
                                        tmp_total_xp_lv = 0
                                        for k in skill_list:
                                            if f"experience_skill_{k}" in jsonData["profiles"][j]["members"][uuid]:
                                                try:
                                                    tmp_xp_lv = int(jsonData["profiles"][j]["members"][uuid][
                                                                        f"experience_skill_{k}"])
                                                    if k in ['fishing', 'alchemy',
                                                             'taming'] and self.bot.calc_skill_level(tmp_xp_lv,
                                                                                                     True) > 50:
                                                        tmp_total_xp_lv += 50
                                                    else:
                                                        tmp_total_xp_lv += self.bot.calc_skill_level(tmp_xp_lv, True)
                                                except KeyError:
                                                    continue
                                        if tmp_total_xp_lv > total_xp_lv:
                                            total_xp_lv = tmp_total_xp_lv

                                    skill_xp_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = float(total_xp_lv / 8)
                                    skill_all_avg += float(total_xp_lv / 8)

                                else:
                                    description = "検索できるskillのワードは'farming', 'combat', mining', 'foraging', 'fishing'," \
                                                  " 'enchanting', 'alchemy', 'carpentry', 'taming' , 'runecrafting', 'avg'の11個です"
                                    await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", description))
                                    return
                            except IndexError:
                                description = "検索キーワードが入力されていません。検索できるSlayerのワードはskillのワードは'farming', 'combat', " \
                                              "mining', 'foraging', 'fishing', 'enchanting', 'alchemy', 'carpentry', " \
                                              "'taming' , 'runecrafting', 'avg'の11個です"
                                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", description))
                                return

                        elif mode == "dungeon":
                            if arg1 is None:
                                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "階層の指定がされていません。"))
                                return
                            elif arg1 == "cata":
                                check_catacombs_level = await self.bot.check_catacombs_level(uuid)
                                if check_catacombs_level[0] == 1.0:
                                    continue
                                elif check_catacombs_level and check_catacombs_level[0]:
                                    cata_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = check_catacombs_level
                            else:
                                try:
                                    frag = True
                                    floor = arg1
                                    if "m" in floor:
                                        frag = False
                                    if frag:
                                        if floor == "all":
                                            rounds = 0
                                            title = f"catacombs全体の周回数ランキング"
                                            for j in range(len(jsonData["profiles"])):
                                                if "dungeons" in jsonData["profiles"][j]["members"][uuid]:
                                                    try:
                                                        temp = 0
                                                        for k in range(8):
                                                            temp += int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["catacombs"]["tier_completions"][
                                                                    f"{k}"])
                                                        if rounds < temp:
                                                            rounds = temp
                                                    except KeyError:
                                                        continue
                                            dungeon_round_dict[self.bot.uuid_to_mcid(uuid)] = rounds
                                        elif 0 <= int(floor) < 8:
                                            floor = int(floor)
                                            rounds = 0
                                            if floor == 0:
                                                title = f"catacombs-Entranceの周回数ランキング"
                                            else:
                                                title = f"catacombs-F{floor}の周回数ランキング"
                                            for j in range(len(jsonData["profiles"])):
                                                if "dungeons" in jsonData["profiles"][j]["members"][uuid]:
                                                    try:
                                                        if rounds < int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["catacombs"]["tier_completions"][
                                                                    f"{floor}"]):
                                                            rounds = int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["catacombs"]["tier_completions"][
                                                                    f"{floor}"])
                                                    except KeyError:
                                                        continue
                                            dungeon_round_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = rounds
                                        else:
                                            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error",
                                                                                            "ダンジョンにそのような階層があるとお思いで???"))
                                            return
                                    else:
                                        floor = str(floor).replace("m", "")
                                        if floor == "all":
                                            rounds = 0
                                            title = f"catacombs-master全体の周回数ランキング"
                                            for j in range(len(jsonData["profiles"])):
                                                if "dungeons" in jsonData["profiles"][j]["members"][uuid]:
                                                    try:
                                                        temp = 0
                                                        for k in range(7):
                                                            temp += int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["master_catacombs"][
                                                                    "tier_completions"][
                                                                    f"{k + 1}"])
                                                        if rounds < temp:
                                                            rounds = temp
                                                    except KeyError:
                                                        continue
                                            dungeon_round_dict[self.bot.uuid_to_mcid(uuid)] = rounds
                                        elif 1 <= int(floor) < 8:
                                            floor = int(floor)
                                            rounds = 0
                                            title = f"catacombs-M{floor}の周回数ランキング"
                                            for j in range(len(jsonData["profiles"])):
                                                if "dungeons" in jsonData["profiles"][j]["members"][uuid]:
                                                    try:
                                                        if rounds < int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["master_catacombs"][
                                                                    "tier_completions"][
                                                                    f"{floor}"]):
                                                            rounds = int(
                                                                jsonData["profiles"][j]["members"][uuid]["dungeons"][
                                                                    "dungeon_types"]["master_catacombs"][
                                                                    "tier_completions"][
                                                                    f"{floor}"])
                                                    except KeyError:
                                                        continue
                                            dungeon_round_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = rounds
                                        else:
                                            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error",
                                                                                            "ダンジョンにそのような階層があるとお思いで???"))
                                            return
                                except KeyError:
                                    await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error",
                                                                                    "階層を数字で指定してください。Entranceは0Fと認識されています。"))
                                    return
                                except ValueError:
                                    await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error",
                                                                                    "数字のみ指定が可能です。Entranceは0Fと設定されています。"))
                                    return

                        elif mode == "jacob":

                            if arg1 == "gold":
                                title = "jacob金メダル取得ランキング"
                                jacob_gold_medals = 0
                                for j in range(len(jsonData["profiles"])):
                                    if "jacob2" in jsonData["profiles"][j]["members"][uuid] and "unique_golds2" in \
                                            jsonData["profiles"][j]["members"][uuid]["jacob2"]:
                                        try:
                                            if int(jacob_gold_medals) < len(
                                                    jsonData["profiles"][j]["members"][uuid]["jacob2"][
                                                        "unique_golds2"]):
                                                jacob_gold_medals = len(
                                                    jsonData["profiles"][j]["members"][uuid]["jacob2"]["unique_golds2"])
                                        except KeyError:
                                            continue
                                jacob_gold_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = jacob_gold_medals
                            elif arg1 == "contest":
                                title = "jacobコンテスト参加数ランキング"
                                jacob_join_contests = 0
                                for j in range(len(jsonData["profiles"])):
                                    if "jacob2" in jsonData["profiles"][j]["members"][uuid]:
                                        try:
                                            if int(jacob_join_contests) < len(
                                                    jsonData["profiles"][j]["members"][uuid]["jacob2"]["contests"]):
                                                jacob_join_contests = len(
                                                    jsonData["profiles"][j]["members"][uuid]["jacob2"]["contests"])
                                        except KeyError:
                                            continue
                                    jacob_gold_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = jacob_join_contests
                            else:
                                await show_embed.edit(
                                    embed=self.bot.edit_embed(show_embed, "Error", "検索キーワードは'gold', 'contest'の2種類です。"))
                                return

                        elif mode == "money":  # まあ構造的に必要はないが念のため
                            title = "所持金額ランキング"
                            bank_amount = 0
                            for j in range(len(jsonData["profiles"])):
                                if "banking" in jsonData["profiles"][j]:
                                    try:
                                        if int(bank_amount) < (int(jsonData["profiles"][j]["banking"]["balance"]) + int(
                                                jsonData["profiles"][j]["members"][uuid]["coin_purse"])):
                                            bank_amount = (int(jsonData["profiles"][j]["banking"]["balance"]) + int(
                                                jsonData["profiles"][j]["members"][uuid]["coin_purse"]))
                                    except KeyError:
                                        bank_amount = 0
                                else:
                                    try:
                                        if int(bank_amount) < int(
                                                jsonData["profiles"][j]["members"][uuid]["coin_purse"]):
                                            bank_amount = int(jsonData["profiles"][j]["members"][uuid]["coin_purse"])
                                    except KeyError:
                                        bank_amount = 0
                            bank_amount_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = bank_amount

                        elif mode == "pets":
                            if arg1 == "type":
                                title = "LEGENDARY PET所持数ランキング"
                                pets = 0
                                for j in range(len(jsonData["profiles"])):
                                    profile_pets = 0
                                    pets_list = []
                                    if "pets" in jsonData["profiles"][j]["members"][uuid]:
                                        try:
                                            for k in range(len(jsonData["profiles"][j]["members"][uuid]["pets"])):
                                                if jsonData["profiles"][j]["members"][uuid]["pets"][k][
                                                    "tier"] == "LEGENDARY" and \
                                                        jsonData["profiles"][j]["members"][uuid]["pets"][k][
                                                            "type"] not in pets_list:
                                                    profile_pets += 1
                                                    pets_list.append(
                                                        jsonData["profiles"][j]["members"][uuid]["pets"][k]["type"])
                                            if int(pets) < int(profile_pets):
                                                pets = profile_pets
                                        except KeyError:
                                            continue
                                pet_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = pets

                            elif arg1 == "max":
                                title = "LEGENDARY PET LV100所持数ランキング"
                                pets = 0
                                for j in range(len(jsonData["profiles"])):
                                    profile_pets = 0
                                    pets_list = []
                                    if "pets" in jsonData["profiles"][j]["members"][uuid]:
                                        try:
                                            for k in range(len(jsonData["profiles"][j]["members"][uuid]["pets"])):
                                                if jsonData["profiles"][j]["members"][uuid]["pets"][k][
                                                    "tier"] == "LEGENDARY" and \
                                                        jsonData["profiles"][j]["members"][uuid]["pets"][k][
                                                            "type"] not in pets_list and \
                                                        float(jsonData["profiles"][j]["members"][uuid]["pets"][k][
                                                                  "exp"]) > 25353230:
                                                    profile_pets += 1
                                                    pets_list.append(
                                                        jsonData["profiles"][j]["members"][uuid]["pets"][k]["type"])
                                            if int(pets) < int(profile_pets):
                                                pets = profile_pets
                                        except KeyError:
                                            continue
                                pet_dict[f"{self.bot.uuid_to_mcid(uuid)}"] = pets
                            else:
                                await show_embed.edit(
                                    embed=self.bot.edit_embed(show_embed, "Error", "検索キーワードは'type', 'max'の2種類です。"))
                                return

                # ランキングを文字列化
                discription = ""
                check_dict = {}

                # cataだけvalueがtupleあるため、特別に分解して50_progressを別として取り扱う
                to_50_check_dict = {}
                if mode == "slayer":
                    check_dict = slayer_slain_dict
                elif mode == "dungeon":
                    if arg1 == "cata":
                        title = "Dungeon Catacombs Levelランキング"
                        cata_dict_keys = cata_dict.keys()
                        for i in cata_dict_keys:
                            check_dict[i] = float(cata_dict[i][0])
                            to_50_check_dict[i] = cata_dict[i][1]
                    else:
                        title = "Dungeon Roundingランキング"
                        check_dict = dungeon_round_dict
                elif mode == "jacob":
                    check_dict = jacob_gold_dict
                elif mode == "money":  # まあ構造的に必要はないが念のため
                    check_dict = bank_amount_dict
                elif mode == "skill":
                    check_dict = skill_xp_dict
                elif mode == "pets":
                    check_dict = pet_dict
                elif mode == "weight":
                    check_dict = weight_dict
                elif mode == "networth":
                    check_dict = networth_dict
                score_sorted = sorted(check_dict.items(), key=lambda x: x[1], reverse=True)
                rank = 1
                rank_stack = 0
                before_amount = 0
                i = 0
                cata_xp_total = 0
                for k in score_sorted:
                    k = list(k)
                    if float(k[1]) != 0:
                        if float(k[1]) < before_amount and i != 0:
                            rank += rank_stack
                            rank_stack = 1
                        else:
                            rank_stack += 1
                        mcid = k[0]
                        k[0] = k[0].replace("_", "\_")
                        if mode == "jacob":
                            if arg1 == "gold":
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}個\n"
                            elif arg1 == "contest":
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}回\n"
                        elif mode == "money":
                            discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}coin\n"
                        elif mode == "networth":
                            discription += f"{rank}位: {k[0]} → {format_BMK(int(k[1]))}\n"
                        elif mode == "dungeon":
                            if arg1 == "cata":
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(float(k[1]))}\n"
                                discription += f"|　　cata 50 Progress: {to_50_check_dict[mcid]}%\n"

                                # cata xpをここで再計算する
                                decimal_part, integer_part = math.modf(float(k[1]))
                                cata_xp_total += catacombs_level_table_totality[int(integer_part)-1]
                                cata_xp_total += float((catacombs_level_table_totality[int(integer_part)] - catacombs_level_table_totality[int(integer_part) - 1])*decimal_part)
                                print(cata_xp_total)
                            elif arg1 == "secret":
                                title = "Skyblock Dungeon Secret ランキング"
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}個\n"
                            else:
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}周\n"
                        elif mode == "skill":
                            if arg1 == "runecrafting":
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}({self.bot.calc_skill_level(float(k[1]), False)})\n"
                            elif arg1 == "avg":
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(float(k[1]))}\n"
                            else:
                                discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}({self.bot.calc_skill_level(float(k[1]), True)})\n"
                        elif mode == "slayer":
                            discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}回\n"
                        elif mode == "pets":
                            discription += f"{rank}位: {k[0]} → {'{:,}'.format(int(k[1]))}種類\n"
                        elif mode == "weight":
                            discription += f"{rank}位: {k[0]} → {'{:,}'.format(float(k[1]))}\n"
                        before_amount = float(k[1])
                        i += 1
                if mode == "skill" and arg1 == "avg":
                    discription += f"\n------------\n サーバー内平均: {Decimal(str(float(skill_all_avg / rank))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"
                if mode == "weight":
                    discription += f"\n------------\n サーバー内平均: {Decimal(str(float(weight_all_avg / rank))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"
                if mode == "dungeon" and arg1 == "cata":
                    cata_xp_avg = float(cata_xp_total / rank)
                    cata_lv_avg = 0
                    for s in range(len(catacombs_level_table_totality)):
                        if cata_xp_avg <= catacombs_level_table_totality[s]:
                            cata_lv_avg = s
                            cata_xp_avg -= catacombs_level_table_totality[s-1]
                            cata_lv_avg += Decimal(str(float(cata_xp_avg/catacombs_level_table_totality[s]))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                            break
                    discription += f"\n------------\n サーバー内平均: {cata_lv_avg}"
                embed = show_embed.embeds[0]
                embed.description = discription
                embed.title = title
                await show_embed.edit(embed=embed)
            else:
                await show_embed.edit(
                    embed=self.bot.edit_embed(show_embed, "Error", "指定された検索単語は対象外です。検索対象は['slayer', 'dungeon', "
                                                                   "'jacob', 'money', 'skill', 'pets', 'weight', 'networth']の8種です。"))

        except Exception as e:
            orig_error = getattr(e, "original", e)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            error_message = f'```{error_msg}```'
            ch = self.bot.get_channel(769236872538357801)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = discord.Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:on_check_time_loop\ntime:{time}\nuser:None')
            await ch.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ranking(bot))
