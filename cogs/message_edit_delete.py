from datetime import datetime

from discord import Embed
from discord.ext import commands


class MessageEditDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        if message.content.startswith("!tend"):
            return

        d = datetime.now()  # 現在時刻の取得
        time = d.strftime("%Y/%m/%d %H:%M:%S")
        embed = Embed(description=f'**Deleted in <#{message.channel.id}>**\n\n{message.content}\n\n',
                      color=0xff0000)  # 発言内容をdescriptionにセット
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        uuid = ""
        for i,j in uuid_list:
            if j == message.author.id:
                uuid = i[1:]
                break
        mcid = self.bot.uuid_to_mcid(uuid[0][1:])
        embed.set_author(name=message.author, icon_url=f"https://cravatar.eu/helmhead/{mcid}", )  # ユーザー名+ID,アバターをセット
        embed.set_footer(text=f'User ID：{message.author.id}\nTime：{time}')  # チャンネル名,時刻,鯖のアイコンをセット
        ch = message.guild.get_channel(768884671869878313)
        await ch.send(embed=embed)

    @commands.Cog.listener()  # point付与の術
    async def on_message_edit(self, before, after):

        # メッセージ送信者がBotだった場合は無視する
        if before.author.bot:
            return
        # URLの場合は無視する
        if "http" in before.content:
            return

        d = datetime.now()  # 現在時刻の取得
        time = d.strftime("%Y/%m/%d %H:%M:%S")
        # 発言内容をdescriptionにセット
        embed = Embed(
            description=f'**Changed in <#{before.channel.id}>**\n\n'
                        f'**before**\n{before.content}\n\n'
                        f'**after**\n{after.content}\n\n',
            color=0x1e90ff
        )
        uuid_list = await self.bot.db_select("player_data")
        uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]
        uuid = ""
        for i,j in uuid_list:
            if j == before.author.id:
                uuid = i[1:]
                break
        mcid = self.bot.uuid_to_mcid(uuid[0][1:])
        embed.set_author(name=before.author, icon_url=f"https://cravatar.eu/helmhead/{mcid}", )  # ユーザー名+ID,アバターをセット
        embed.set_footer(text=f'User ID：{before.author.id}\nTime：{time}')  # チャンネル名,時刻,鯖のアイコンをセット
        ch = before.guild.get_channel(768884671869878313)
        await ch.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageEditDelete(bot))
