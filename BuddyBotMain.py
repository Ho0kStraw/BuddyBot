import discord
from discord.ext import commands
from discord import app_commands

# Zet hier je nieuwe, geldige bot token (NOOIT openbaar delen!)
DISCORD_TOKEN = "Hier moet de token"

# Jouw server (guild) ID
GUILD_ID = (serverID)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Buddybot is wakker geworden!")

    # Slash commands alleen zichtbaar in jouw server (direct zichtbaar)
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print("Slash commands zijn herkend door Discord (guild sync actief)")

# -----------------------------
# /help command
# -----------------------------
@bot.tree.command(name="help", description="Toon de commandolijst")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🤖 **Buddybot commands**\n"
        "/help – laat dit bericht zien\n"
        "/ping – check of de bot online is\n"
        "/shutdown – sluit de bot af (admin only)"
    )

# -----------------------------
# /ping command
# -----------------------------
@bot.tree.command(name="ping", description="Check of de bot online is")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Buddybot leeft.")

# -----------------------------
# /shutdown command
# -----------------------------
@bot.tree.command(name="shutdown", description="Sluit de bot af (alleen admin)")
async def shutdown(interaction: discord.Interaction):
    # Alleen server admins mogen de bot afsluiten
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Bot wordt afgesloten... 👋")
        await bot.close()  # Sluit de bot veilig af
    else:
        await interaction.response.send_message(
            "Je hebt geen permissie om dit te doen!", ephemeral=True
        )

# Start de bot
bot.run(DISCORD_TOKEN)

