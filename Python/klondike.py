import random
import json
import base64
import os
import time

#   CONSTANTS

CIPHER_KEY = 42  # XOR key for save encryption

PICKAXES = {
    "Wooden":  {"price":    0, "min": 1, "max": 8,  "emoji": "", "crit": 0.05},
    "Iron":    {"price":  80, "min": 4, "max": 15,  "emoji": "",  "crit": 0.10},
    "Steel":   {"price": 250, "min": 8, "max": 25,  "emoji": "", "crit": 0.18},
    "Golden":  {"price": 700, "min": 15, "max": 45, "emoji": "", "crit": 0.30},
}

PICKAXE_ORDER = ["Wooden", "Iron", "Steel", "Golden"]

#   SAVE / LOAD  (XOR cipher + base64)

def encrypt(data: dict) -> str:
    raw = json.dumps(data).encode()
    xored = bytes(b ^ CIPHER_KEY for b in raw)
    return base64.b64encode(xored).decode()

def decrypt(code: str) -> dict:
    try:
        xored = base64.b64decode(code.encode())
        raw = bytes(b ^ CIPHER_KEY for b in xored)
        return json.loads(raw.decode())
    except Exception:
        return None

#   DISPLAY HELPERS

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def hr(char="─", width=42):
    print(char * width)

def pause():
    input("\n  Press Enter to continue...")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def header(player):
    pickaxe = player["pickaxe"]
    emoji   = PICKAXES[pickaxe]["emoji"]
    hr("═")
    print(f"  KLONDIKE GOLD RUSH")
    hr("═")
    print(f"  {player['name']}   |   {player['gold']:.1f}g   |   {emoji} {pickaxe} Pickaxe")
    print(f"  Day {player['day']}   |   Digs: {player['total_digs']}   |   Best find: {player['best_find']}g")
    hr()

#   MINING

def mine(player):
    clear()
    header(player)
    p  = PICKAXES[player["pickaxe"]]
    print("\n  You swing your pickaxe into the rock face...\n")
    time.sleep(1)

    # Critical hit?
    crit = random.random() < p["crit"]
    found = round(random.uniform(p["min"], p["max"]) * (2.5 if crit else 1), 1)

    # Rare chance of finding nothing
    if random.random() < 0.15:
        slow_print("  Nothing but dust this time. Tough luck, miner.")
        found = 0
    elif crit:
        slow_print(f"  RICH VEIN! You struck a golden pocket!")
        slow_print(f"  You found {found}g of gold!  (Critical!)")
    else:
        slow_print(f"  You chipped away and found {found}g of gold.")

    player["gold"] += found
    player["gold"]  = round(player["gold"], 1)
    player["total_digs"] += 1
    player["day"]  += 1
    if found > player["best_find"]:
        player["best_find"] = found

    pause()

#   SHOP

def shop(player):
    clear()
    header(player)
    print("\n  GENERAL STORE")
    hr()

    current_idx = PICKAXE_ORDER.index(player["pickaxe"])

    for i, name in enumerate(PICKAXE_ORDER):
        p = PICKAXES[name]
        if i < current_idx:
            status = "  owned"
        elif i == current_idx:
            status = "  you have this"
        else:
            status = f"  {p['price']}g"
        range_str = f"{p['min']}–{p['max']}g/dig"
        crit_str  = f"crit {int(p['crit']*100)}%"
        print(f"  [{i+1}] {p['emoji']} {name:<8}  {range_str:<14} {crit_str:<10} {status}")

    hr()
    print("  [0] Back to camp")
    choice = input("\n  Buy which pickaxe? › ").strip()

    if choice == "0":
        return
    if not choice.isdigit() or int(choice) - 1 not in range(len(PICKAXE_ORDER)):
        print("  Invalid choice.")
        pause()
        return

    idx  = int(choice) - 1
    name = PICKAXE_ORDER[idx]
    p    = PICKAXES[name]

    if idx <= current_idx:
        print("\n  You already own this or better.")
    elif player["gold"] < p["price"]:
        print(f"\n  Not enough gold! You need {p['price']}g.")
    else:
        player["gold"]    -= p["price"]
        player["gold"]     = round(player["gold"], 1)
        player["pickaxe"]  = name
        slow_print(f"\n  You bought the {name} Pickaxe! Happy mining!")
    pause()

