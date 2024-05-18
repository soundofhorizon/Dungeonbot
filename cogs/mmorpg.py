import asyncio
import random
from typing import Any, List

import discord
from discord.ext import commands


class CustomException(Exception):
    pass


def colon_formatted_number(number: int) -> str:
    return "{:,}".format(number)


class Mmorpg(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_embed(self, ctx: commands.Context, title: str, description: str) -> discord.Message:
        embed = discord.Embed(title=title, description=description, color=0x3dc3a2)
        return await ctx.send(embed=embed)

    async def add_reactions(self, message: discord.Message, reactions: List[str]):
        for reaction in reactions:
            await message.add_reaction(reaction)

    async def wait_for_reaction(self, ctx: commands.Context, message: discord.Message, valid_reactions: List[str]):
        def check(reaction: discord.Reaction, user: discord.User):
            return user == ctx.author and str(reaction.emoji) in valid_reactions and reaction.message.id == message.id

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
            return str(reaction.emoji)
        except asyncio.TimeoutError:
            await ctx.send("時間切れです。もう一度お試しください。")
            return None

    async def clear_reactions(self, message: discord.Message):
        try:
            await message.clear_reactions()
        except discord.errors.Forbidden:
            for reaction in message.reactions:
                await message.remove_reaction(reaction.emoji, self.bot.user)

    @commands.command()
    async def mr(self, ctx: commands.Context):
        try:
            mmo_data = await self.bot.db_select("mmorpg")

            uuid_list = [
                [str(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]), int(item[5]), int(item[6]), int(item[7])]
                for item in mmo_data
            ]

            for player in uuid_list:
                if player[0] == str(ctx.author.id):
                    await self.handle_player(ctx, player)
                    break
            else:
                pass

            player_data = "\n".join(" ".join(map(str, player)) for player in uuid_list)
            await self.bot.db_insert("mmorpg", player_data)

        except Exception as e:
            await self.send_embed(ctx, "Error", f"Request Error. 少々お待ちいただき再度お試しください。\n\n{e}")

    async def handle_player(self, ctx: commands.Context, player_data: List[Any]):
        i, j, k, l, m, n, o, p = player_data

        description = (
            f"{ctx.author.display_name}さんの攻撃回数は{colon_formatted_number(j)}回、strは{colon_formatted_number(k)}、"
            f"manaは{colon_formatted_number(p)}、お金は{colon_formatted_number(l)}coinsです。\n\n"
            "あなたはラスボスに挑むこともできるし、子分と戦うこともできます。\n\n"
            ":regional_indicator_l: ラスボスに挑む\n:regional_indicator_w: 子分と戦う\n:regional_indicator_s: ショップ"
        )
        show_embed = await self.send_embed(ctx, "選択", description)
        await self.add_reactions(show_embed, ["🇱", "🇼", "🇸"])

        reaction = await self.wait_for_reaction(ctx, show_embed, ["🇱", "🇼", "🇸"])
        await self.clear_reactions(show_embed)

        if reaction == "🇱":
            await self.handle_boss_battle(ctx, show_embed, player_data)
        elif reaction == "🇼":
            await self.handle_minion_battle(ctx, show_embed, player_data)
        elif reaction == "🇸":
            await self.handle_shop(ctx, show_embed, player_data)

    async def handle_boss_battle(self, ctx: commands.Context, show_embed: discord.Message, player_data: List[Any]):
        i, j, k, l, m, n, o, p = player_data
        description = f"貴方はラスボスに遭遇した。ラスボスのHPは残り{colon_formatted_number(m)}。\n攻撃を行うなら:regional_indicator_a: と入力せよ。"
        await self.safe_edit_embed(show_embed, "ラスボスPhase", description)
        await self.add_reactions(show_embed, ["🇦"])

        reaction = await self.wait_for_reaction(ctx, show_embed, ["🇦"])
        await self.clear_reactions(show_embed)

        if reaction == "🇦":
            await self.process_attack(ctx, show_embed, player_data, is_boss=True)

    async def handle_minion_battle(self, ctx: commands.Context, show_embed: discord.Message, player_data: List[Any]):
        i, j, k, l, m, n, o, p = player_data
        weak_boss_name = ["子分", "魔法使い", "スリの銀次", "メタル子分"]
        description = (
            f"貴方はラスボスの子分の{weak_boss_name[o]}に遭遇した。{weak_boss_name[o]}のHPは残り{colon_formatted_number(n)}。\n"
            "攻撃を行うなら:regional_indicator_a: と入力せよ。"
        )
        await self.safe_edit_embed(show_embed, "子分Phase", description)
        await self.add_reactions(show_embed, ["🇦"])

        reaction = await self.wait_for_reaction(ctx, show_embed, ["🇦"])
        await self.clear_reactions(show_embed)

        if reaction == "🇦":
            await self.process_attack(ctx, show_embed, player_data, is_boss=False)

    async def process_attack(self, ctx: commands.Context, show_embed: discord.Message, player_data: List[Any], is_boss: bool):
        i, j, k, l, m, n, o, p = player_data
        multiplied_dmg = random.randint(0, 20)
        multiplied_money = random.random() / random.randint(1, 8)
        multiAttack_frag = random.randint(0, 1)
        damage = k * multiplied_dmg if multiAttack_frag == 0 else k
        coins = k * multiplied_dmg * multiplied_money if multiAttack_frag == 0 else k * multiplied_money

        if is_boss:
            remaining_hp = m - damage
            enemy_name = "ラスボス"
            hp_label = "ラスボスの残りHP"
            boss_defeated_msg = (
                f"<@!{ctx.author.id}> さんがラスボスを打倒しました！おめでとうございます！:tada:\n\n"
                "次回は強くてラスボスも強いニューゲーム！\n ラスボスHPは 6000000000000000, strは20から開始です。頑張ってね！"
            )
        else:
            remaining_hp = n - damage
            enemy_name = ["子分", "魔法使い", "スリの銀次", "メタル子分"][o]
            hp_label = f"{enemy_name}の残りHP"
            boss_defeated_msg = (
                f"{enemy_name}が殲滅された！ボーナスコイン{colon_formatted_number(int(coins))}coins獲得！\n\n"
                "ラスボス < まだまだ…私には遠い… 子分はまだまだいるからな…"
            )

        await self.safe_edit_embed(
            show_embed, "攻撃！", f"{ctx.author.display_name}の攻撃！\n{colon_formatted_number(damage)}のダメージ！\n\n{hp_label}: {colon_formatted_number(remaining_hp)}\n獲得coins: {colon_formatted_number(int(coins))}"
        )

        if remaining_hp <= 0:
            await ctx.send(boss_defeated_msg)
            if is_boss:
                player_data[1:] = [0, 20, 0, 6000000000000000, 1000, 0, 0]
            else:
                # Logic for handling minion battle victory
                pass
        else:
            if is_boss:
                player_data[1:5] = [j + 1, k, l + int(coins), remaining_hp]
            else:
                player_data[1:7] = [j + 1, k, l + int(coins), m, remaining_hp, o]

    async def handle_shop(self, ctx: commands.Context, show_embed: discord.Message, player_data: List[Any]):
        i, j, k, l, m, n, o, p = player_data
        description = (
            "何を買いたいの？\n\n"
            ":regional_indicator_s: strを1増加 (100coins)\n"
            ":regional_indicator_m: manaを1増加 (50coins)\n"
            ":regional_indicator_p: 終了"
        )
        await self.safe_edit_embed(show_embed, "SHOP", description)
        await self.add_reactions(show_embed, ["🇸", "🇲", "🇵"])

        reaction = await self.wait_for_reaction(ctx, show_embed, ["🇸", "🇲", "🇵"])
        await self.clear_reactions(show_embed)

        if reaction == "🇸":
            await self.process_shop_purchase(ctx, show_embed, player_data, item="str")
        elif reaction == "🇲":
            await self.process_shop_purchase(ctx, show_embed, player_data, item="mana")
        elif reaction == "🇵":
            await self.safe_edit_embed(show_embed, "SHOP", "そっか…また来てね。")

    async def process_shop_purchase(self, ctx: commands.Context, show_embed: discord.Message, player_data: List[Any], item: str):
        i, j, k, l, m, n, o, p = player_data
        item_cost = {"str": 100, "mana": 50}
        if l >= item_cost[item]:
            player_data[2 if item == "str" else 7] += 1
            player_data[3] -= item_cost[item]
            await self.safe_edit_embed(
                show_embed,
                "SHOP",
                f"SHOPで {item} を購入しました。\n\n 現在の所持{item}: {colon_formatted_number(player_data[2 if item == str else 7])}"
            )
        else:
            await self.safe_edit_embed(show_embed, "SHOP", f"コインが足りません。必要なコイン: {colon_formatted_number(item_cost[item])}")

    async def safe_edit_embed(self, message: discord.Message, title: str, description: str):
        try:
            await message.edit(embed=self.bot.edit_embed(message, title, description))
        except discord.errors.NotFound:
            await self.send_embed(message.channel, title, description)

def setup(bot):
    bot.add_cog(Mmorpg(bot))