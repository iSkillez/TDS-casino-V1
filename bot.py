import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Nastavení bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Soubor pro uložení peněz
WALLET_FILE = 'wallets.json'

# Funkcích pro práci s penězi
def load_wallets():
    """Načte všechny peněženky z JSON souboru"""
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_wallets(wallets):
    """Uloží peněženky do JSON souboru"""
    with open(WALLET_FILE, 'w') as f:
        json.dump(wallets, f, indent=4)

def get_balance(user_id):
    """Vrátí zůstatek uživatele"""
    wallets = load_wallets()
    return wallets.get(str(user_id), 0)

def set_balance(user_id, amount):
    """Nastaví zůstatek uživatele"""
    wallets = load_wallets()
    wallets[str(user_id)] = max(0, amount)  # Nesmí být záporné
    save_wallets(wallets)

def add_balance(user_id, amount):
    """Přidá peníze uživateli"""
    current = get_balance(user_id)
    set_balance(user_id, current + amount)

# Bot je připraven
@bot.event
async def on_ready():
    print(f'✅ Bot je online jako {bot.user}')

# ============= PŘÍKAZY =============

# Příkaz: Získat peníze (startovací bonus)
@bot.command(name='start', help='Začni s 1000 Fogo Sad Coins')
async def start(ctx):
    user_id = ctx.author.id
    current = get_balance(user_id)
    
    if current > 0:
        embed = discord.Embed(title="❌ Chyba", description=f"Už máš {current} Fogo Sad Coins! Nemůžeš si vzít bonus dvakrát.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    set_balance(user_id, 1000)
    embed = discord.Embed(
        title="🎉 Vítej v kasinu!",
        description=f"{ctx.author.mention} dostal **1000 Fogo Sad Coins**! Začni hrát: `!dice`, `!roulette`, `!slot`",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

# Příkaz: Zkontrolovat zůstatek
@bot.command(name='balance', help='Podívej se na svůj zůstatek')
async def balance(ctx):
    user_id = ctx.author.id
    amount = get_balance(user_id)
    embed = discord.Embed(
        title="💰 Tvůj zůstatek",
        description=f"Máš **{amount} Fogo Sad Coins**",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

# Příkaz: Kostky (Dice)
@bot.command(name='dice', help='Sázej na kostky! Použití: !dice <sázka>')
async def dice(ctx, bet: int):
    user_id = ctx.author.id
    balance = get_balance(user_id)
    
    # Ověření
    if bet <= 0:
        await ctx.send("❌ Sázka musí být alespoň 1 Fogo Sad Coin!")
        return
    
    if bet > balance:
        await ctx.send(f"❌ Nemáš dost peněz! Máš pouze {balance} Fogo Sad Coins.")
        return
    
    # Hra
    your_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)
    
    if your_roll > bot_roll:
        # Vyhraješ
        winnings = bet * 2
        add_balance(user_id, winnings)
        embed = discord.Embed(
            title="🎲 Kostky - VÝHRA!",
            description=f"Tvůj hod: **{your_roll}** vs Bot: **{bot_roll}**\n\n✅ Vyhrál jsi **{winnings} Fogo Sad Coins**!",
            color=discord.Color.green()
        )
    elif your_roll < bot_roll:
        # Prohraješ
        set_balance(user_id, balance - bet)
        embed = discord.Embed(
            title="🎲 Kostky - PROHRA",
            description=f"Tvůj hod: **{your_roll}** vs Bot: **{bot_roll}**\n\n❌ Ztratil jsi **{bet} Fogo Sad Coins**.",
            color=discord.Color.red()
        )
    else:
        # Remíza
        embed = discord.Embed(
            title="🎲 Kostky - REMÍZA",
            description=f"Tvůj hod: **{your_roll}** vs Bot: **{bot_roll}**\n\n🤝 Nikdo nevyhrál!",
            color=discord.Color.blue()
        )
    
    new_balance = get_balance(user_id)
    embed.add_field(name="Tvůj nový zůstatek", value=f"**{new_balance} Fogo Sad Coins**", inline=False)
    await ctx.send(embed=embed)

# Příkaz: Ruleta
@bot.command(name='roulette', help='Sázej na ruletě! Použití: !roulette <sázka>')
async def roulette(ctx, bet: int):
    user_id = ctx.author.id
    balance = get_balance(user_id)
    
    # Ověření
    if bet <= 0:
        await ctx.send("❌ Sázka musí být alespoň 1 Fogo Sad Coin!")
        return
    
    if bet > balance:
        await ctx.send(f"❌ Nemáš dost peněz! Máš pouze {balance} Fogo Sad Coins.")
        return
    
    # Hra - 50% šance
    if random.random() < 0.5:
        # Výhra
        winnings = bet * 2
        add_balance(user_id, winnings)
        emoji = "🟢"
        embed = discord.Embed(
            title="🎡 Ruleta - VÝHRA!",
            description=f"{emoji} Padla ti správná barva!\n\n✅ Vyhrál jsi **{winnings} Fogo Sad Coins**!",
            color=discord.Color.green()
        )
    else:
        # Prohra
        set_balance(user_id, balance - bet)
        emoji = "🔴"
        embed = discord.Embed(
            title="🎡 Ruleta - PROHRA",
            description=f"{emoji} Padla ti špatná barva!\n\n❌ Ztratil jsi **{bet} Fogo Sad Coins**.",
            color=discord.Color.red()
        )
    
    new_balance = get_balance(user_id)
    embed.add_field(name="Tvůj nový zůstatek", value=f"**{new_balance} Fogo Sad Coins**", inline=False)
    await ctx.send(embed=embed)

# Příkaz: Slot Machine
@bot.command(name='slot', help='Sázej na automatu! Použití: !slot <sázka>')
async def slot(ctx, bet: int):
    user_id = ctx.author.id
    balance = get_balance(user_id)
    
    # Ověření
    if bet <= 0:
        await ctx.send("❌ Sázka musí být alespoň 1 Fogo Sad Coin!")
        return
    
    if bet > balance:
        await ctx.send(f"❌ Nemáš dost peněz! Máš pouze {balance} Fogo Sad Coins.")
        return
    
    # Hra - 3 symboly
    symbols = ['🍎', '🍊', '🍋', '🍌', '💎']
    roll = [random.choice(symbols) for _ in range(3)]
    
    set_balance(user_id, balance - bet)
    
    if roll[0] == roll[1] == roll[2]:
        # Jackpot!
        winnings = bet * 10
        add_balance(user_id, winnings + bet)  # +bet protože jsme už odečetli
        embed = discord.Embed(
            title="🎰 JACKPOT!!!",
            description=f"{roll[0]} {roll[1]} {roll[2]}\n\n🎉 TŘI NA SOBĚ! Vyhrál jsi **{winnings} Fogo Sad Coins**!",
            color=discord.Color.gold()
        )
    elif roll[0] == roll[1] or roll[1] == roll[2]:
        # Dvě stejné
        winnings = bet * 3
        add_balance(user_id, winnings + bet)
        embed = discord.Embed(
            title="🎰 Malá výhra",
            description=f"{roll[0]} {roll[1]} {roll[2]}\n\n✅ Dvě stejné! Vyhrál jsi **{winnings} Fogo Sad Coins**!",
            color=discord.Color.green()
        )
    else:
        # Prohra
        embed = discord.Embed(
            title="🎰 Prohra",
            description=f"{roll[0]} {roll[1]} {roll[2]}\n\n❌ Nic se neshoduje. Ztratil jsi **{bet} Fogo Sad Coins**.",
            color=discord.Color.red()
        )
    
    new_balance = get_balance(user_id)
    embed.add_field(name="Tvůj nový zůstatek", value=f"**{new_balance} Fogo Sad Coins**", inline=False)
    await ctx.send(embed=embed)

# Příkaz: Help
@bot.command(name='help_casino', help='Všechny příkazy')
async def help_casino(ctx):
    embed = discord.Embed(
        title="🎰 Casino Bot - Nápověda",
        description="Vítej v kasinu! Tady jsou všechny příkazy:",
        color=discord.Color.purple()
    )
    embed.add_field(name="!start", value="Získej 1000 Fogo Sad Coins (jenom jednou)", inline=False)
    embed.add_field(name="!balance", value="Podívej se na svůj zůstatek", inline=False)
    embed.add_field(name="!dice <sázka>", value="Kostky - vítězství = 2x sázka", inline=False)
    embed.add_field(name="!roulette <sázka>", value="Ruleta - 50% šance, vítězství = 2x sázka", inline=False)
    embed.add_field(name="!slot <sázka>", value="Automat - jackpot = 10x sázka!", inline=False)
    embed.set_footer(text="Měna: Fogo Sad Coins | Hrát zodpovědně! 🎲")
    await ctx.send(embed=embed)

# Spuštění bota
bot.run(TOKEN)
