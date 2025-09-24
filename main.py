import pygame
import sys
import json
import os
import math
GAME_STATS=[{"allCookies":0,"CokiesPerSecond":0,"Cokies":0}]
UPGRADE = [
    {"name": "Leather Click", "cost": 100, "To Unlock": {"Cursors": 1},
     "description": "Clicks and Cursor are two time efficient", "Visable": False},
    {"name": "Bronze Click", "cost": 500, "To Unlock": {"Cursors": 1},
     "description": "Clicks and Cursor are two time efficient", "Visable": False},
    {"name": "Iron Click", "cost": 10000, "To Unlock": {"Cursors": 10},
     "description": "Clicks and Cursor are two time efficient", "Visable": False},
    {"name": "Iron Click", "cost": 100000, "To Unlock": {"Cursors": 25},
     "description": "Clicks and Cursor are two time efficient", "Visable": False}

]

STORE = [
    {"name": "Cursor", "cost": 15, "cps": 0.1, "count": 0,"CookieCountNeeded":0},
    {"name": "Grandma", "cost": 100, "cps": 1, "count": 0, "CookieCountNeeded":50},
    {"name": "Farm", "cost": 1100, "cps": 8, "count": 0, "CookieCountNeeded":500},
    {"name": "Mine", "cost": 12000, "cps": 47, "count": 0, "CookieCountNeeded":10000},
    {"name": "Factory", "cost": 130000, "cps": 260, "count": 0, "CookieCountNeeded":120000},
    {"name": "Bank", "cost": 1400000, "cps": 1400, "count": 0, "CookieCountNeeded":1300000}
]

ACHIEVEMENTS = [
    {"name": "First Cookie", "desc": "Click the cookie once", "unlocked": False, "check": lambda c, u: c >= 1},
    {"name": "10 Upgrades", "desc": "Own 10 upgrades total", "unlocked": False,
     "check": lambda c, u: sum(up['count'] for up in u) >= 10},
    {"name": "1k Cookies", "desc": "Reach 1,000 cookies", "unlocked": False, "check": lambda c, u: c >= 1000},
    {"name": "10K Cookies ", "desc": "Reach 10,000 cookies", "unlocked": False, "check": lambda c, u: c >= 10000}
]
# Pygame setup
pygame.init()
WIDTH, HEIGHT =1200, 600
WHITE, BLACK, GRAY, GREEN, BROWN = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 155, 0), (210, 180, 140)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# Objects & Data
cookie_rect = pygame.Rect(100, 150, 160, 160)
upgrade_rects = [pygame.Rect(350, 80 + i * 70, 350, 60) for i in range(len(STORE))]
# For example, starting at x=350, y=550 and vertically spaced by 70 px
store_rects = [pygame.Rect(720, 80 + i * 70, 350, 60) for i in range(len(UPGRADE))]

save_button = pygame.Rect(1100, 30, 80, 40)
load_button = pygame.Rect(1100, 80, 80, 40)

allCookies=0
cookies = 0
cps = 0
click_multiplier = 1
# New variable for click power
def recalc_cps():
    global cps
    cps = 0
    for upg in STORE:
        cps += upg["cps"] * upg["count"]


def draw():
    screen.fill(WHITE)
    # Cookie
    pygame.draw.ellipse(screen, BROWN, cookie_rect)
    screen.blit(font.render("Cookie", True, BLACK), (cookie_rect.x + 30, cookie_rect.y + 60))
    # Stats
    screen.blit(font.render(f"All Time Cookies: {millify(int(allCookies))}", True, BLACK), (40, 1))
    screen.blit(font.render(f"Cookies: {millify(int(cookies))}", True, BLACK), (40, 40))
    screen.blit(font.render(f"Cookies/sec: {cps:.1f}", True, BLACK), (40, 80))
    screen.blit(font.render(f"Cookies/click: {click_multiplier}", True, BLACK), (40, 120))  # Show click multiplier
    #Store
    drawAndUpdateUpgrades()
    #Upgrades

    drawUpgrades()
    # Achievements
    screen.blit(font.render("Achievements:", True, BLACK), (40, 350))
    for i, ach in enumerate(ACHIEVEMENTS):
        color = GREEN if ach["unlocked"] else BLACK
        screen.blit(font.render(f"- {ach['name']}", True, color), (60, 380 + i * 25))
    # Save/Load
    pygame.draw.rect(screen, GRAY, save_button)
    screen.blit(font.render("Save", True, BLACK), (save_button.x + 10, save_button.y + 5))
    pygame.draw.rect(screen, GRAY, load_button)
    screen.blit(font.render("Load", True, BLACK), (load_button.x + 10, load_button.y + 5))

def drawAndUpdateUpgrades():
    screen.blit(font.render("Store", True, BLACK), (350, 50))
    mouse_pos = pygame.mouse.get_pos()
    for i, up in enumerate(STORE):
        if up["CookieCountNeeded"] <= allCookies:

            rect = upgrade_rects[i]
            # Draw the upgrade box
            pygame.draw.rect(screen, GRAY, rect)
            txt = f"{up['name']} ({up['count']}) - Cost: {millify(int(up['cost']))}"
            screen.blit(font.render(txt, True, BLACK), (rect.x + 10, rect.y + 15))
            # Check for hover
            if rect.collidepoint(mouse_pos):
                # Draw the CPS info text on hover
                if(up['count']==0):
                    hover_text = f"+{up['cps']} cps"
                else:
                    hover_text = f"+{up['cps']} cps. You get {millify(up['cps'] * up['count'])}/sec"
                hover_surface = font.render(hover_text, True, BLACK)
                # Position the hover text slightly above or near the upgrade rectangle
                if(i==0):
                    hover_pos = (rect.x + 60, rect.y - hover_surface.get_height() - 5)
                else:
                    hover_pos = (rect.x, rect.y - hover_surface.get_height() - 5)
                screen.blit(hover_surface, hover_pos)
