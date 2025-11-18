import requests

# ========== CONFIG ==========
GAMES = {
    "2756920": "Keep Driving",          # Steam AppID : Game Name
    "2661300": "Grounded 2",
    "1649950": "News Tower",
    "2274620": "Discounty",
    # Add more games here
}

TELEGRAM_BOT_TOKEN = "8594393626:AAF9tD3TOEh3ySBlzXmItKIb6zDwFtpNKI4"  # Your Bot Token
TELEGRAM_CHAT_ID = "5284278311"          # Your Chat ID
# ============================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_prices():
    for appid, name in GAMES.items():
        try:
            # Get current price from Steam API
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=MY&l=en"
            res = requests.get(url).json()
            data = res[appid]["data"]

            if "price_overview" not in data:
                continue  # Free game or no price

            current_price = data["price_overview"]["final"] / 100
            currency = data["price_overview"]["currency"]

            # Get lowest price from SteamDB (simple scraping)
            steamdb_url = f"https://steamdb.info/app/{appid}/"
            r = requests.get(steamdb_url)
            text = r.text
            # Simple extraction: find "Lowest recorded price"
            marker = 'Lowest recorded price</span></td><td class="price">'
            if marker in text:
                price_str = text.split(marker)[1].split('<')[0].replace('\n','').strip()
                lowest_price = float(''.join(c for c in price_str if (c.isdigit() or c=='.')))
            else:
                lowest_price = current_price

            # Compare
            if current_price <= lowest_price:
                send_telegram(f"{name} is on sale! RM{current_price} (Lowest price EVER!)")
        except Exception as e:
            print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check_prices()
