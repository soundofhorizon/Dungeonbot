import discord
from discord.ext import commands
import numpy as np

class OthelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Othello()
        self.command_user = None
        self.current_game_message = None

    @commands.command()
    async def othello(self, ctx):
        self.game.reset()
        self.command_user = ctx.author
        await self.start_game(ctx)

    async def start_game(self, ctx):
        board_str = self.game.get_board_str_with_moves()
        embed = discord.Embed(title="Othello", description=board_str, color=0x00ff00)
        self.current_game_message = await ctx.send(embed=embed)
        if self.game.current_player == 1:
            await ctx.send("あなたの番です。1〜9の数字を入力してください。")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author != self.command_user:
            return
        if not message.content.isdigit() or int(message.content) not in range(1, 10):
            if message.content == "!othello":
                pass
            else:
                await message.channel.send("無効な入力です。1〜9の数字を入力してください。")
                return

        move_index = int(message.content) - 1
        valid_moves = sorted(self.game.get_valid_moves(self.game.current_player), key=lambda x: x[0] * 8 + x[1])
        if move_index < len(valid_moves):
            row, col = valid_moves[move_index]
            if self.game.is_valid_move(row, col, self.game.current_player):
                self.game.make_move(row, col, self.game.current_player)
                async for msg in message.channel.history(limit=10):
                    if msg.id != self.current_game_message.id:
                        await msg.delete()
                    else:
                        break
                await self.update_board()
                if self.game.current_player == -1:
                    await self.bot_move(message.channel)
        else:
            await message.channel.send("無効な手です。別の手を入力してください。")

    async def update_board(self):
        board_str = self.game.get_board_str_with_moves()
        embed = discord.Embed(title="Othello", description=board_str, color=0x00ff00)
        await self.current_game_message.edit(embed=embed)
        if self.game.current_player == 1:
            if not self.game.get_valid_moves(self.game.current_player):
                self.game.current_player = -self.game.current_player
                await self.update_board()
            else:
                await self.current_game_message.channel.send("あなたの番です。1〜9の数字を入力してください。")
        elif not self.game.get_valid_moves(self.game.current_player):
            await self.check_winner(self.current_game_message.channel)

    async def bot_move(self, channel):
        valid_moves = self.game.get_valid_moves(self.game.current_player)
        if valid_moves:
            row, col = valid_moves[0]  # 簡単なボットのロジック
            self.game.make_move(row, col, self.game.current_player)
            await self.update_board()
        elif not self.game.get_valid_moves(self.game.current_player):
            await self.check_winner(channel)

    async def check_winner(self, channel):
        black_count = np.sum(self.game.board == 1)
        white_count = np.sum(self.game.board == -1)
        if black_count > white_count:
            winner = "黒（🔴）の勝ちです！"
        elif white_count > black_count:
            winner = "白（⚪）の勝ちです！"
        else:
            winner = "引き分けです！"
        await channel.send(winner)
        self.game.reset()

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3], self.board[4, 4] = 1, 1
        self.board[3, 4], self.board[4, 3] = -1, -1
        self.current_player = 1

    def reset(self):
        self.__init__()

    def is_valid_move(self, row, col, player):
        if self.board[row, col] != 0:
            return False
        opponent = -player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                while 0 <= r < 8 and 0 <= c < 8:
                    r += dr
                    c += dc
                    if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == player:
                        return True
                    if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == 0:
                        break
        return False

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False
        self.board[row, col] = player
        opponent = -player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        to_flip = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            cells_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == opponent:
                cells_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r, c] == player:
                to_flip.extend(cells_to_flip)
        for r, c in to_flip:
            self.board[r, c] = player
        self.current_player = -player
        return True

    def get_board_str(self):
        board_str = ""
        for row in self.board:
            for cell in row:
                if cell == 1:
                    board_str += "🔴"
                elif cell == -1:
                    board_str += "⚪"
                else:
                    board_str += "➖"
            board_str += "\n"
        return board_str

    def get_board_str_with_moves(self):
        number_emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        valid_moves = self.get_valid_moves(self.current_player)
        sorted_moves = sorted(valid_moves, key=lambda x: x[0] * 8 + x[1])
        board_str = ""
        move_map = {move: number_emojis[i] for i, move in enumerate(sorted_moves)}
        for row in range(8):
            for col in range(8):
                if self.board[row, col] == 1:
                    board_str += "🔴"
                elif self.board[row, col] == -1:
                    board_str += "⚪"
                elif (row, col) in move_map:
                    board_str += move_map[(row, col)]
                else:
                    board_str += "➖"
            board_str += "\n"
        return board_str

def setup(bot):
    bot.add_cog(OthelloCog(bot))