import discord
from discord.ext import commands
from discord.ui import View


class PCommandView(View):

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    @discord.ui.button(label="show party command")
    async def getPCmdButton(self, button: discord.Button, interaction: discord.Interaction):
        p_cmd = self.text
        await interaction.response.send_message(f"このコマンドで一斉に呼ぶことができます。\n```{p_cmd}```", ephemeral=True)


class ReactionNotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.threshold = 1  # n個以上のリアクションがある場合の閾値

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # リアクションが付加されたメッセージを取得
        channel = self.bot.get_channel(payload.channel_id)
        if payload.channel_id == 730835860316225627:
            self.threshold = 4
        elif payload.channel_id == 1040544205933654047:
            self.threshold = 3
        else:
            return

        # 一番下のメッセージを取得
        message = await channel.history(limit=1).flatten()
        if message:
            message = message[0]
        else:
            return

        # リアクションをつけたメンバーの情報を取得
        reactors = []

        for reaction in message.reactions:
            async for user in reaction.users():
                member = message.guild.get_member(user.id)
                if member and not member in reactors:
                    reactors.append(member)
                else:
                    continue

        if len(reactors) == self.threshold:
            # メンションして通知
            mcid_list = []
            uuid_list = await self.bot.db_select("player_data")
            uuid_list = [[str(item[0]), int(item[1])] for item in uuid_list]

            notification = f"{message.author.mention} - リアクションが{self.threshold}個つきました！\nメンバー"
            for reactor in reactors:
                nickname = reactor.nick if reactor.nick else reactor.name
                notification += f"\n{nickname}さん"
                for i, j in uuid_list:
                    if j == reactor.id:
                        mcid_list.append(i[1:])

            clipboard_text = "/p "
            for i in mcid_list:
                clipboard_text += f"{self.bot.uuid_to_mcid(i)} "

            p_cmd_view = PCommandView(clipboard_text[:-1])
            await channel.send(notification, view=p_cmd_view)


def setup(bot):
    bot.add_cog(ReactionNotifyCog(bot))
