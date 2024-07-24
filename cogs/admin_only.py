import asyncio
import datetime
import random
import re

import discord
from discord.ext import commands

"""Adminのみ使えるコマンド群"""


class AdminOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # cog内のコマンド全てに適用されるcheck
        if discord.utils.get(ctx.author.roles, name="admin") or discord.utils.get(ctx.author.roles, id=998197009515282493):
            return True
        await ctx.send('このコマンドは運営以外は使用禁止です・。・')
        return False


    @commands.command(aliases=["cca"])
    async def catacombs_check_all(self, ctx):
        player_data = await self.bot.db_select("player_data")  # player_data : [1] discordid, [0] uuid
        player_data = [[str(item[0]), int(item[1])] for item in player_data]
        for uuid, discord_id in player_data:
            if discord_id == 449814227683639296:
                continue

            mcid = self.bot.uuid_to_mcid(uuid[1:])
            catacombs_level_result = await self.bot.check_catacombs_level(uuid[1:])
            update_catacombs_level = catacombs_level_result[0]
            mem = self.bot.get_guild(730269755432239116).get_member(discord_id)
            if update_catacombs_level == 1.00:
                await mem.edit(nick=f"<-->{mcid}")
            else:
                nick_prefix = "<" if float(update_catacombs_level) < 50 else "★<"
                await mem.edit(nick=f"{nick_prefix}{update_catacombs_level}>{mcid}")
        await ctx.send("完了")

    @commands.command(aliases=["fe"])
    async def fishing_event(self, ctx, start_time_str):
        start_time = datetime.datetime.strptime(start_time_str, '%m/%d-%H:%M')
        event_times = [start_time + datetime.timedelta(hours=10, minutes=20) * i for i in range(12)]

        description = "Fishing event 開始時刻 (JST)\n-----------------------\n"
        for i, event_time in enumerate(event_times):
            description += f"{i+1}回目: {event_time.strftime('%m/%d-%H:%M')}\n"

        await self.bot.get_channel(740183927729160252).send(description)

    @commands.command(aliases=["del"])
    async def _del(self, ctx, n):  # メッセージ削除用
        p = re.compile(r'^[0-9]+$')
        if p.fullmatch(n):
            count = int(n)
            await ctx.channel.purge(limit=count + 1)

    @commands.command()
    async def clean_sql(self, ctx):
        await ctx.send("実行中")
        player_data = await self.bot.db_select("player_data")  # player_data : [0] uuid, [1] discord_id
        left_mcid = []
        for uuid, discord_id in player_data:
            mcid = self.bot.uuid_to_mcid(uuid[1:])
            member = self.bot.get_guild(ctx.guild.id).get_member(int(discord_id))
            if not member:  # memberが存在しない場合は削除する
                player_data.remove(["uuid", discord_id])
                left_mcid.append(mcid)
                continue
        if left_mcid:
            message = ""
            for i in player_data:
                message += f"{i[0]} {i[1]}\n"
            await ctx.send(f"以下のmcidは退会していたのでデータを削除しました。{left_mcid}")
        else:
            await ctx.send("処理が終わりました。退会者は…誰一人いませんでした…")

    @commands.command()
    async def rr(self, ctx, check_role: discord.Role, member_id):
        i = 0
        if member_id == "a":
            for mem in check_role.members:
                i += 1
                await mem.remove_roles(check_role)
            embed = discord.Embed(
                description=f"{ctx.author.display_name}により、\n"
                            f"{i}人の{check_role.name}役職\n"
                            f"をはく奪しました。",
                color=0x006400)
            await ctx.send(embed=embed)
        else:
            try:
                member = discord.utils.get(ctx.guild.members, id=int(member_id))
                if discord.utils.get(member.roles, id=check_role.id):
                    await member.remove_roles(check_role)
                    embed = discord.Embed(
                        description=f"{ctx.author.display_name}により、\n"
                                    f"{member.display_name}から\n"
                                    f"{check_role.name}をはく奪しました。",
                        color=0x006400)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"{member.display_name}は{check_role.name}を所持していません。")
            except ValueError:
                await ctx.send("引数が不正です。リファレンスを読み直してください。")
            except discord.errors.HTTPException:
                await ctx.send("空白は一つだけ有効です。(Roleをメンションで挿入した際に空白を更に一つ開けていませんか？)")

    @commands.command()
    async def cr(self, ctx, hex_num: str, create_role_name: str):

        def html2rgb(color_code):
            R = int(color_code[0:2], 16)
            G = int(color_code[2:4], 16)
            B = int(color_code[4:6], 16)
            return [R, G, B]

        def check(m):
            if m.author.bot:
                return
            return m.channel == ctx.channel

        role_color_RGB = html2rgb(hex_num.replace("#", ""))
        await ctx.guild.create_role(name=create_role_name,
                                    colour=discord.Colour.from_rgb(role_color_RGB[0], role_color_RGB[1],
                                                                   role_color_RGB[2]))
        await ctx.send("ロール情報を受け取りました。次にどの位置に配置するかを番号で入力してください。")
        description = ""
        guild_roles = ctx.guild.roles
        guild_roles.reverse()  # ロールを格式が高い順に並び替え
        for i in range(len(guild_roles) - 1):
            description += f"{guild_roles[i].name}\n"
            description += f"<{guild_roles[i].position}>\n"
        embed = discord.Embed(description=description, color=0x006400)
        await ctx.send(embed=embed)

        user_select_input = await self.bot.wait_for('message', check=check)
        user_select_input = user_select_input.content

        role_position = {discord.utils.get(ctx.guild.roles, name=create_role_name): int(user_select_input)}
        await ctx.guild.edit_role_positions(positions=role_position)
        embed = discord.Embed(
            description=f"{ctx.author.display_name}により、\n"
                        f"{create_role_name}ロールを作成しました。",
            color=0x006400)
        await ctx.send(embed=embed)

    @commands.command()
    async def dr(self, ctx, delete_role: discord.Role):
        delete_role = discord.utils.get(ctx.guild.roles, id=delete_role.id)
        embed = discord.Embed(
            description=f"{ctx.author.display_name}により、\n"
                        f"{delete_role.name}ロールを削除しました。",
            color=0x006400)
        await asyncio.sleep(0.5)
        await delete_role.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def restart(self, ctx):
        await ctx.send("restarting ")
        await self.bot.close()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("1 2023/08/20T16:15:00")

    @commands.command()
    async def mmo_init(self, ctx):
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        player_data = ""
        for i in uuid_list:
            player_data += f"{i[1]} 0 1 0 100000000000000 150 0 0\n"
        await self.bot.db_insert("mmorpg", player_data)

    @commands.command()
    async def odds_init(self, ctx):
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        player_data = ""
        for i in uuid_list:
            player_data += f"{i[1]} 0 0 {random.randint(0, 1)} |\n"
        await self.bot.db_insert("odd", player_data)


def setup(bot):
    bot.add_cog(AdminOnly(bot))
