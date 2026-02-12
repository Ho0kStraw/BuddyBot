import discord
from discord.ext import commands
from discord import app_commands
import cv2
import os
import asyncio

DISCORD_TOKEN = "Hier moet je token"
GUILD_ID = 1468980945033105450

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Ingelogd als {bot.user}")

# -----------------------------
# /webcam command
# -----------------------------
@bot.tree.command(name="webcam", description="Maak één webcamfoto (demo)")
async def webcam(interaction: discord.Interaction):
    await interaction.response.defer()

    def capture_image():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False

        success, frame = cap.read()
        if success:
            cv2.imwrite("webcam.png", frame)

        cap.release()
        return success

    loop = asyncio.get_running_loop()
    success = await loop.run_in_executor(None, capture_image)

    if not success:
        await interaction.followup.send("❌ Webcam kon niet worden gebruikt.")
        return

    with open("webcam.png", "rb") as f:
        await interaction.followup.send(file=discord.File(f))

    os.remove("webcam.png")

bot.run(DISCORD_TOKEN)
