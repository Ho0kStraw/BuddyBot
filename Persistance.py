# Deze imports komen bovenaan de code.
import winreg
import os
import sys


# -----------------------------
# Persistance. Commando: /persist. 
# -----------------------------

#Enable eenmalig de persistence van de bot. De bot zal automatisch opstarten bij het opstarten van Windows.

#Hier komt nog een een Bot API Command function.

#def set_persistence():
#    # Pad naar dit script/exe en de naam in het register
#    path = os.path.realpath(sys.argv[0])
#    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
#    
#   try:
#        # Open de 'Run' sleutel en voeg de waarde toe
#        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
#        winreg.SetValueEx(key, "MyBotService", 0, winreg.REG_SZ, path)
#        winreg.CloseKey(key)
#        print("Persistence succesvol ingesteld.")
#    except Exception as e:
#        print(f"Fout: {e}")
#
#set_persistence()