def drawUpgrades():
    screen.blit(font.render("Upgrades", True, BLACK), (720, 50))
    mouse_pos = pygame.mouse.get_pos()
def save_game(filename="savegame.json"):
    state = {
        "allCookies":allCookies,
        "cookies": cookies,
        "cps": cps,
        "store": STORE,
        "achievements": [ach["unlocked"] for ach in ACHIEVEMENTS],
        "click_multiplier": click_multiplier
    }
    with open(filename, "w") as f:
        json.dump(state, f)

def millify(n):
    numnames = ['', 'K', ' Mil', ' Bil', ' Tril']
    n = float(n)
    numidx = max(0, min(len(numnames) - 1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    return '{:.1f}{}'.format(n / 10**(3 * numidx), numnames[numidx])


def load_game(filename="savegame.json"):
    global cookies, cps, STORE, ACHIEVEMENTS, click_multiplier ,allCookies
    if os.path.exists(filename):
        with open(filename, "r") as f:
            state = json.load(f)
        allCookies = state.get("allCookies",0)
        cookies = state.get("cookies", 0)
        cps = state.get("cps", 0)
        up_saved = state.get("upgrades", [])
        for i in range(min(len(up_saved), len(STORE))):
            STORE[i].update(up_saved[i])
        ach_saved = state.get("achievements", [])
        for i, unlocked in enumerate(ach_saved):
            if i < len(ACHIEVEMENTS):
                ACHIEVEMENTS[i]["unlocked"] = unlocked
        click_multiplier = state.get("click_multiplier", 1)


def buy_store(idx):
    global cookies, cps, click_multiplier
    u = STORE[idx]
    if cookies >= u["cost"]:
        cookies -= u["cost"]
        u["count"] += 1
        cps += u["cps"]
        u["cost"] = int(u["cost"] * 1.20)
        if u["name"] == "Click Multiplier":
            click_multiplier *= 2


def check_achievements():
    for ach in ACHIEVEMENTS:
        if not ach["unlocked"] and ach["check"](cookies, STORE):
            ach["unlocked"] = True
# Modify buy_upgrades()



def buy_upgrades(idx):
    global cookies,click_multiplier
    u = UPGRADE[idx]
    if cookies >= u["cost"] and u["Visable"] and not u.get("purchased", False):
        cookies -= u["cost"]
        u["purchased"] = True
        u["Visable"] = False
        u["cost"] = 0
        click_multiplier = click_multiplier*2
        # Find related store item by name from upgrade, example hardcoded here:
        related_store_name = "Cursor"  # customize per upgrade if needed

        # Multiply cps of related store item by 2
        for store_item in STORE:
            if store_item["name"] == related_store_name:
                store_item["cps"] *= 2

        recalc_cps()



def update_upgrade_visibility():
    for u in UPGRADE:
        if not u["Visable"]:
            unlocked = True
            for key, val in u["To Unlock"].items():
                # Singularize key crudely: remove trailing 's' if plural
                key_singular = key[:-1] if key.endswith("s") else key
                found = False
                for store_item in STORE:
                    if store_item["name"] == key_singular:
                        found = True
                        if store_item["count"] < val:
                            unlocked = False
                            break
                if not found:
                    unlocked = False
            if unlocked:
                u["Visable"] = True


def drawUpgrades():
    screen.blit(font.render("Upgrades", True, BLACK), (720, 50))
    mouse_pos = pygame.mouse.get_pos()
    for i, u in enumerate(UPGRADE):
        if u["Visable"] and not u.get("purchased", False):
            rect = store_rects[i]
            pygame.draw.rect(screen, GRAY, rect)
            cost_text = f"Cost: {millify(int(u['cost']))}" if u["cost"] > 0 else "Purchased"
            txt = f"{u['name']} - {cost_text}"
            screen.blit(font.render(txt, True, BLACK), (rect.x + 10, rect.y + 15))
            if rect.collidepoint(mouse_pos):
                desc_surf = font.render(u["description"], True, BLACK)
                screen.blit(desc_surf, (rect.x, rect.y - desc_surf.get_height() - 5))


# Main Game Loop
running = True
cps_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if cookie_rect.collidepoint(x, y):
                cookies += click_multiplier
                allCookies += click_multiplier
            for i, rect in enumerate(upgrade_rects):
                if rect.collidepoint(x, y):
                    buy_store(i)
            for i, rect in enumerate(store_rects):
                if rect.collidepoint(x, y):
                    buy_upgrades(i)
            if save_button.collidepoint(x, y):
                save_game()
            if load_button.collidepoint(x, y):
                load_game()
    update_upgrade_visibility()
    # Accumulate cookies/sec
    dt = clock.tick(60)
    cps_timer += dt
    if cps_timer >= 1000:
        cookies += cps
        allCookies += cps
        cps_timer = 0
    check_achievements()
    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
