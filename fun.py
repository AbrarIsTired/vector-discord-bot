# fun.py
import discord
from discord.ext import commands
import random
import socket

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0

    # Simple Ping Command
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title ="🏓 Ping!",
            description=f"Pong! Latency is {round(self.bot.latency*1000)}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        #await ctx.send(f"Current Latency: {round(self.bot.latency*1000)}ms")

    # Rock Paper Scissors Command
    @commands.command()
    async def rps(self, ctx, user_choice: str = None):
        embed = discord.Embed(
            title ="Rock, Paper, Scissors!",
            color=discord.Color.green()
        )

        if user_choice is None: # Check for no input
            embed.add_field(name="How To Play", value="Commander, you need to type out v!rps with your choice! i.e v!rps rock", inline=False)
            await ctx.send(embed=embed)
            return None

        choices = ["rock", "paper", "scissors"] # Available choices for Bot and User
        user_choice = user_choice.lower()

        if user_choice not in choices: # Check for invalid value
            embed.add_field(name="Invalid Choice", value="You can only use rock, paper or scissors Commander", inline=False)
            await ctx.send(embed=embed)
            return None

        # Bot Choice
        bot_choice = random.choice(choices)
        result = ""

        # Winner Logic
        if user_choice == bot_choice:
            result = "It's a tie Commander!"
        if(user_choice == "rock" and bot_choice == "scissors") or (user_choice == "paper" and bot_choice == "rock") or (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win Commander!"
        elif user_choice != bot_choice:
            result = "I win. Better luck next time!"
        
        # Result Output
        embed.add_field(name="Outcome", value=f"You chose {user_choice}, I chose {bot_choice}. {result}", inline=False)
        await ctx.send(embed=embed)

        

    # Dice Roll Command
    @commands.command()
    async def dice(self, ctx, sides: int = 6):
        embed = discord.Embed(
            title ="Dice Roll",
            color=discord.Color.green()
        )
        # Guard for anything less than 2 sides
        if(sides <= 1):
            embed.add_field(name="Invalid Amount", value="Commander, you can only roll a dice 2 or higher", inline=False)
            await ctx.send(embed=embed)
            return None
        
        # Dice Roll Logic
        result = random.randint(1, sides)
        
        # For Nat-Values
        if(result == sides):
            embed.add_field(name="Outcome", value=f"🎲 Nat-{sides}! You rolled a {result}!", inline=False)
            await ctx.send(embed=embed)
        # Roll Result    
        embed.add_field(name="Outcome", value=f"🎲 You rolled a {result} on a {sides}-sided dice!", inline=False)
        await ctx.send(embed=embed)
        # await ctx.send(f"🎲 You rolled a {result} on a {sides}-sided dice!")


    # Event Listener for messages containing specific words
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "vector" in message.content.lower():
            await message.channel.send(f"Yo Commander, what's up?")

    # Status Command to check server status of active game servers
    @commands.command()
    async def status(self,ctx):
        def check_server(host, port):
            try:
                with socket.create_connection((host, port), timeout=2):
                    return True
            except:
                return False
        # Dictionary storing server names and their corresponding IP + port
        services = {
            "CasaOS Home (Port 80)": ("10.0.0.26", 80),
            "SSH Home (Port 22)": ("10.0.0.26", 22),
            "CasaOS Game Server (Port 80)": ("10.0.0.202", 80),
            "SSH Game Server (Port 22)": ("10.0.0.202", 22),
            "Terraria (Port 7777)": ("10.0.0.202", 7777),
            "Minecraft Aether II (Port 25565)": ("10.0.0.202", 25565)
        }

        # Creates a Discord embed 
        embed = discord.Embed(
            title="🖥️ Server Status",                     
            description="Abrar's Game Server Status:",    
            color=discord.Color.green()                   
        )

        # Loop through each server in the dictionary
        for name, (host, port) in services.items():
            online = check_server(host, port)

            # Convert output from check_server (Boolean) into a readable message
            status = "✅ Online" if online else "❌ Offline"

            embed.add_field(
                name=name,
                value=status,
                inline=True
            )

        await ctx.send(embed=embed)

    


# Cog seutp
async def setup(bot):
    await bot.add_cog(Fun(bot))