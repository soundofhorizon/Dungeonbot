import random
import re

import discord
import qrcode
from discord.ext import commands


class SimpleCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, qrcode_context):
        try:
            img = qrcode.make(f"{qrcode_context}")
            img.save("./icon.png")
            image = discord.File("./icon.png", filename="icon.png")
            embed = discord.Embed(description=f"作成結果",
                                  color=0x4259fb
                                  )
            embed.set_image(url="attachment://icon.png")
            await ctx.send(file=image, embed=embed, content="作成完了")
        except Exception:
            await ctx.send("QRコードに含めるデータ量が大きすぎます")

    @commands.command()
    async def sub_account(self, ctx):
        guild = self.bot.get_guild(730269755432239116)
        role1 = discord.utils.get(guild.roles, name="sub_account")
        role2 = discord.utils.get(guild.roles, name="ign未チェック")
        await ctx.author.remove_roles(role2)
        await ctx.author.add_roles(role1)
        await ctx.send("サブアカウントとして認識しました。")

    @commands.command()
    async def update(self, ctx):
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        uuid = ""
        for i,j in uuid_list:
            if j == ctx.author.id:
                uuid = i[1:]
                break

        nickname = str(ctx.author.display_name).replace("★", "")
        current_catacombs_level = nickname[1:6]
        mcid = str(nickname[6:]).replace(">", "")
        try:
            float(current_catacombs_level)
        except ValueError:
            current_catacombs_level = current_catacombs_level[:1]
        update_catacombs = await self.bot.check_catacombs_level(uuid)
        update_catacombs_level = update_catacombs[0]
        mem = self.bot.get_guild(730269755432239116).get_member(int(ctx.author.id))
        if not (str(update_catacombs_level) in nickname) and ctx.author.id != 449814227683639296:
            if update_catacombs_level == 1.00:
                await mem.edit(nick=f"<-->{mcid}")
            else:
                if float(update_catacombs_level) < 50:
                    await mem.edit(nick=f"<{update_catacombs_level}>{mcid}")
                else:
                    await mem.edit(nick=f"★<{update_catacombs_level}>{mcid}")
            if not ctx.channel.id == 783727171142156298:
                await ctx.send(
                    f"Your Catacombs Level is updated! {current_catacombs_level} to {update_catacombs_level}! :tada:")
                return
        elif not str(self.bot.uuid_to_mcid(uuid)) == mcid and ctx.author.id != 449814227683639296:
            if str(update_catacombs_level) == "1.00":
                await mem.edit(nick=f"<-->{self.bot.uuid_to_mcid(uuid)}")
            else:
                if float(update_catacombs_level) < 50:
                    await mem.edit(nick=f"<{update_catacombs_level}>{self.bot.uuid_to_mcid(uuid)}")
                else:
                    await mem.edit(nick=f"★<{update_catacombs_level}>{self.bot.uuid_to_mcid(uuid)}")
            if not ctx.channel.id == 783727171142156298:
                await ctx.send(
                    f"<:leaf_on_fire:731718802173198346> Your nickname is updated! {mcid} to {self.bot.uuid_to_mcid(uuid)}! <:leaf_on_fire:731718802173198346>")
        else:
            await ctx.send("Your status is already updated.")

    @commands.command()
    async def random_rgb(self, ctx):
        hex_chars = "0123456789ABCDEF"
        result = ''.join(random.choices(hex_chars, k=6))
        await ctx.send(f"#{result}")

    @commands.command()
    async def restart2(self, ctx):
        await ctx.send("restarting. please wait")
        await self.bot.close()

    @commands.command(name='dice')
    async def roll_dice(self, ctx, dice: str):
        # 全角を半角に変換
        dice = dice.translate(str.maketrans('０１２３４５６７８９ｄ＋', '0123456789d+'))

        # 正規表現でダイスのパターンを解析
        match = re.match(r'(\d+)d(\d+)((\+\d+d\d+)|(\+\d+))?', dice)
        if not match:
            await ctx.send('フォーマットが正しくありません。例: !dice 4d6, !dice 1d10+3, !dice 1d6+2d5')
            return

        number_of_dice = int(match.group(1))
        dice_size = int(match.group(2))
        modifier_dice = match.group(3)

        if number_of_dice >= 500:
            await ctx.send("diceの数が多すぎです。500個以内に収めてください。")
            return

        if dice_size >= 65537:
            await ctx.send("それはもう球ではないですか？サイコロの出目の指定は65537以下に収めてください。")
            return

        if number_of_dice <= 0 or dice_size <= 0:
            await ctx.send('ダイスの数とサイズは正の整数でなければなりません。')
            return

        # メインのダイスロール
        rolls = [random.randint(1, dice_size) for _ in range(number_of_dice)]
        roll_results = ' + '.join(map(str, rolls))
        total = sum(rolls)

        # 修正値としての追加ダイスロール
        if modifier_dice:
            if 'd' in modifier_dice:
                mod_match = re.match(r'\+(\d+)d(\d+)', modifier_dice)
                if mod_match:
                    mod_number_of_dice = int(mod_match.group(1))
                    mod_dice_size = int(mod_match.group(2))
                    if mod_number_of_dice >= 500:
                        await ctx.send("diceの数が多すぎです。500個以内に収めてください。")
                        return

                    if mod_dice_size >= 65537:
                        await ctx.send("それはもう球ではないですか？サイコロの出目の指定は65537以下に収めてください。")
                        return

                    if mod_number_of_dice <= 0 or mod_dice_size <= 0:
                        await ctx.send('ダイスの数とサイズは正の整数でなければなりません。')
                        return
                    mod_rolls = [random.randint(1, mod_dice_size) for _ in range(mod_number_of_dice)]
                    mod_roll_results = ' + '.join(map(str, mod_rolls))
                    mod_total = sum(mod_rolls)
                    total += mod_total
                    description = f'({roll_results}) + ({mod_roll_results}) ➤ {total}'
                else:
                    await ctx.send('フォーマットが正しくありません。例: !dice 1d6+2d5')
                    return
            else:
                modifier = int(modifier_dice[1:])
                total += modifier
                description = f'({roll_results}) + {modifier} ➤ {total}'
        else:
            description = f'{roll_results} ➤ {total}' if number_of_dice > 1 else f'{total}'

        embed = discord.Embed(title="ダイスロール結果", description=description, color=0xADFF2F)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(SimpleCommands(bot))
