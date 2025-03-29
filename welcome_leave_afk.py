import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not set.")

# Set up bot intents and instance
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="^", intents=intents)

# Global variables for AFK and channel toggles
afk_users = set()           # Stores user IDs marked as AFK
welcome_enabled = False     # Toggle for welcome messages
welcome_channel_id = None   # Channel ID for welcome messages
log_channel_id = None       # Channel ID for logging data

# Replace with your admin user ID
ADMIN_USER_ID = 123456789012345678

# --------------------------
# AFK Command: ^afk on/off
# --------------------------
@bot.command()
async def afk(ctx, toggle: str = None):
    """
    Toggle AFK status on or off.
    
    Usage:
      ^afk on  -> Mark yourself as AFK.
      ^afk off -> Remove your AFK status.
    """
    toggle = (toggle or "").lower()
    if toggle == "on":
        if ctx.author.id in afk_users:
            await ctx.send(f"{ctx.author.mention}, you are already AFK.")
        else:
            afk_users.add(ctx.author.id)
            await ctx.send(f"{ctx.author.mention} is now AFK.")
    elif toggle == "off":
        if ctx.author.id in afk_users:
            afk_users.remove(ctx.author.id)
            await ctx.send(f"{ctx.author.mention}, you are no longer AFK.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not AFK.")
    else:
        await ctx.send("Invalid usage. Use '^afk on' or '^afk off'.")

# --------------------------
# on_message Event for AFK Response
# --------------------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # If an AFK user sends a message, remove them from the AFK set
    if message.author.id in afk_users:
        afk_users.remove(message.author.id)

    # For each mentioned user, if they're AFK, notify the channel once
    responded = set()
    for user in message.mentions:
        if user.id in afk_users and user.id not in responded:
            responded.add(user.id)
            await message.channel.send(f"{user.display_name} is AFK")
    
    await bot.process_commands(message)

# --------------------------
# Welcome Command: ^welcome on/off
# --------------------------
@bot.command()
async def welcome(ctx, toggle: str):
    """
    Toggle welcome messages on or off.
    
    Usage:
      ^welcome on   -> Enable welcome messages in the current channel.
      ^welcome off  -> Disable welcome messages.
    (Admin-only: Only the admin user can use this command.)
    """
    global welcome_enabled, welcome_channel_id
    if ctx.author.id != ADMIN_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return

    toggle = toggle.lower()
    if toggle == "on":
        welcome_enabled = True
        welcome_channel_id = ctx.channel.id
        await ctx.send(f"Welcome messages enabled in {ctx.channel.mention}.")
    elif toggle == "off":
        welcome_enabled = False
        welcome_channel_id = None
        await ctx.send("Welcome messages disabled.")
    else:
        await ctx.send("Invalid option. Use '^welcome on' or '^welcome off'.")

# --------------------------
# Data Logging Command: ^datato on/off
# --------------------------
@bot.command()
async def datato(ctx, toggle: str):
    """
    Toggle data logging on or off.
    
    Usage:
      ^datato on   -> Set the current channel as the log channel for member data.
      ^datato off  -> Disable data logging.
    (Admin-only: Only the admin user can use this command.)
    """
    global log_channel_id
    if ctx.author.id != ADMIN_USER_ID:
        await ctx.send("You are not authorized to use this command.")
        return

    toggle = toggle.lower()
    if toggle == "on":
        log_channel_id = ctx.channel.id
        await ctx.send(f"Data logging enabled in {ctx.channel.mention}.")
    elif toggle == "off":
        log_channel_id = None
        await ctx.send("Data logging disabled.")
    else:
        await ctx.send("Invalid option. Use '^datato on' or '^datato off'.")

# --------------------------
# on_ready Event
# --------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    bot.run(TOKEN)
