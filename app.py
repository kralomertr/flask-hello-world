import discord
import os
from flask import Flask
from threading import Thread

# Botun 7/24 açık kalması için küçük bir web sunucusu
app = Flask('')
@app.route('/')
def home(): return "Bot Aktif!"

def run(): app.run(host='0.0.0.0', port=8080)

# Gerçek Discord Bot Kısmı
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} Olarak Giriş Yapıldı!')

# Botu Başlat
t = Thread(target=run)
t.start()
client.run(os.getenv('DISCORD_TOKEN'))
