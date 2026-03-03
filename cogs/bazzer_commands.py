import asyncio

import discord
from discord.ext import commands

"""Eventの期間を検索するコマンド"""


class BazzerCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cb(self, ctx, search_text: str):

        def check(m):
            if m.author.bot:
                return
            return m.channel == ctx.channel and m.author == ctx.author

        show_embed_description = "Starting..."
        embed = discord.Embed(
            description=show_embed_description,
            color=0x61c1a9)
        show_embed = await ctx.send(embed=embed)
        await asyncio.sleep(0.1)
        url = "https://api.hypixel.net/v2/skyblock/bazaar"
        jsonData = self.bot.request_json_get(url, timeout=3.0)

        transfer_list_before = ["LOG:1", "LOG:2", "LOG:3", "LOG_2:1", "LOG_2", "INK_SACK:3", "INK_SACK:4",
                                "RAW_FISH:3", "RAW_FISH:2", "RAW_FISH:1", "SULPHUR"]
        transfer_list_after = ["SPRUCE_WOOD", "BRICH_WOOD", "JUNGLE_WOOD", "DARK_OAK_WOOD", "ACACIA WOOD",
                               "COCOA_BEANS", "LAPIS_LAZULI", "PUFFER_FISH", "CLOWN_FISH", "RAW_SALMON",
                               "GUN_POWDER"]

        # もし、API disableなどの理由で死んでいるときはここで通知して終わる。
        if not jsonData["success"]:
            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "APIは現在disableです。時間をおいて再度実行してください。"))
            return
        # このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
        # JSONでの名前を指定することで情報がとってこれる
        key_list = list(jsonData["products"])

        # 変な形の単語をみんながわかる単語に変換する
        for i in range(len(key_list)):
            for j in range(len(transfer_list_before)):
                if transfer_list_before[j] in key_list[i]:
                    key_list[i] = transfer_list_after[j]
                    continue

        search_result = [i for i in key_list if (search_text.upper() in i)]

        select_description = ""
        num = 1
        user_select_input = 1
        if len(search_result) >= 2:
            for j in search_result:
                select_description += f"{num}: {j.lower()}\n"
                num += 1

            if len(select_description) <= 2000:
                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "検索したいアイテムはどれですか", select_description))
                user_select_input = await self.bot.wait_for("message", check=check)
                user_select_input = user_select_input.content
                try:
                    if int(user_select_input) <= 0 or num < int(user_select_input):
                        await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "指定した番号が範囲外です。\nSession closed."))
                        return
                except ValueError:
                    await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "検索したいアイテムを「番号」で入力してください。\nSession closed."))
                    return
            else:
                await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "検索結果が多すぎます。検索単語を絞ってください。"))
                return
            await ctx.channel.purge(limit=1)
        elif len(search_result) == 1:
            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Success", f"{search_result[int(user_select_input) - 1].lower()}の1件のみがヒットしました。1秒後にBuy/Sell表示します。"))
            await asyncio.sleep(1)
        else:
            await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Error", "検索しましたが、該当アイテムがありませんでした。検索単語を確かめ、再度実行してください。"))
            return
        await show_embed.edit(embed=self.bot.edit_embed(show_embed, "Success", f"{search_result[int(user_select_input) - 1].lower()}の直近のBuy/Sellを表示します。"))

        # 検索を賭けるため元の状態にする
        for i in range(len(search_result)):
            for j in range(len(transfer_list_after)):
                if transfer_list_after[j] in search_result[i]:
                    search_result[i] = transfer_list_before[j]
                    continue

        # buy
        sell_description = "```yaml\n"
        sell_summary = jsonData["products"][search_result[int(user_select_input) - 1]]["sell_summary"]
        for i in range(len(sell_summary)):
            sell_description += f"{i + 1}: 単価 {sell_summary[i]['pricePerUnit']}, 個数 {sell_summary[i]['amount']}\n"
        sell_description += "```"
        embed = discord.Embed(title="Buy Offer", description=sell_description, color=0x55FF55)
        await ctx.send(embed=embed)
        # sell
        buy_description = "```yaml\n"
        buy_summary = jsonData["products"][search_result[int(user_select_input) - 1]]["buy_summary"]
        for i in range(len(buy_summary)):
            buy_description += f"{i + 1}: 単価 {buy_summary[i]['pricePerUnit']}, 個数 {buy_summary[i]['amount']}\n"
        buy_description += "```"
        embed = discord.Embed(title="Sell Offer", description=buy_description, color=0xFFAA00)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BazzerCommands(bot))