#   SALOON GAMBLING  (High-Low dice)

def saloon(player):
    clear()
    header(player)
    print("\n  GOLDEN NUGGET SALOON")
    hr()
    print("  Roll two dice. Guess if the total will be HIGH (8-12)")
    print("  or LOW (2-6). A roll of 7 means the house wins.")
    hr()
    print(f"  Your gold: {player['gold']}g")
    print("  [0] Back to camp")
    hr()

    bet_input = input("  How much do you bet? › ").strip()
    if bet_input == "0":
        return

    try:
        bet = float(bet_input)
    except ValueError:
        print("  Enter a valid number.")
        pause()
        return

    if bet <= 0:
        print("  Bet must be positive.")
        pause()
        return
    if bet > player["gold"]:
        print("  You don't have that much gold!")
        pause()
        return

    print("\n  Guess HIGH or LOW?")
    print("  [H] High (8–12)   [L] Low (2–6)")
    guess = input("  Your call › ").strip().upper()
    if guess not in ("H", "L"):
        print("  Type H or L.")
        pause()
        return

    time.sleep(0.5)
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    total  = d1 + d2
    print(f"\n  Rolling... [{d1}] + [{d2}] = {total}")
    time.sleep(1)

    if total == 7:
        slow_print("  Lucky 7 — the house always wins. You lose your bet.")
        player["gold"] -= bet
    elif (total >= 8 and guess == "H") or (total <= 6 and guess == "L"):
        slow_print(f"  Correct! You win {bet}g!")
        player["gold"] += bet
    else:
        slow_print(f"  Wrong call. You lose {bet}g.")
        player["gold"] -= bet

    player["gold"] = round(max(player["gold"], 0), 1)
    player["day"] += 1
    pause()

#   SAVE CODE

def show_save_code(player):
    clear()
    header(player)
    code = encrypt(player)
    print("\n  YOUR SAVE CODE")
    hr()
    print("  Copy this and keep it safe!\n")
    print(f"  {code}")
    hr()
    print("  Paste it at the start of the game to resume.")
    pause()

#   MAIN MENU

def main_menu(player):
    while True:
        clear()
        header(player)
        print()
        print("  [1]  Go Mining")
        print("  [2]  General Store")
        print("  [3]  Visit the Saloon")
        print("  [4]  Get Save Code")
        print("  [5]  Quit")
        hr()
        choice = input("  What will you do? › ").strip()

        if choice == "1":
            mine(player)
        elif choice == "2":
            shop(player)
        elif choice == "3":
            saloon(player)
        elif choice == "4":
            show_save_code(player)
        elif choice == "5":
            clear()
            slow_print("\n  Thanks for playing, partner. See you in the Klondike!\n")
            break
        else:
            print("  Invalid option.")
            time.sleep(0.8)

#   STARTUP

def new_game():
    clear()
    hr("═")
    slow_print("  Welcome to the KLONDIKE, stranger.")
    slow_print("  Gold won't mine itself.")
    hr("═")
    name = input("\n  What's your name, miner? › ").strip() or "Stranger"
    return {
        "name":       name,
        "gold":       10.0,
        "pickaxe":    "Wooden",
        "day":        1,
        "total_digs": 0,
        "best_find":  0,
    }

def load_game():
    clear()
    hr("═")
    print("  LOAD SAVE")
    hr("═")
    code = input("\n  Paste your save code › ").strip()
    data = decrypt(code)
    if data is None:
        print("\n  Invalid code. Starting a new game instead.")
        time.sleep(2)
        return new_game()
    slow_print(f"\n  Welcome back, {data['name']}!")
    time.sleep(1)
    return data

def startup():
    clear()
    print()
    hr("═")
    print("   K L O N D I K E   G O L D   R U S H")
    hr("═")
    print()
    print("  [1]  New Game")
    print("  [2]  Load from Save Code")
    hr()
    choice = input("  › ").strip()
    if choice == "2":
        return load_game()
    return new_game()

#   ENTRY POINT

if __name__ == "__main__":
    player = startup()
    main_menu(player)