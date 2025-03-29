import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime

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

# Global variables
afk_users = set()           # Global AFK set
welcome_enabled = False     # Toggle for welcome messages
welcome_channel_id = None   # Channel ID for welcome messages
log_channel_id = None       # Channel ID for logging member events

# Placeholder channel IDs for the welcome embed (replace with actual IDs)
ROLE_CHANNEL_ID = 123456789012345678   # Replace with your role channel ID
INTRO_CHANNEL_ID = 123456789012345679   # Replace with your introductions channel ID
INFO_CHANNEL_ID = 123456789012345680    # Replace with your info channel ID
LOUNGE_CHANNEL_ID = 123456789012345681  # Replace with your lounge channel ID

# Replace with your admin user ID
ADMIN_USER_ID = 123456789012345682

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
            await ctx.send(f"{ctx.author.mention} is AFK")
    elif toggle == "off":
        if ctx.author.id in afk_users:
            afk_users.remove(ctx.author.id)
            await ctx.send(f"{ctx.author.mention}, you are no longer AFK.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not AFK.")
    else:
        await ctx.send("Invalid usage. Use '^afk on' or '^afk off'.")

# --------------------------
# Welcome Messages Command: ^welcome on/off
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
        await ctx.send(f"Welcome messages have been enabled in {ctx.channel.mention}.")
    elif toggle == "off":
        welcome_enabled = False
        welcome_channel_id = None
        await ctx.send("Welcome messages have been disabled.")
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
        await ctx.send(f"Data logging has been enabled in {ctx.channel.mention}.")
    elif toggle == "off":
        log_channel_id = None
        await ctx.send("Data logging has been disabled.")
    else:
        await ctx.send("Invalid option. Use '^datato on' or '^datato off'.")

# --------------------------
# Global on_message Event for AFK Responses
# --------------------------
@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # If an AFK user sends a message, remove them from AFK (optionally notify)
    if message.author.id in afk_users:
        afk_users.remove(message.author.id)
        # Optionally: notify them that they're no longer AFK

    # For each mentioned user, if they're AFK, send one reply using their display name
    responded = set()
    for user in message.mentions:
        if user.id in afk_users and user.id not in responded:
            responded.add(user.id)
            await message.channel.send(f"{user.display_name} is AFK")

    # Process commands after handling AFK logic
    await bot.process_commands(message)

# --------------------------
# Helper: Build Welcome Embed
# --------------------------
def build_welcome_embed(member: discord.Member) -> discord.Embed:
    role_channel = bot.get_channel(ROLE_CHANNEL_ID)
    intro_channel = bot.get_channel(INTRO_CHANNEL_ID)
    info_channel = bot.get_channel(INFO_CHANNEL_ID)
    lounge_channel = bot.get_channel(LOUNGE_CHANNEL_ID)
    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}!",
        description=(f"We hope you will have a great time here, {member.mention}!\n\n"
                     "Here are some channels to get you started:"),
        color=discord.Color.green()
    )
    embed.add_field(name="Info", value=info_channel.mention if info_channel else "#info", inline=True)
    embed.add_field(name="Introductions", value=intro_channel.mention if intro_channel else "#introductions", inline=True)
    embed.add_field(name="Roles", value=role_channel.mention if role_channel else "#roles", inline=True)
    embed.add_field(name="Lounge", value=lounge_channel.mention if lounge_channel else "#lounge", inline=True)
    embed.set_image(url="https://i.imgur.com/wJJnMSI.png")
    return embed

# --------------------------
# Helper: Build Log Embed
# --------------------------
def build_log_embed(member: discord.Member, action: str) -> discord.Embed:
    joined_at_str = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "N/A"
    created_at_str = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_time_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if action == "joined":
        title = "New Member Joined"
        color = discord.Color.blue()
        description = f"{member.mention} joined the server."
    else:
        title = "Member Left"
        color = discord.Color.orange()
        description = f"{member.mention} left or was kicked from the server."
    embed = discord.Embed(title=title, description=description, color=color, timestamp=datetime.datetime.utcnow())
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="User", value=f"{member} (ID: {member.id})", inline=False)
    embed.add_field(name="Joined Discord", value=created_at_str, inline=True)
    embed.add_field(name="Joined Server", value=joined_at_str, inline=True)
    if action == "left":
        embed.add_field(name="Left Server", value=current_time_str, inline=True)
    embed.set_footer(text="Member Log")
    return embed

# --------------------------
# Event: on_member_join
# --------------------------
@bot.event
async def on_member_join(member: discord.Member):
    if welcome_enabled and welcome_channel_id is not None:
        channel = bot.get_channel(welcome_channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            embed = build_welcome_embed(member)
            await channel.send(embed=embed)
    if log_channel_id is not None:
        channel = bot.get_channel(log_channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            embed = build_log_embed(member, action="joined")
            await channel.send(embed=embed)

# --------------------------
# Event: on_member_remove
# --------------------------
@bot.event
async def on_member_remove(member: discord.Member):
    if log_channel_id is not None:
        channel = bot.get_channel(log_channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            embed = build_log_embed(member, action="left")
            await channel.send(embed=embed)

# --------------------------
# Event: on_member_ban
# --------------------------
@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    if log_channel_id is not None:
        channel = bot.get_channel(log_channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            try:
                ban_entry = await guild.fetch_ban(user)
                reason = ban_entry.reason if ban_entry else None
            except discord.NotFound:
                reason = None
            embed = discord.Embed(title="Member Banned", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="User", value=f"{user} (ID: {user.id})", inline=False)
            embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
            embed.set_footer(text="Ban Log")
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)
            await channel.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
