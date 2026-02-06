#Hier importeren we de benodigde libraries voor de Discord Bot integration.
import discord


#Alvast de discord token hier gezet, want die gaan we nodig hebben.    
DISCORD_TOKEN="TOKEN MOET HIER. HAAL DEZE ALTIJD WEG VOORDAT JE DE CODE GAAT COMITTEN, SLA ERGENS ANDERS VEILIG OP"

#startup banner en welkom message.(alleen cosmetisch nu, maar later correct implementeren met de bot.)
print(""" 
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

""")
print()
print("Buddybot is wakker geworden, wat wil je doen?","\n \n","gebruik /help voor de commandolijst.")   

#Bij een correcte integration kan hier d.m.v if functie, commando's(userinput vanuit de discord bot) worden gebruikt om snippets te invoken. en de output terug te sturen naar de discord chat.