# main.py
# Abrar's Discord Bot: Vector

# Bot character based on the game series, Girl's Frontline. This character in said game is based on the 45ACP Variant of the Kriss Vector

# Imports
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
import random

# Loading Token from environment file (.env)
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# Intents + Perms
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Discord Status Options
status = ["Playing with LEGOs", "Playing in the armory", "Playing with IEDs", "Playing with .45","Playing with 9mm", "Playing with .22LR", "Playing with Fire"]

# Declaring Prefix as m! and setting Playing Status 
bot = commands.Bot(command_prefix="v!", help_command=None, activity=discord.Game(random.choice(status)), intents=intents)

# Async function to load cogs
async def load_cogs():
    cog_extensions = ["fun", "admin"] # Cog/File List
    for extension in cog_extensions:
        await bot.load_extension(extension)
        print(f"Loaded {extension}")

#Status Changer Task/Function - changes status every 30 minutes
@tasks.loop(minutes=30) 
async def change_status():
    new_status = random.choice(status)
    await bot.change_presence(activity=discord.Game(new_status))
    print(f"Status changed to: {new_status}")  # Status changes in console

# Launch Status in the Terminal
@bot.event
async def on_ready():
    print(f"Long time no see, Commander… Neural module nominal, all limbs accounted for, I’m not scraps yet… I’m glad to see you again, Commander, you’re like the sun after a storm.")
    if not change_status.is_running():
        change_status.start()
        print("Status changer started")



# Help Command. Overrides default help command. Learning Embeds
@bot.command()
async def help(ctx):
    # Create the Embed Title
    embed = discord.Embed(
        title="🤖 Vector Bot Commands (v!)",
        description="Long time no see, Commander. Here's a list of my current protocols.",
        color=discord.Color.blue() 
    )

    # General/Fun Commands Field
    fun_commands = (
        "`v!help` | Display this help message.\n"
        "`v!ping` | Check the bot's latency.\n"
        "`v!dice [sides]` | Roll a dice (default 6 sides).\n"
        "`v!rps [rock/paper/scissors]` | Play Rock-Paper-Scissors.\n"
        "`v!status` | Check the status of Abrar's current game servers"
    )
    embed.add_field(name="🛠️ General/Fun Commands", value=fun_commands, inline=False)

    # Admin Commands Field
    admin_commands = (
        "`v!shutdown` | Safely shut down the bot.\n"
        "`v!clear [amount]` | Clear messages (2-100)."
    )
    embed.add_field(name="⚙️ Admin Commands (Owner Only)", value=admin_commands, inline=False)
    
    # Special Features Field
    embed.add_field(
        name="⭐ Special Feature", 
        value="I'll respond if you mention my name, **Vector**, in a message!", 
        inline=False
    )

    await ctx.send(embed=embed)

# Main async function to run the bot
async def main():
    await load_cogs()
    await bot.start(discord_token)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())