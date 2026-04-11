import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from flask import Flask
from threading import Thread

# --- Flask Sunucusu (Render'ı uyanık tutmak için) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif!"

def run():
    # Render portu otomatik atar, 8080 varsayılandır
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot Kodun ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Ban vb. yetkiler için gerekli
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Komutlar senkronize edildi!")

bot = MyBot()

@bot.tree.command(name="spam", description="Tek mesajın içinde 100 kez deneme yazar")
async def spam(interaction: discord.Interaction):
    uzun_mesaj = " ".join([f"deneme {i+1}" for i in range(100)])
    try:
        await interaction.response.send_message(uzun_mesaj)
    except Exception as e:
        print(f"Hata: {e}")

@bot.tree.command(name="ban", description="Belirlediğiniz üyeyi sunucudan yasaklar.")
@app_commands.describe(kim="Yasaklanacak üyeyi seçin", sebep="Yasaklanma sebebi")
@app_commands.checks.has_permissions(ban_members=True) # Burası True olmalı!
async def ban(interaction: discord.Interaction, kim: discord.Member, sebep: str = "Belirtilmedi"):
    try:
        await kim.ban(reason=sebep)
        await interaction.response.send_message(f"✅ **{kim.name}** yasaklandı. Sebep: {sebep}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

@bot.tree.command(name="komydynu", description="Merhaba mesajı gönderir")
async def komydynu(interaction: discord.Interaction):
    await interaction.response.send_message("islem başarili sunucuda veya kanalda açik vardir")

# --- Başlatma ---
if __name__ == "__main__":
    keep_alive() # Flask'ı başlatır
    token = os.getenv("TOKEN") # Token'ı Render panelinden alacak
    if token:
        bot.run(token)
    else:
        print("HATA: TOKEN bulunamadı. Render Environment Variables kısmına ekle!")
