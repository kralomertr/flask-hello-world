from flask.cli import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
load_dotenv()
TOKEN = os.getenv('TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        # Botun temel izinlerini (intents) ayarlıyoruz
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Komutları Discord'a global olarak kaydeder
        await self.tree.sync()
        print(f"Komutlar senkronize edildi!")

bot = MyBot()

# Birinci Komut: /komutlu
@bot.tree.command(name="spam", description="Tek mesajın içinde 100 kez deneme yazar")
async def spam(interaction: discord.Interaction):
    
    # 1'den 100'e kadar "deneme1", "deneme2" şeklinde bir liste oluşturup 
    # aralarına boşluk koyarak tek bir uzun metin (string) yapıyoruz.
    uzun_mesaj = " ".join([f"deneme {i+1}" for i in range(100)])
    
    try:
        # Sadece 1 kere yanıt verdiğimiz için Discord bunu engellemez 
        # ve bot sunucuda ekli olmasa bile herkes görebilir.
        await interaction.response.send_message(uzun_mesaj)
        
    except Exception as e:
        print(f"Hata oluştu: {e}")


@bot.tree.command(name="ban", description="Belirlediğiniz üyeyi sunucudan yasaklar.")
@app_commands.describe(kim="Yasaklanacak üyeyi seçin", sebep="Yasaklanma sebebi (isteğe bağlı)")
@app_commands.checks.has_permissions(ban_members=False) # False yerine True olmalı
async def ban(interaction: discord.Interaction, kim: discord.Member, sebep: str = "Belirtilmedi"):
    try:
        await kim.ban(reason=sebep)
        await interaction.response.send_message(f"✅ **{kim.name}** başarıyla yasaklandı.\n**Sebep:** {sebep}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Bir hata oluştu: {e}", ephemeral=True)


# İkinci Komut: /komydynu
@bot.tree.command(name="komydynu", description="Merhaba mesajı gönderir")
async def komydynu(interaction: discord.Interaction):
    await  interaction.response.send_message("islem başarili sunucuda veya kanalda açik vardir")

# Botu başlat (Tokenini buraya yapıştır)
bot.run(os.getenv("TOKEN"))


# Botun 7/24 açık kalması 
@app.route('/')
