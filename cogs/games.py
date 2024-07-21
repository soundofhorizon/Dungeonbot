import asyncio
import random

import discord
from discord.ext import commands

from decimal import Decimal, ROUND_HALF_UP


class Frag_collect:
    # これをONにするとチンチロはピンゾロモードになります。使用厳禁。(Debugのみ可能)
    pinzoro_frag = False
    # ccr用123さんこんにちは(来んな)
    hihumi_frag = False
    # この値がTrueになったとき確定演出が入るかもしれない
    confirm_frag = False
    # チンチロメンテナンス
    ccr_maintenance_frag = False


def is_integer(n):
    try:
        int(n)
        if int(n) <= 0:
            return
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def dm_only():
    def predicate(ctx):
        return isinstance(ctx.channel, discord.DMChannel)

    async def wrapper(ctx):
        if predicate(ctx):
            await ctx.send("ここは…どこ？私は誰？\n(DMでコマンドは実行しないでください。)")
        else:
            await ctx.command(ctx)

    return commands.check(wrapper)


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @dm_only()
    async def toss(self, ctx):
        random_event_frag = random.randint(1, 1000)
        if random_event_frag == 1000:
            await ctx.send(f"<@!{ctx.author.id}> の周りの空気が凪いでいる…")
            await asyncio.sleep(1)
            await ctx.send("ざわ…ざわ…")
            await asyncio.sleep(3)
        result = random.choice(["表", "裏"])
        await ctx.send(result)

    @commands.command()
    async def a_toss(self, ctx):
        result = random.randint(0, 15)
        hp = [-300, -200, -100, 100, 200, 300]
        if result == 0:
            result = f"Your High Class Archfiend Dice rolled a **6**! Nice! Bonus: {hp[5]}:heart:"
        else:
            num = random.randint(0, 4)
            result = f"Your High Class Archfiend Dice rolled a **{num + 1}**! Bonus: {hp[num]}:heart:"
        await ctx.send(result)

    @commands.command()
    async def keiba(self, ctx, msg):
        if is_integer(msg):
            num_horses = int(msg)
            if 20 >= num_horses >= 1:
                uma_emoji = ":racehorse:"
                space = "　"
                space_count = 36
                uma_space = [space_count] * num_horses
                uma_finished = [False] * num_horses
                description = ":checkered_flag:\n"

                for _ in range(num_horses):
                    description += f"{space * space_count}{uma_emoji}\n"

                uma = await ctx.channel.send(description)
                finish_order = []
                while len(finish_order) < num_horses - 1:
                    await asyncio.sleep(0.3)
                    description = ":checkered_flag:\n"

                    for j in range(num_horses):
                        if uma_finished[j]:
                            description += f"{space * uma_space[j]}{uma_emoji}\n"
                            continue

                        random_event = random.randint(1, 100)
                        if random_event <= 20:
                            uma_space[j] = min(space_count, uma_space[j] + random.randint(0, 3))
                        else:
                            uma_space[j] = max(0, uma_space[j] - random.randint(0, 3))

                        if uma_space[j] == 0:
                            uma_finished[j] = True
                            finish_order.append(j + 1)

                        description += f"{space * uma_space[j]}{uma_emoji}\n"

                    await uma.edit(content=description)

                # 最後にゴールする馬の順位を決定
                last_horse = [i + 1 for i, finished in enumerate(uma_finished) if not finished][0]
                finish_order.append(last_horse)

                finish_message = "順位:\n"
                for rank, horse in enumerate(finish_order, 1):
                    finish_message += f"{rank}位: {horse}番目の馬\n"

                await ctx.channel.send(finish_message)
            else:
                await ctx.channel.send("20匹より多い馬を使った競馬は出来ません。")
        else:
            await ctx.channel.send("20以下の正整数で入力してください")

    @commands.command()
    async def bj(self, ctx):
        # cardIndex.txtに書かれたファイル名を読み込んでListへ
        card_data = open(r"cogs/card/cardIndex.txt", "r")
        lines = card_data.readlines()
        card_data.close()
        score = 0
        score_low = 0
        score_high = 0

        # 各自ファイル名に対してスコアを決定
        def score_calc(m):
            if m == "2 (1).png" or m == "2 (2).png" or m == "2 (3).png" or m == "2 (4).png":
                return 2
            elif m == "3 (1).png" or m == "3 (2).png" or m == "3 (3).png" or m == "3 (4).png":
                return 3
            elif m == "4 (1).png" or m == "4 (2).png" or m == "4 (3).png" or m == "4 (4).png":
                return 4
            elif m == "5 (1).png" or m == "5 (2).png" or m == "5 (3).png" or m == "5 (4).png":
                return 5
            elif m == "6 (1).png" or m == "6 (2).png" or m == "6 (3).png" or m == "6 (4).png":
                return 6
            elif m == "7 (1).png" or m == "7 (2).png" or m == "7 (3).png" or m == "7 (4).png":
                return 7
            elif m == "8 (1).png" or m == "8 (2).png" or m == "8 (3).png" or m == "8 (4).png":
                return 8
            elif m == "9 (1).png" or m == "9 (2).png" or m == "9 (3).png" or m == "9 (4).png":
                return 9
            else:
                return 10

        showFileURI1 = lines[random.randint(0, 51)].replace('\n', '')
        if showFileURI1 == "A (1).png" or showFileURI1 == "A (2).png" or showFileURI1 == "A (3).png" or showFileURI1 == "A (4).png":
            score_low += 1
            score_high += 11
        else:
            score_low += score_calc(showFileURI1)
            score_high += score_calc(showFileURI1)

            showFileURI2 = lines[random.randint(0, 51)].replace('\n', '')
            if showFileURI2 == "A (1).png" or showFileURI2 == "A (2).png" or showFileURI2 == "A (3).png" or showFileURI2 == "A (4).png":
                score_low += 1
                # 高いほうのスコアが21を超えるかどうかの判断を行う。Aが2枚あったとき、現時点でlow8.high19だとして、+1は耐える
                if score_high + 11 > 21 and score_high + 1 < 21:
                    score_high += 1
                else:
                    score_high += 11
            else:
                score_low += score_calc(showFileURI2)
                score_high += score_calc(showFileURI2)

            my_files = [
                discord.File(f'cogs/card/{showFileURI1}'),
                discord.File(f'cogs/card/{showFileURI2}'),
            ]
            await ctx.send(files=my_files)

            if score_low == score_high or score_high > 21:
                await ctx.send(f"**{ctx.author.display_name}'s Score is: {score_low}**")
            else:
                if score_high == 21:
                    await ctx.send("_**BlackJack!!**_")
                    return
                await ctx.send(
                    f"**{ctx.author.display_name}'s Score is: low:{score_low}, high:{score_high}**")

            await ctx.send("HIT? or STAND? please write your action -> ['hit', 'stand']")

            # 書いた人がコマンド打った人、また、standかhitを打った人
            def check(m):
                return m.author.id == ctx.author.id and m.content == 'stand' or m.content == 'hit'

            try:
                # ユーザーの返答を待つ
                playerSelect = await self.bot.wait_for('message', check=check, timeout=60.0)

                # standじゃない分、カード引き続けてどうぞ

                while playerSelect != "stand":
                    if playerSelect.content == "hit":
                        addFileURI = lines[random.randint(0, 51)].replace('\n', '')

                        if addFileURI == "A (1).png" or addFileURI == "A (2).png" or addFileURI == "A (3).png" or addFileURI == "A (4).png":
                            score_low += 1
                            # 高いほうのスコアが21を超えるかどうかの判断を行う。Aが2枚あったとき、現時点でlow8.high19だとして、+1は耐える
                            if score_high + 11 > 21 and score_high + 1 < 21:
                                score_high += 1
                            else:
                                score_high += 11
                        else:
                            score_low += score_calc(addFileURI)
                            score_high += score_calc(addFileURI)

                        await ctx.send(file=discord.File(f'cogs/card/{addFileURI}'))

                        # Aの最大値が21超えた時
                        if score_low == score_high or score_high > 21:
                            if score_low == 21:
                                await ctx.send("_**Just 21!**_")
                                return
                            await ctx.send(f"**{ctx.author.display_name}'s Score is: {score_low}**")
                        else:
                            if score_high == 21:
                                await ctx.send("_**Just 21!**_")
                                return
                            await ctx.send(
                                f"**{ctx.author.display_name}'s Score is: low:{score_low}, high:{score_high}**")

                        if score_low > 21:
                            await ctx.send("You are **BURST!!!!!!!!!**")
                            return

                        await ctx.send("HIT? or STAND? please write your action -> ['hit', 'stand']")
                        playerSelect = await self.bot.wait_for('message', check=check, timeout=60.0)

                    elif playerSelect.content == "stand":
                        # Aが出た時、高い点だった場合はこのスコアを採用するだろう。
                        if score_high != 0 and score_high <= 21:
                            score = score_high
                        elif score_low != 0:
                            score = score_low

                        await ctx.send(f"**{ctx.author.display_name}'s Score is: {score}**")
                        return

            except asyncio.TimeoutError:
                await ctx.send("You are Timeout! BURST!")

    @commands.command()
    async def bj_help(self, ctx):
        await ctx.send("自分の得点を**21**に近づけろ…超えるんじゃねえぞ…", file=discord.File(r"cogs/help/explain.png"))

    @commands.command()
    async def ccr(self, ctx):
        saikoro = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
        # サイコロはon_ctx直下にあるサイコロリストを参考にしている。そこから3つ、ランダム選択して新たにリストに突っ込む
        # Config内のFrag操作にて、piczoro_fragをTrueにするとピンゾロしか出ません
        if not Frag_collect.pinzoro_frag:
            result = [saikoro[random.randint(0, 5)], saikoro[random.randint(0, 5)], saikoro[random.randint(0, 5)]]
        else:
            result = [saikoro[random.randint(0, 0)], saikoro[random.randint(0, 0)], saikoro[random.randint(0, 0)]]
        # 最後に結果をまとめて表示するほうが負荷が少ない
        show_result = ""
        # 1%の確率でションベンしようぜ
        shonben_time = random.randint(0, 99)

        # 確定演出の確率を操作しようぜ
        confirm_probability = random.randint(0, 3)  # 1/4
        worst_probability = random.randint(0, 19)  # 1/20
        hazure_pattern = random.randint(0, 2)  # 1-2,3-4,5-6をいい感じに混ぜる

        # リストの中の数字を数え上げ、その結果により分岐していく。このリストには1~6における数字の個数が入っている
        saikoro_count = [result.count(":one:"), result.count(":two:"),
                         result.count(":three:"), result.count(":four:"),
                         result.count(":five:"), result.count(":six:")]

        # ぞろ目について(重複する個数が3つあるとき)
        if 3 in saikoro_count:
            if saikoro_count[0] == 3:
                show_result += "ピンゾロ！五倍付け！"
                Frag_collect.pinzoro_frag = True
            else:
                show_result += "ゾロメ！三倍付け！"
                Frag_collect.confirm_frag = True
        # 普通の目について,2個出てる部分がある場合について、1個しかない部分のindex+1(0からindexは始まるから)が目である。そのindexとsaikoroリストのindexは一致してる
        elif 2 in saikoro_count:
            show_result += f"目は{saikoro[saikoro_count.index(1)]}です！"

        # 123と456について
        else:
            if saikoro_count == [1, 1, 1, 0, 0, 0]:
                show_result += "ヒフミ！倍払い！"
                result = [saikoro[random.randint(0, 0)], saikoro[random.randint(1, 1)],
                          saikoro[random.randint(2, 2)]]
                Frag_collect.hihumi_frag = True
            elif saikoro_count == [0, 0, 0, 1, 1, 1]:
                result = [saikoro[random.randint(3, 3)], saikoro[random.randint(4, 4)],
                          saikoro[random.randint(5, 5)]]
                show_result += "シゴロ！倍付け！"
                Frag_collect.confirm_frag = True
            else:
                show_result += "目無し！"
        # 結果出力
        await ctx.channel.send(f"{ctx.author.display_name}さんがサイコロを降ります。")
        if shonben_time == 0:
            await ctx.channel.send("椀からサイコロが出ちまった…\n**ションベンだ！**")
        else:
            # 確定演出モードになったとき(1/4で外れますelse以降が外れた際の処理)
            if Frag_collect.confirm_frag:
                await ctx.channel.send("**ざわ…ざわ…ざわ…**")
                await asyncio.sleep(2.0)
                if confirm_probability != 0:
                    show_result += "**\n僥倖…！圧倒的感謝…！**"
                else:
                    if worst_probability == 0:
                        await ctx.channel.send(f":one::two::three:")
                        await ctx.channel.send("ヒフミ！倍払い！", file=discord.File("cogs/picture/zetubou.png"))
                        Frag_collect.hihumi_frag = False
                        Frag_collect.confirm_frag = False
                        return
                    else:
                        show_result = "なんだよ…はずれか…"
                        if hazure_pattern == 0:
                            await ctx.channel.send(
                                f"{saikoro[random.randint(0, 1)]}{saikoro[random.randint(2, 3)]}{saikoro[random.randint(4, 5)]}")
                        elif hazure_pattern == 1:
                            await ctx.channel.send(
                                f"{saikoro[random.randint(4, 5)]}{saikoro[random.randint(0, 1)]}{saikoro[random.randint(2, 3)]}")
                        elif hazure_pattern == 2:
                            await ctx.channel.send(
                                f"{saikoro[random.randint(2, 3)]}{saikoro[random.randint(4, 5)]}{saikoro[random.randint(0, 1)]}")
                        await ctx.channel.send(show_result)
                        Frag_collect.hihumi_frag = False
                        Frag_collect.confirm_frag = False
                        return
            await ctx.channel.send(f"{result[0]}{result[1]}{result[2]}")
            if Frag_collect.hihumi_frag:
                await ctx.channel.send(show_result, file=discord.File("cogs/picture/zetubou.png"))
            elif Frag_collect.pinzoro_frag:
                await ctx.channel.send(show_result, file=discord.File("cogs/picture/gyoukou.jpg"))
            else:
                await ctx.channel.send(show_result)
        Frag_collect.pinzoro_frag = False
        Frag_collect.hihumi_frag = False
        Frag_collect.confirm_frag = False

    @commands.command()
    async def ccr_help(self, ctx):
        await ctx.send(
            "ヘルプを表示します\n"
            "https://ja.wikipedia.org/wiki/チンチロリン\n"
            "https://gyazo.com/4141792166fe610e79beff1a6c03613f\n"
            "1%の確率でションベンします。その場合は1倍払いです"
        )

    @commands.command()
    async def oe(self, ctx, msg):
        try:
            saikoro = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
            player = []
            betprice = []
            playerchoice = []
            join_member_count = int(msg)
            oya_id = ctx.author.id

            def check1(m):
                if m.author.bot:
                    return
                else:
                    return m.channel == ctx.channel and m.content == "半" or m.content == "丁"

            def check2(m):
                if m.author.bot:
                    return
                else:
                    return m.channel == ctx.channel and is_integer(unformat_BMK(m.content))

            def check3(m):
                if m.author.bot:
                    return
                else:
                    return m.channel == ctx.channel

            def check4(m):
                if m.author.bot:
                    return
                elif m.author.id == oya_id:
                    return m.channel == ctx.channel and m.content == "dice"

            def format_BMK(m) -> str:
                if m >= 1000000000:
                    m = f"{Decimal(str(float(m / 1000000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}B"
                elif m >= 1000000:
                    m = f"{Decimal(str(float(m / 1000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}M"
                elif m >= 1000:
                    m = f"{Decimal(str(float(m / 1000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}K"
                return m

            def unformat_BMK(value_str):
                multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}

                value_str = value_str.strip().lower()
                last_char = value_str[-1]

                if last_char.isdigit():
                    return int(value_str)

                if last_char in multipliers:
                    multiplier = multipliers[last_char]
                    num = Decimal(value_str[:-1])
                    return int(num * multiplier)

            await ctx.channel.send(
                f"{join_member_count}人で丁半を始めます。よろしいですか? よければ``yes``,違っていれば``no``と親が書いてください")
            response = await self.bot.wait_for("message", check=check3)
            if response.content == "YES" or response.content == "yes" or response.content == "いぇｓ":
                await ctx.channel.send(
                    f"{ctx.author.display_name}が親だ！\n参加者は掛け金額を書いてください。")
                for i in range(join_member_count):
                    joinbet = await self.bot.wait_for('message', check=check2)
                    player.append(joinbet.author.display_name)
                    betprice.append(unformat_BMK(joinbet.content))
                    await ctx.channel.send(
                        f"{joinbet.author.display_name}の参加をbet額: {joinbet.content}で受け付けました")

                await ctx.channel.send(file=discord.File("cogs/picture/in.png"))
                await ctx.channel.send("さあ張った張った！")

                for i in range(join_member_count):
                    await ctx.channel.send(f"Player: {player[i]}さん、半か丁を書いてください")
                    choice = await self.bot.wait_for('message', check=check1)
                    playerchoice.append(choice.content)

                await ctx.channel.send("丁半揃いました!")
                await ctx.channel.send("親は``dice``と書き、サイコロを振ってください。``※30秒以内で振らないと親の負けになります``")

                try:
                    response2 = await self.bot.wait_for("message", check=check4, timeout=30.0)
                    if response2.content == "dice":
                        deme1 = random.randint(0, 5)
                        deme2 = random.randint(0, 5)
                        result = "丁" if (deme1 + deme2) % 2 == 0 else "半"
                        await ctx.channel.send(f"{saikoro[deme1]}{saikoro[deme2]}")
                        await ctx.channel.send(f"**{result}!!**")

                        seisan = ""
                        for i in range(join_member_count):
                            if playerchoice[i] == result:
                                print(betprice[i] * 2)
                                seisan += f"{player[i]}　取り分: sb coins {format_BMK(int(betprice[i]) * 2)}\n"
                        if seisan == "":
                            await ctx.channel.send(f"**------清算------**\n勝ち人数0！")
                        else:
                            await ctx.channel.send(f"**------清算------**\n{seisan}")
                    else:  # This code can`t reach default...
                        await ctx.channel.send("(Error)サイコロが振られませんでした")
                except asyncio.TimeoutError:
                    await ctx.channel.send("親がサイコロを振らなかったので子の勝ちです！")
            else:
                await ctx.channel.send("最初からやり直してください")
        except ValueError:
            await ctx.channel.send("引数に参加人数が必要です！ Command usage:``!oe 参加人数　ex:!oe 4``")


def setup(bot):
    bot.add_cog(Games(bot))
