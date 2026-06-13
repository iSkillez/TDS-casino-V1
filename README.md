# 🎰 TDS Casino Bot - Discord Kasino

Víjej v tomto Discord Casino botovi s virtuální měnou **Fogo Sad Coins**!

## 📋 Funkce

✅ **3 Kasinové hry:**
- 🎲 **Kostky** - Sázka 1:2 (vyhraješ = 2x peníze)
- 🎡 **Ruleta** - 50% šance na výhru (2x peníze)
- 🎰 **Automat** - Jackpot až 10x sázka!

✅ **Správa peněz:**
- JSON databáze pro ukládání zůstatků
- Startovací bonus 1000 coinů
- Bezpečné transakce

## 🚀 Instalace

### 1. Klonuj repozitář
```bash
git clone https://github.com/iSkillez/TDS-casino-V1
cd TDS-casino-V1
```

### 2. Nainstaluj závislosti
```bash
pip install -r requirements.txt
```

### 3. Vytvoř Discord bota
1. Jdi na https://discord.com/developers/applications
2. Klikni na "New Application"
3. Pojmenuj ho (např. "Casino Bot")
4. Jdi na "Bot" a klikni "Add Bot"
5. Zkopíruj token

### 4. Nastav .env soubor
```bash
cp .env.example .env
```

Otevři `.env` a vlož svůj token:
```
DISCORD_TOKEN=tvůj_bot_token_tady
```

### 5. Spusť bota
```bash
python bot.py
```

## 📖 Příkazy

| Příkaz | Popis |
|--------|-------|
| `!start` | Získej 1000 Fogo Sad Coins (jenom jednou) |
| `!balance` | Podívej se na svůj zůstatek |
| `!dice <sázka>` | Sázej na kostky |
| `!roulette <sázka>` | Sázej na ruletě |
| `!slot <sázka>` | Sázej na automatu |
| `!help_casino` | Zobraz všechny příkazy |

## 💰 Příklady her

### Kostky
```
!dice 100
```
Tvůj hod se porovná s botem. Pokud budeš mít vyšší číslo, vyhrál jsi 200 coinů!

### Ruleta
```
!roulette 50
```
50% šance na výhru. Pokud vyhraješ, dostaneš 100 coinů!

### Automat
```
!slot 200
```
- 🍎🍎🍎 = Jackpot! 2000 coinů!
- 🍎🍎🍊 = Malá výhra! 600 coinů!
- 🍎🍊🍋 = Prohra! -200 coinů

## 📁 Struktura projektu

```
TDS-casino-V1/
├── bot.py           # Hlavní bot
├── wallets.json     # Databáze peněženek (vytvoří se automaticky)
├── requirements.txt # Závislosti
├── .env             # Tvůj Discord token
└── README.md        # Tento soubor
```

## 🎯 Rozšíření v budoucnu

Možné vylepšení:
- [ ] Leaderboard s top hráči
- [ ] Denní bonus
- [ ] Více kasinových her
- [ ] Systém úrovní
- [ ] Sázky mezi hráči

## ⚠️ Důležité

- **Nikdy** nedělej pull-requesty s `.env` souborem!
- `.env` je jen pro tvoji lokalní instalaci
- Hrát zodpovědně! 🎲

## 📞 Pomoc

Pokud máš nějaké problémy, otevři si **Issue** na GitHubu!

---

**Vytvořeno pro Tibora XD** 🎉
