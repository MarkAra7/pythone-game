import pygame
import sys
import json
import os
GAME_STATS=[{"TotalCookies":0,"CokiesPerSecond":0,"Cokies":0}]
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
    {"name": "Cursor", "cost": 15, "cps": 0.1, "count": 0},
    {"name": "Grandma", "cost": 100, "cps": 1, "count": 0},
    {"name": "Farm", "cost": 1100, "cps": 8, "count": 0},
    {"name": "Mine", "cost": 12000, "cps": 47, "count": 0},
    {"name": "Factory", "cost": 130000, "cps": 260, "count": 0},
    {"name": "Bank", "cost": 1400000, "cps": 1400, "count": 0}
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
WIDTH, HEIGHT = 1000, 600
WHITE, BLACK, GRAY, GREEN, BROWN = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 155, 0), (210, 180, 140)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# Objects & Data
cookie_rect = pygame.Rect(100, 150, 160, 160)
upgrade_rects = [pygame.Rect(350, 80 + i * 70, 430, 60) for i in range(len(STORE))]
save_button = pygame.Rect(900, 30, 80, 40)
load_button = pygame.Rect(900, 80, 80, 40)

cookies = 0
cps = 0
click_multiplier = 1  # New variable for click power



def draw():
    screen.fill(WHITE)
    # Cookie
    pygame.draw.ellipse(screen, BROWN, cookie_rect)
    screen.blit(font.render("Cookie", True, BLACK), (cookie_rect.x + 30, cookie_rect.y + 60))
    # Stats
    screen.blit(font.render(f"Cookies: {int(cookies)}", True, BLACK), (40, 40))
    screen.blit(font.render(f"Cookies/sec: {cps:.1f}", True, BLACK), (40, 80))
    screen.blit(font.render(f"Cookies/click: {click_multiplier}", True, BLACK), (40, 120))  # Show click multiplier
    # Upgrades
    screen.blit(font.render("Upgrades", True, BLACK), (350, 50))
    for i, up in enumerate(STORE):
        rect = upgrade_rects[i]
        pygame.draw.rect(screen, GRAY, rect)
        txt = f"{up['name']} ({up['count']}) - +{up['cps']} cps - Cost: {int(up['cost'])}"
        screen.blit(font.render(txt, True, BLACK), (rect.x + 10, rect.y + 15))
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


def save_game(filename="savegame.json"):
    state = {
        "cookies": cookies,
        "cps": cps,
        "store": STORE,
        "achievements": [ach["unlocked"] for ach in ACHIEVEMENTS],
        "click_multiplier": click_multiplier
    }
    with open(filename, "w") as f:
        json.dump(state, f)


def load_game(filename="savegame.json"):
    global cookies, cps, STORE, ACHIEVEMENTS, click_multiplier
    if os.path.exists(filename):
        with open(filename, "r") as f:
            state = json.load(f)
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


def buy_upgrade(idx):
    global cookies, cps, click_multiplier
    u = STORE[idx]
    if cookies >= u["cost"]:
        cookies -= u["cost"]
        u["count"] += 1
        cps += u["cps"]
        u["cost"] = int(u["cost"] * 1.15)
        if u["name"] == "Click Multiplier":
            click_multiplier *= 2


def check_achievements():
    for ach in ACHIEVEMENTS:
        if not ach["unlocked"] and ach["check"](cookies, STORE):
            ach["unlocked"] = True


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
            for i, rect in enumerate(upgrade_rects):
                if rect.collidepoint(x, y):
                    buy_upgrade(i)
            if save_button.collidepoint(x, y):
                save_game()
            if load_button.collidepoint(x, y):
                load_game()
    # Accumulate cookies/sec
    dt = clock.tick(60)
    cps_timer += dt
    if cps_timer >= 1000:
        cookies += cps
        cps_timer = 0
    check_achievements()
    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
