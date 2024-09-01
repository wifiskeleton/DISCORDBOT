import discord
from discord.ext import commands
import asyncio, random
import requests

class Blacktea(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.players = {}  # player_id: {'lives': int}
        self.game_channel = None
        self.game_message = None
        self.game_active = False
        self.fmsgwait = 1.35
        self.max_lives = 2
        self.join_time = 30  # seconds to join the game
        self.turn_time = 15  # seconds to guess a word
        self.letter_combinations = [
            'ABM', 'AGP', 'ANT', 'APT', 'ART', 'ASL', 'BUN', 'CAB', 'CAY', 'CIN', 
            'COB', 'CON', 'CRU', 'DAW', 'DIA', 'DUN', 'DUP', 'EEL', 'FAN', 'FAR', 
            'FAT', 'FIT', 'GAM', 'GEN', 'GIT', 'GOA', 'HIT', 'HOG', 'HOP', 'ILE', 
            'IND', 'INT', 'IRE', 'JAM', 'JAP', 'JOW', 'LIT', 'MAC', 'MAR', 'MAY', 
            'MEN', 'MET', 'MOR', 'MOT', 'NAM', 'NEP', 'NIT', 'NOM', 'NOT', 'NUN', 
            'OIL', 'OPT', 'ORB', 'PAR', 'PAT', 'PIT', 'PLU', 'POL', 'PUN', 'PUT', 
            'RAG', 'RAW', 'REC', 'RED', 'RET', 'ROW', 'RUG', 'RUM', 'SAD', 'SAG', 
            'SAT', 'SEG', 'SIR', 'SIT', 'SOP', 'SOW', 'SPR', 'SUN', 'SUP', 'TAG', 
            'TEA', 'TIL', 'TIN', 'TOP', 'TUB', 'TUN', 'VAN', 'VET', 'WAX', 'WEB', 
            'WIT', 'YET', 'YON', 'ZIP', 'ZOO', 'BAN', 'BAY', 'BEG', 'BIG', 'BLU', 
            'BUR', 'CAN', 'CAR', 'CAT', 'CHE', 'CHU', 'CLI', 'COR', 'CUP', 'DEW', 
            'ELF', 'GAP', 'GEM', 'GUN', 'HOB', 'JET', 'JIN', 'JOT', 'JUN', 'JUR', 
            'KID', 'LAB', 'LEF', 'LOP', 'MAG', 'MAY', 'MOT', 'MUG', 'NOR', 'PEN', 
            'PER', 'PEG', 'PEP', 'POL', 'POW', 'PRO', 'RAY', 'REC', 'RIT', 'ROD', 
            'SPY', 'TED', 'TOM', 'TOW', 'WIN'
        ]

    def generate_random_letters(self):
        return random.choice(self.letter_combinations)

    def is_valid_word(self, word):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}")
        return response.status_code == 200

    @commands.command(aliases=['bt'])
    async def startblacktea(self, ctx: commands.Context):
        if self.game_active:
            await ctx.send("A game is already in progress.")
            return

        self.game_active = True
        self.players = {}
        self.game_channel = ctx.channel

        embed = discord.Embed(
            title="Blacktea Game Started",
            description="React with ✅ to join the game. You have 30 seconds to join.",
            color=discord.Color.blue()
        )
        self.game_message = await ctx.send(embed=embed)
        await self.game_message.add_reaction("✅")

        def check(reaction, user):
            return reaction.message.id == self.game_message.id and str(reaction.emoji) == "✅" and user != self.client.user

        try:
            while True:
                reaction = await self.client.wait_for('reaction_add', timeout=self.join_time, check=check)
                user = reaction[1]
                self.players[user.id] = {'lives': self.max_lives}
                if len(self.players) > 0:
                    break
            await self.game_message.delete()

            if len(self.players) == 0:
                await ctx.send("No players joined. Game cancelled.")
                self.game_active = False
                return

            if len(self.players) == 1:
                await ctx.send(f"Only one player joined. The game will continue until this player loses all lives.")
                await self.play_game(ctx, single_player_mode=True)
            else:
                await ctx.send(f"Game starting with {len(self.players)} players!")
                await self.play_game(ctx, single_player_mode=False)
        except asyncio.TimeoutError:
            await ctx.send("Joining time is over. Starting the game now...")
            await self.game_message.delete()
            await self.play_game(ctx, single_player_mode=False)

    async def play_game(self, ctx, single_player_mode=False):
        while len(self.players) > 1 or (single_player_mode and len(self.players) == 1):
            letters = self.generate_random_letters()
            embed = discord.Embed(
                title="New Round!",
                description=f"Use these letters to form a valid word: **{letters}**\nYou have {self.turn_time} seconds to respond.",
                color=discord.Color.green()
            )
            game_message = await ctx.send(embed=embed)

            def check(msg):
                return msg.author.id in self.players and msg.channel == ctx.channel

            try:
                msg = await self.client.wait_for('message', timeout=self.turn_time, check=check)
                word = msg.content.strip()
                if self.is_valid_word(word):
                    await msg.add_reaction("✅")
                    await ctx.send(f"{msg.author.mention} used the word '{word}' correctly!")
                    await asyncio.sleep(0.5)
                else:
                    await ctx.send(f"{msg.author.mention} has lost a life for the invalid word!")
                    self.players[msg.author.id]['lives'] -= 1
                    if self.players[msg.author.id]['lives'] <= 0:
                        await ctx.send(f"{msg.author.mention} has been eliminated!")
                        del self.players[msg.author.id]
                        if len(self.players) == 1 and single_player_mode:
                            break
            except asyncio.TimeoutError:
                await ctx.send("Time is up! Moving to the next round.")

            await game_message.delete()

        if len(self.players) == 1:
            winner_id = next(iter(self.players))
            winner = ctx.guild.get_member(winner_id)
            await ctx.send(f"Congratulations {winner.mention}, you won the Blacktea game!")
        else:
            await ctx.send("The game ended with no winners.")

        self.game_active = False

async def setup(bot: commands.Bot):
    try:
        await bot.add_cog(Blacktea(bot))
        print("Blacktea cog loaded successfully.")
    except Exception as e:
        print(f"Failed to load Blacktea cog. Error: {e}")
        raise e
