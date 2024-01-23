import asyncio
import random

import discord
from discord.ext import commands


class CustomException(Exception):
    pass


# player_data 0:discord_id 1: 攻撃回数 2: str 3: money 4: last boss hp 5: weak boss hp 6: weak boss status(0 normal 1 str debuff 2 money debuff 3 rare boss)) 7: mana
class Mmorpg(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mr(self, ctx):
        try:
            mmo_data = await self.bot.db_select("mmorpg")

            def check1(m):
                return m.channel == ctx.channel and m.author == ctx.author and m.content == "L" or m.content == "W" or m.content == "S"

            def check2(m):
                return m.channel == ctx.channel and m.author == ctx.author and m.content == "A"

            def check3(m):
                return m.channel == ctx.channel and m.author == ctx.author and m.content == "C" or m.content == "P"

            def colon_formatted_number(number):
                formatted_number = "{:,}".format(number)
                return formatted_number

            uuid_list = [
                [str(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]), int(item[5]), int(item[6]),
                 int(item[7])] for item in mmo_data]
            player_data = ""
            for i, j, k, l, m, n, o, p in uuid_list:
                temp_player_data = f"{i} {j} {k} {l} {m} {n} {o} {p}"
                if i == str(ctx.author.id):
                    show_embed_description = f"{ctx.author.display_name}さんの攻撃回数は{colon_formatted_number(j)}回、strは{colon_formatted_number(k)}、manaは{colon_formatted_number(p)}、お金は{colon_formatted_number(l)}coinsです。\n\nあなたはラスボスに挑むこともできるし、子分と戦うこともできます。\n\nラスボスならL, 子分ならW, ショップならSと打ってください。"
                    embed = discord.Embed(
                        description=show_embed_description,
                        color=0x3dc3a2)
                    show_embed = await ctx.send(embed=embed)
                    response = await self.bot.wait_for('message', check=check1)

                    # ラスボス関係
                    if response.content == "L":
                        await ctx.channel.purge(limit=1)
                        await show_embed.edit(embed=self.bot.edit_embed(show_embed, "ラスボスPhase",
                                                                        f"貴方はラスボスに遭遇した。ラスボスのHPは残り{colon_formatted_number(m)}。\n攻撃を行うなら**A**と入力せよ。"))
                        response = await self.bot.wait_for('message', check=check2)
                        if response.content == "A":
                            await ctx.channel.purge(limit=1)
                            multiplied_dmg = random.randint(0, 20)
                            multiplied_money = random.random() / random.randint(1, 8)
                            multiAttack_frag = random.randint(0, 1)
                            if multiAttack_frag == 0:
                                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "攻撃！",
                                                                                f"{ctx.author.display_name}の攻撃！\n{multiplied_dmg}倍攻撃！ラスボスに{colon_formatted_number(k * multiplied_dmg)}のダメージ！\n\nラスボスの残りHP: {colon_formatted_number(m - (k * multiplied_dmg))}\n獲得coins: {colon_formatted_number(int(k * multiplied_dmg * multiplied_money))}"))
                                if m - (k * multiplied_dmg) <= 0:
                                    await ctx.send(
                                        f"<@!{ctx.author.id}> さんがラスボスを打倒しました！おめでとうございます！:tada:\n\n次回は強くてラスボスも強いニューゲーム！\n ラスボスHPは 6000000000000000, strは20から開始です。頑張ってね！")
                                    temp_player_data = f"{i} {0} {20} {0} {6000000000000000} {1000} {0} {0}"
                                else:
                                    temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_dmg * multiplied_money)} {m - (k * multiplied_dmg)} {n} {o} {p}"
                            else:
                                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "攻撃！",
                                                                                f"{ctx.author.display_name}の攻撃！\nラスボスに{colon_formatted_number(k)}のダメージ！\n\nラスボスの残りHP: {colon_formatted_number(m - (k))}\n獲得coins: {colon_formatted_number(int(k * multiplied_money))}"))
                                if m - (k) <= 0:
                                    await ctx.send(
                                        f"<@!{ctx.author.id}> さんがラスボスを打倒しました！おめでとうございます！:tada:\n\n次回は強くてラスボスも強いニューゲーム！\n ラスボスHPは 6000000000000000, strは20から開始です。頑張ってね！")
                                    temp_player_data = f"{i} {0} {20} {0} {6000000000000000} {1000} {0} {0}"
                                else:
                                    temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money)} {m - (k)} {n} {o} {p}"


                    # 子分関係
                    elif response.content == "W":
                        weak_boss_name = ["子分", "魔法使い", "スリの銀次", "メタル子分"]
                        await ctx.channel.purge(limit=1)
                        await show_embed.edit(embed=self.bot.edit_embed(show_embed, "子分Phase",
                                                                        f"貴方はラスボスの子分の{weak_boss_name[o]}に遭遇した。{weak_boss_name[o]}のHPは残り{colon_formatted_number(n)}。\n攻撃を行うなら**A**と入力せよ。"))
                        response = await self.bot.wait_for('message', check=check2)
                        if response.content == "A":

                            # 攻撃関数
                            async def Attack(enemy_type, show_embed, temp_player_data):
                                i, j, k, l, m, n, o, p = temp_player_data.split(" ")
                                temp_player_data = ""
                                multiplied_dmg = random.randint(0, 20)
                                multiplied_money = random.random() / random.randint(1, 8)
                                multiAttack_frag = random.randint(0, 1)
                                if multiAttack_frag == 0:
                                    description = f"{ctx.author.display_name}の攻撃！\n{multiplied_dmg}倍攻撃！{weak_boss_name[o]}に{colon_formatted_number(k * multiplied_dmg)}のダメージ！\n\n{weak_boss_name[o]}の残りHP: {colon_formatted_number(n - (k * multiplied_dmg))}\n獲得coins: {colon_formatted_number(int(k * multiplied_dmg * multiplied_money))}"
                                    if n - (k * multiplied_dmg) <= 0:
                                        if o == 3:
                                            bonus = random.randint(50, 200) * k
                                        else:
                                            bonus = random.randint(5, 20) * k
                                        nexthp = k * random.randint(50, 830)
                                        next_weakboss = random.randint(0, 100)
                                        description += f"\n\n{weak_boss_name[o]}が殲滅された！ボーナスコイン{colon_formatted_number(bonus)}coins獲得！\n\nラスボス < まだまだ…私には遠い… 子分はまだまだいるからな…"
                                        await ctx.send(embed=self.bot.edit_embed(show_embed, "攻撃！", description))
                                        if next_weakboss <= 50:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {0} {p}"
                                        elif 50 < next_weakboss <= 72:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {1} {p}"
                                        elif 72 < next_weakboss <= 95:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {2} {p}"
                                        elif 95 < next_weakboss <= 100:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {3} {p}"
                                        raise CustomException(temp_player_data)
                                    else:
                                        await ctx.send(embed=self.bot.edit_embed(show_embed, "攻撃！", description))
                                        temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_dmg * multiplied_money)} {m} {n - (k * multiplied_dmg)} {o} {p}"
                                else:
                                    description = f"{ctx.author.display_name}の攻撃！\n{weak_boss_name[o]}に{colon_formatted_number(k)}のダメージ！\n\n{weak_boss_name[o]}の残りHP: {colon_formatted_number(n - (k))}\n獲得coins: {colon_formatted_number(int(k * multiplied_money))}"
                                    if n - (k) <= 0:
                                        if o == 3:
                                            bonus = random.randint(50, 200) * k
                                        else:
                                            bonus = random.randint(5, 20) * k
                                        nexthp = k * random.randint(50, 830)
                                        next_weakboss = random.randint(0, 100)
                                        description += f"\n\n{weak_boss_name[o]}が殲滅された！ボーナスコイン{colon_formatted_number(bonus)}coins獲得！\n\nラスボス < まだまだ…私には遠い… 子分はまだまだいるからな…"
                                        await ctx.send(embed=self.bot.edit_embed(show_embed, "攻撃！", description))
                                        if next_weakboss <= 50:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {0} {p}"
                                        elif 50 < next_weakboss <= 72:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {1} {p}"
                                        elif 72 < next_weakboss <= 95:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {2} {p}"
                                        elif 95 < next_weakboss <= 100:
                                            temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money + bonus)} {m} {nexthp} {3} {p}"
                                        raise CustomException(temp_player_data)
                                    else:
                                        await ctx.send(embed=self.bot.edit_embed(show_embed, "攻撃！", description))
                                        temp_player_data = f"{i} {j + 1} {k} {l + int(k * multiplied_money)} {m} {n - (k)} {o} {p}"

                                return temp_player_data

                            async def EnemyAttack(Type, show_embed, temp_player_data):
                                weak_boss_name = ["ノーマル子分", "魔法使い", "スリの銀次", "メタル子分"]
                                if Type == 0:
                                    description = f"{weak_boss_name[Type]}は相手の様子を伺っている…"
                                    await show_embed.edit(
                                        embed=self.bot.edit_embed(show_embed, "Enemy Turn", description))
                                elif Type == 1:
                                    description = f"{weak_boss_name[Type]}が呪文を詠唱している…"
                                    await show_embed.edit(
                                        embed=self.bot.edit_embed(show_embed, "Enemy Turn", description))
                                    await asyncio.sleep(random.randint(2, 4))
                                    ishit = random.randint(0, 100)
                                    if ishit > 80:
                                        str_debuff = random.randint(5, 30)
                                        description = f"{weak_boss_name[Type]}の攻撃！\n自分のstrが{str_debuff}%減少した!"
                                        await show_embed.edit(
                                            embed=self.bot.edit_embed(show_embed, "Enemy Attack!", description))
                                        temp_player_data = f"{i} {j} {int(k * ((100 - str_debuff) / 100))} {l} {m} {n} {o} {p}\n"
                                    else:
                                        description = f"どうやら何も起こらなかったようだ…"
                                        await show_embed.edit(
                                            embed=self.bot.edit_embed(show_embed, "Enemy Attack!", description))
                                elif Type == 2:
                                    description = f"{weak_boss_name[Type]}は不敵な笑みを浮かべている…"
                                    await show_embed.edit(
                                        embed=self.bot.edit_embed(show_embed, "Enemy Turn", description))
                                    await asyncio.sleep(random.randint(2, 4))
                                    isthief = random.randint(0, 100)
                                    if isthief <= 85:
                                        money_debuff = random.randint(40, 100)
                                        description = f"{weak_boss_name[Type]}は{colon_formatted_number(int(l * (money_debuff / 100)))}coinsスっていった！なんて奴だ！"
                                        await show_embed.edit(
                                            embed=self.bot.edit_embed(show_embed, "Enemy Attack!", description))
                                        temp_player_data = f"{i} {j} {k} {int(l - (l * (money_debuff) / 100))} {m} {n} {o} {p}"
                                    else:
                                        description = f"どうやら何も起こらなかったようだ…"
                                        await show_embed.edit(
                                            embed=self.bot.edit_embed(show_embed, "Enemy Attack!", description))
                                elif Type == 3:
                                    isescape = random.randint(0, 100)
                                    if isescape > 95:
                                        description = f"{weak_boss_name[Type]}は不思議な力により、ノーマル子分になってしまった！残念！"
                                        await show_embed.edit(
                                            embed=self.bot.edit_embed(show_embed, "Enemy Turn", description))
                                        temp_player_data = f"{i} {j} {k} {l} {m} {n} {0} {p}"
                                    description = f"{weak_boss_name[Type]}は相手の様子を伺っている…"
                                    await show_embed.edit(
                                        embed=self.bot.edit_embed(show_embed, "Enemy Turn", description))

                                return temp_player_data

                            await ctx.channel.purge(limit=1)
                            try:
                                temp_player_data = await EnemyAttack(o, show_embed, temp_player_data)
                                print(temp_player_data)
                                await asyncio.sleep(2)
                                temp_player_data = await Attack(o, show_embed, temp_player_data)
                            except CustomException as e:
                                player_data += f"{e}\n"
                                continue

                    # SHOP関係
                    elif response.content == "S":
                        await ctx.channel.purge(limit=1)
                        await show_embed.edit(embed=self.bot.edit_embed(show_embed, "SHOP",
                                                                        f"ここは、貴方が持っている全てのcoinsを生贄にし、random.randint(0,yourcoins)×random.random()で決定されたstr分加算されるSHOPだよ…\n\n …やってくかい？\n\nstrを購入するならP, 中止するならCを入力せよ。\n\n 貴方の所持コイン: {colon_formatted_number(l)}coins"))
                        response = await self.bot.wait_for('message', check=check3)
                        if response.content == "P":
                            await ctx.channel.purge(limit=1)
                            await show_embed.edit(
                                embed=self.bot.edit_embed(show_embed, "Purchase Processing...", "ひひひ…"))
                            await asyncio.sleep(3)
                            div_str = random.randint(1, 4)
                            result = int(random.randint(0, int(l / div_str)) * random.random())
                            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Purchase Complete!",
                                                                            f"{ctx.author.display_name}のstrが{colon_formatted_number(result)}上昇した！"))
                            temp_player_data = f"{i} {j} {k + result} {0} {m} {n} {o} {p}"
                        elif response.content == "C":
                            await show_embed.edit(
                                embed=self.bot.edit_embed(show_embed, "Purchase Cancelled", "ちっ…冷やかしか…"))
                            temp_player_data = f"{i} {j} {k} {l} {m} {n} {o} {p}"

                    player_data += f"{temp_player_data}\n"
                else:
                    player_data += f"{i} {j} {k} {l} {m} {n} {o} {p}\n"

            await self.bot.db_insert("mmorpg", player_data)
        except Exception as e:
            await show_embed.edit(
                embed=self.bot.edit_embed(show_embed, "Error", f"Request Error. 少々お待ちいただき再度お試しください。\n\n{e}"))

    @commands.command()
    async def mmo_init(self, ctx):
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        player_data = ""
        for i in uuid_list:
            player_data += f"{i[1]} 0 1 0 100000000000000 150 0 0\n"
        await self.bot.db_insert("mmorpg", player_data)


def setup(bot):
    bot.add_cog(Mmorpg(bot))
