import random
import re
import traceback
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        try:
            # Secret Role
            check = random.randint(1, 1000000)
            if 999900 <= check <= 999999:
                await message.guild.get_channel(1214065130988503112).send(f"{check} : {message.author.display_name}")
            elif check == 1000000:
                role = message.guild.get_role(1192898828764971149)
                await message.author.add_roles(role)
                msg = await message.channel.send(
                    f"@everyone\nおめでとう！{message.author.display_name}は、0.0001%の壁を乗り越え、{role.mention} を入手した！\n(条件開放: メッセージ送信毎抽選、1/1000000で当選する)")
                await msg.pin()

            # 引用機能
            url_filter = [msg.split("/")[1:] for msg in
                          re.split("https://(ptb.|canary.|)discord(app|).com/channels/730269755432239116((/[0-9]+){2})",
                                   message.content)
                          if re.match("(/[0-9]+){2}", msg)]
            if len(url_filter) >= 1:
                for url in url_filter:
                    try:
                        channel_id = int(url[0])
                        message_id = int(url[1])
                        ch = message.guild.get_channel(channel_id)
                        if ch is None:
                            continue
                        msg = await ch.fetch_message(message_id)

                        def quote_reaction(msg, embed):
                            if msg.reactions:
                                reaction_send = ''
                                for reaction in msg.reactions:
                                    emoji = reaction.emoji
                                    count = str(reaction.count)
                                    reaction_send = f'{reaction_send}{emoji}{count} '
                                embed.add_field(name='reaction', value=reaction_send, inline=False)
                            return embed

                        if msg.embeds or msg.content or msg.attachments:
                            embed = Embed(description=msg.content, timestamp=msg.created_at)
                            embed.set_author(name=msg.author, icon_url=msg.author.avatar)
                            embed.set_footer(text=msg.channel.name, icon_url=msg.guild.icon)
                            if msg.attachments:
                                embed.set_image(url=msg.attachments[0].url)
                            embed = quote_reaction(msg, embed)
                            if msg.content or msg.attachments:
                                await message.channel.send(embed=embed)
                            if len(msg.attachments) >= 2:
                                for attachment in msg.attachments[1:]:
                                    embed = Embed().set_image(url=attachment.url)
                                    await message.channel.send(embed=embed)
                            for embed in msg.embeds:
                                embed = quote_reaction(msg, embed)
                                await message.channel.send(embed=embed)
                        else:
                            await message.channel.send('メッセージIDは存在しますが、内容がありません')
                    except discord.errors.NotFound:
                        await message.channel.send("指定したメッセージが見つかりません")
        except Exception:
            error_message = f'```{traceback.format_exc()}```'
            ch = message.guild.get_channel(628807266753183754)
            d = datetime.now()  # 現在時刻の取得
            time = d.strftime("%Y/%m/%d %H:%M:%S")
            embed = Embed(title='Error_log', description=error_message, color=0xf04747)
            embed.set_footer(text=f'channel:{message.channel}\ntime:{time}\nuser:{message.author.display_name}')
            await ch.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Message(bot))
