import json

import discord
import requests
from discord.ext import commands
from senitherweight import SenitherWeight


class ROLE_CHECK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rc"])
    async def role_check(self, ctx):

        show_embed_description = "Checking... \nPlease wait..."
        embed = discord.Embed(
            description=show_embed_description,
            color=0xb2d6ed)
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

        guild = self.bot.get_guild(730269755432239116)

        def func(role):
            return role.id

        # data fetch
        url = f"https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}"
        print(url)

        response = requests.get(url)
        jsonData = response.json()

        # skills
        skills = ['farming', 'combat', 'mining', 'foraging', 'fishing',
                  'enchanting', 'alchemy', 'carpentry', 'taming',
                  'runecrafting']

        role_ids = []
        remove_ids = []

        for j in range(len(jsonData["profiles"])):
            for k in range(len(skills)):
                if f"experience_skill_{skills[k]}" in jsonData["profiles"][j]["members"][uuid]:
                    try:
                        if int(jsonData["profiles"][j]["members"][uuid][
                                   f"experience_skill_{skills[k]}"]) > 111672425:
                            # Farming
                            if k == 0 and not 820811970797895762 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783766472064368659))
                                remove_ids.append(783766472064368659)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=820811970797895762))
                                role_ids.append(820811970797895762)
                            # Combat
                            elif k == 1 and not 818873067366252625 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783750260500463636))
                                remove_ids.append(783750260500463636)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=818873067366252625))
                                role_ids.append(818873067366252625)
                            # Mining
                            elif k == 2 and not 825922760366751834 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783766608904323122))
                                remove_ids.append(783766608904323122)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=825922760366751834))
                                role_ids.append(825922760366751834)
                            # Foraging
                            elif k == 3 and not 1030041107146489917 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783767079819804674))
                                remove_ids.append(783767079819804674)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=1030041107146489917))
                                role_ids.append(1030041107146489917)
                            # Fishing
                            elif k == 4 and not 931621139610996776 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=802484842838097920))
                                remove_ids.append(802484842838097920)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=931621139610996776))
                                role_ids.append(931621139610996776)
                            # Enchanting
                            elif k == 5 and not 788987562764140564 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783766529212678185))
                                remove_ids.append(783766529212678185)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=788987562764140564))
                                role_ids.append(788987562764140564)
                            # Alchemy
                            elif k == 6 and not 834751643891138600 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783750261976989747))
                                remove_ids.append(783750261976989747)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=834751643891138600))
                                role_ids.append(834751643891138600)
                            # Carpentry
                            elif k == 7 and not 1091332618034888744 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=784470119577026570))
                                remove_ids.append(784470119577026570)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=1091332618034888744))
                                role_ids.append(1091332618034888744)
                            # Taming
                            elif k == 8 and not 804713247642615809 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).remove_roles(
                                    discord.utils.get(guild.roles, id=783767493440438272))
                                remove_ids.append(783767493440438272)
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=804713247642615809))
                                role_ids.append(804713247642615809)
                        elif int(jsonData["profiles"][j]["members"][uuid][
                                     f"experience_skill_{skills[k]}"]) > 55172425:
                            if k == 0 and not 783766472064368659 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783766472064368659))
                                role_ids.append(783766472064368659)
                            elif k == 1 and not 783750260500463636 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783750260500463636))
                                role_ids.append(783750260500463636)
                            elif k == 2 and not 783766608904323122 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783766608904323122))
                                role_ids.append(783766608904323122)
                            # Foraging
                            elif k == 3 and not 783767079819804674 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783767079819804674))
                                role_ids.append(783767079819804674)
                            # Fishing
                            elif k == 4 and not 802484842838097920 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=802484842838097920))
                                role_ids.append(802484842838097920)
                            elif k == 5 and not 783766529212678185 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783766529212678185))
                                role_ids.append(783766529212678185)
                            elif k == 6 and not 783750261976989747 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783750261976989747))
                                role_ids.append(783750261976989747)
                            elif k == 7 and not 784470119577026570 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=784470119577026570))
                                role_ids.append(784470119577026570)
                            elif k == 8 and not 783767493440438272 in map(func, guild.get_member(ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(
                                    discord.utils.get(guild.roles, id=783767493440438272))
                                role_ids.append(783767493440438272)
                        elif k == 9 and int(jsonData["profiles"][j]["members"][uuid][
                                                f"experience_skill_{skills[k]}"]) > 94450 and not 791625293399326750 in map(
                            func, guild.get_member(ctx.author.id).roles):
                            await guild.get_member(ctx.author.id).add_roles(
                                discord.utils.get(guild.roles, id=791625293399326750))
                            role_ids.append(791625293399326750)

                    except KeyError:
                        continue

            # rich系
            bank_amount = 0
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

            if bank_amount > 5000000000 and not 1012405159722237953 in map(func, guild.get_member(ctx.author.id).roles):
                if 789887304042545152 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).remove_roles(
                        discord.utils.get(guild.roles, id=789887304042545152))
                    remove_ids.append(789887304042545152)
                await guild.get_member(ctx.author.id).add_roles(discord.utils.get(guild.roles, id=1012405159722237953))
                role_ids.append(1012405159722237953)
            elif bank_amount > 1000000000 and not 1012405159722237953 in map(func, guild.get_member(ctx.author.id).roles) and not 789887304042545152 in map(func, guild.get_member(ctx.author.id).roles):
                await guild.get_member(ctx.author.id).add_roles(discord.utils.get(guild.roles, id=789887304042545152))
                role_ids.append(789887304042545152)

            # Powder系
            if "mining_core" in jsonData["profiles"][j]["members"][uuid] and "powder_mithril_total" in \
                    jsonData["profiles"][j]["members"][uuid]["mining_core"] and "powder_gemstone_total" in \
                    jsonData["profiles"][j]["members"][uuid]["mining_core"]:
                if int(jsonData["profiles"][j]["members"][uuid]["mining_core"]["powder_mithril_total"] +
                       jsonData["profiles"][j]["members"][uuid]["mining_core"]["powder_gemstone_total"]) >= 10000000 \
                        and not 952233672491302932 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=952233672491302932))
                    role_ids.append(952233672491302932)

            # Auction系
            if "stats" in jsonData["profiles"][j]["members"][uuid] and "auctions_completed" in \
                    jsonData["profiles"][j]["members"][uuid]["stats"]:
                if int(jsonData["profiles"][j]["members"][uuid]["stats"]["auctions_completed"]) >= 20000 \
                        and not 837364656019603497 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=837364656019603497))
                    role_ids.append(837364656019603497)

            # Bestiary系
            if "bestiary" in jsonData["profiles"][j]["members"][uuid] and "milestone" in \
                    jsonData["profiles"][j]["members"][uuid]["bestiary"]:
                print(jsonData["profiles"][j]["members"][uuid]["bestiary"]["milestone"]["last_claimed_milestone"])
                if int(jsonData["profiles"][j]["members"][uuid]["bestiary"]["milestone"]["last_claimed_milestone"]) >= 325 \
                        and not 881394243237728377 in map(func, guild.get_member(ctx.author.id).roles):
                    if 833469163145134100 in map(func, guild.get_member(ctx.author.id).roles):
                        await guild.get_member(ctx.author.id).remove_roles(
                            discord.utils.get(guild.roles, id=833469163145134100))
                        remove_ids.append(833469163145134100)
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=881394243237728377))
                    role_ids.append(881394243237728377)
                elif int(jsonData["profiles"][j]["members"][uuid]["bestiary"]["milestone"]["last_claimed_milestone"]) >= 300 \
                        and not 833469163145134100 in map(func, guild.get_member(ctx.author.id).roles) and not 881394243237728377 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=833469163145134100))
                    role_ids.append(833469163145134100)

            # trophy系
            if "trophy_fish" in jsonData["profiles"][j]["members"][uuid] and "rewards" in \
                    jsonData["profiles"][j]["members"][uuid]["trophy_fish"]:
                if int(len(jsonData["profiles"][j]["members"][uuid]["trophy_fish"]["rewards"])) >= 4 \
                        and not 1090254262501638324 in map(func, guild.get_member(ctx.author.id).roles):
                    if 1191380319862018048 in map(func, guild.get_member(ctx.author.id).roles):
                        await guild.get_member(ctx.author.id).remove_roles(
                            discord.utils.get(guild.roles, id=1191380319862018048))
                        remove_ids.append(1191380319862018048)
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=1090254262501638324))
                    role_ids.append(1090254262501638324)
                elif int(len(jsonData["profiles"][j]["members"][uuid]["trophy_fish"]["rewards"])) >= 3 \
                        and not 1191380319862018048 in map(func, guild.get_member(ctx.author.id).roles) and not 1090254262501638324 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=1191380319862018048))
                    role_ids.append(1191380319862018048)

            # Secret Role
            rift_data = jsonData["profiles"][j]["members"][uuid].get("rift", {}).get("west_village", {}).get("kat_house", {})

            if rift_data and all(rift_data.get(f"bin_collected_{creature}", 0) >= 100 for creature in ["silverfish", "spider", "mosquito"]):
                if len(set(rift_data[f"bin_collected_{creature}"] for creature in ["silverfish", "spider", "mosquito"])) == 1 \
                    and not 1191383168264196146 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(discord.utils.get(guild.roles, id=1191383168264196146))
                    role_ids.append(1191383168264196146)
            # dungeons
            if "dungeons" in jsonData["profiles"][j]["members"][uuid]:
                # Classes
                classes = [["archer", 952239445627785276], ["mage", 952239048527868014],
                           ["berserk", 952239181801861162], ["healer", 952238853769547827],
                           ["tank", 933063229607919626]]
                for i in classes:
                    try:
                        if "experience" in jsonData["profiles"][j]["members"][uuid]["dungeons"]["player_classes"][i[0]]:
                            if int(jsonData["profiles"][j]["members"][uuid]["dungeons"]["player_classes"][i[0]][
                                       "experience"]) >= 569809640 and not i[1] in map(func, guild.get_member(
                                ctx.author.id).roles):
                                await guild.get_member(ctx.author.id).add_roles(discord.utils.get(guild.roles, id=i[1]))
                                role_ids.append(i[1])
                    except KeyError:
                        pass

                # Catacombs Level
                clv = await self.bot.check_catacombs_level(uuid)
                if clv[0] >= 50 and not 847891295560138803 in map(func,guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=847891295560138803))
                    role_ids.append(847891295560138803)

                # Boss Kills:
                boss_kill_roles = [952249753842896906, 952249863318417468, 952249917995372684, 952250079195049995,
                                   788351892694630450, 845224491742134292, 815508395347935263]
                for i in range(7):
                    rounds = 0
                    try:
                        if "catacombs" in jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]:
                            rounds += \
                                jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"][
                                    "tier_completions"][str(i + 1)]
                        if "master_catacombs" in jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]:
                            rounds += \
                                jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]["master_catacombs"][
                                    "tier_completions"][str(i + 1)]
                    except KeyError:
                        pass
                    if rounds >= 1000:
                        if not boss_kill_roles[i] in map(func, guild.get_member(ctx.author.id).roles):
                            await guild.get_member(ctx.author.id).add_roles(
                                discord.utils.get(guild.roles, id=boss_kill_roles[i]))
                            role_ids.append(boss_kill_roles[i])

                # F7 Fast rn
                try:
                    if jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]["master_catacombs"][
                        "fastest_time_s_plus"]["7"] <= 510000 or \
                            jsonData["profiles"][j]["members"][uuid]["dungeons"]["dungeon_types"]["catacombs"][
                                "fastest_time_s_plus"]["7"] <= 330000:
                        if not 796316214657679390 in map(func, guild.get_member(ctx.author.id).roles):
                            await guild.get_member(ctx.author.id).add_roles(
                                discord.utils.get(guild.roles, id=796316214657679390))
                            role_ids.append(796316214657679390)
                except KeyError:
                    pass

        # Weight系
        try:
            senither = SenitherWeight(api_key)
            jsonData = await senither.get_weight(uuid)
            weight = round(float(jsonData["total"]), 2)
            if weight >= 20000 and not 891552104844521474 in map(func, guild.get_member(ctx.author.id).roles):
                if 1056214203544903691 in map(func, guild.get_member(ctx.author.id).roles) or 1091326995280973845 in map(func, guild.get_member(ctx.author.id).roles):
                    pass
                else:
                    await guild.get_member(ctx.author.id).add_roles(
                        discord.utils.get(guild.roles, id=891552104844521474))
                    role_ids.append(891552104844521474)
            elif weight >= 30000 and not 1056214203544903691 in map(func, guild.get_member(ctx.author.id).roles):
                if 891552104844521474 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).remove_roles(
                        discord.utils.get(guild.roles, id=891552104844521474))
                    remove_ids.append(891552104844521474)
                await guild.get_member(ctx.author.id).add_roles(
                    discord.utils.get(guild.roles, id=1056214203544903691))
                role_ids.append(1056214203544903691)
            elif weight >= 45000 and not 1091326995280973845 in map(func, guild.get_member(ctx.author.id).roles):
                if 891552104844521474 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).remove_roles(
                        discord.utils.get(guild.roles, id=891552104844521474))
                    remove_ids.append(891552104844521474)
                if 1056214203544903691 in map(func, guild.get_member(ctx.author.id).roles):
                    await guild.get_member(ctx.author.id).remove_roles(
                        discord.utils.get(guild.roles, id=1056214203544903691))
                    remove_ids.append(1056214203544903691)
                await guild.get_member(ctx.author.id).add_roles(
                    discord.utils.get(guild.roles, id=1091326995280973845))
                role_ids.append(1091326995280973845)
        except json.decoder.JSONDecodeError:
            pass

        show_text = "ロールのチェックが完了しました。\n\n"

        if len(role_ids) == 0:
            show_text += "追加できるロールはありませんでした。"
        else:
            show_text += "以下のロールを追加しました。\n\n"
            for i in role_ids:
                show_text += f"<@&{i}>\n"
            if len(remove_ids) >= 1:
                show_text += "\n以下のロールは剥奪されました。\n\n"
                for i in remove_ids:
                    show_text += f"<@&{i}>\n"

        await show_embed.edit(
            embed=self.bot.edit_embed(show_embed, "Checking Finish!", f"{show_text}"))

    @commands.command()
    async def how_did_you_find_this_command(self, ctx):
        # 指定されたロールIDを取得
        role = ctx.guild.get_role(1211000756635959319)

        # サーバー全体のメンバーを取得
        members = ctx.guild.members

        # ロールを持っているかどうかを全メンバーに確認
        role_exists = any(role in member.roles for member in members)

        if role_exists:
            await ctx.send(f"既に `{role.name}` ロールは攻略されました。")
        else:
            # ロールを持っていない場合、コマンドを実行したメンバーにロールを付与
            await ctx.author.add_roles(role)
            msg = await ctx.send(f"@everyone\nおめでとう！{ctx.author.display_name}は、暗号を解読し、{role.mention} を入手した！")
            await msg.pin()


def setup(bot):
    bot.add_cog(ROLE_CHECK(bot))
