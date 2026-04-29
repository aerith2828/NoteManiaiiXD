import pygame
import time
import os
import json

pygame.init()
pygame.mixer.init()

folder_path = os.path.dirname(os.path.abspath(__file__))
scores_file = os.path.join(folder_path, "scores", "data.json")

def loadScores(): # ładowanie wyników z pliku json
    with open(scores_file, 'r') as f:
        return json.load(f)

def saveScore(song_name, stats): # zapisywanie wyniku jeśli accuracy przewyższa stary wynik
    all_scores = loadScores()
    old_acc = all_scores.get(song_name, {}).get("accuracy", 0)
    if stats["accuracy"] >= old_acc:
        all_scores[song_name] = stats
        with open(scores_file, 'w') as f:
            json.dump(all_scores, f, indent=4)

screen_w, screen_h = 1000, 800
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("NoteMania iiXD")

font_title = pygame.font.SysFont("Impact", 70)
font_menu = pygame.font.SysFont("Impact", 32)
# font_small = pygame.font.SysFont("Arial", 16)
# font_stats = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Consolas", 16)
font_stats = pygame.font.SysFont("Consolas", 16, bold=True)
font_judge = pygame.font.SysFont("Impact", 48)
font_combo = pygame.font.SysFont("Impact", 48)

game_state = "MENU"
selected_song = 0

songs = [
    {"name": "Angelic Layer", "bms_path": os.path.join(folder_path, "notefiles", "angeliclayer.bml"), "mp3_path": os.path.join(folder_path, "music", "angeliclayer.mp3"), "offset": 0.0},
    {"name": "Total Eclipse of the Sun", "bms_path": os.path.join(folder_path, "notefiles", "totaleclipse.bms"), "mp3_path": os.path.join(folder_path, "music", "totaleclipseofthesun.mp3"), "offset": 1.75},
    {"name": "Freedom Dive", "bms_path": os.path.join(folder_path, "notefiles", "freedomdive.bml"), "mp3_path": os.path.join(folder_path, "music", "freedomdive.mp3"), "offset": 0.0},
    {"name": "Angelic Snow", "bms_path": os.path.join(folder_path, "notefiles", "angelicsnow.bme"), "mp3_path": os.path.join(folder_path, "music", "angelicsnow.mp3"), "offset": 0.1}
]

lane_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_j, pygame.K_k, pygame.K_l] # bindowanie przyciskow pod lane
lane_positions = [80, 140, 200, 260, 320, 380, 440] # pozycje X lane'ów
lane_flash = [0] * 7 # efekt podswietlenia po nacisnieciu przycisku
ingame_colors = {
    "BLUE": (0, 255, 255),
    "GREEN": (0, 255, 100),
    "RED": (255, 50, 50),
    "GRAY": (150, 150, 150),
    "WHITE": (255, 255, 255),
    "SONGMENUCOLOR": (20, 20, 30),
    "GAMECOLOR": (15, 15, 25),
    "FILLCOLOR": (5, 5, 10),
    "WELCOMEGOLDEN": (255, 165, 0),
    "LANEDIVIDIER": (40, 40, 60)
}

lane_note_colors = [(255, 255, 255), (100, 150, 255), (255, 255, 255), (255, 255, 0), (255, 255, 255), (100, 150, 255), (255, 255, 255)]

note_list = [] #lista aktywnych note
perfect_hits = 0
great_hits = 0
miss_count = 0
current_combo = 0
max_combo = 0
music_playing = False
start_time = 0
hit_offsets = []
judgment_text = "" 
judgment_color = () 
judgment_timer = 0
perfect = 0.045
missed = 0.15

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_UP: selected_song = (selected_song - 1) % len(songs)
                if event.key == pygame.K_DOWN: selected_song = (selected_song + 1) % len(songs)
                
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    target = songs[selected_song]
                    if os.path.exists(target["bms_path"]) and os.path.exists(target["mp3_path"]):
                        note_list = []
                        perfect_hits = 0
                        great_hits = 0
                        miss_count = 0
                        current_combo = 0
                        max_combo = 0
                        hit_offsets = []
                        music_playing = False
                        judgment_text = ""
                        
                        with open(target["bms_path"], 'r') as f: # silnik gameplayu, wczytywanie pliku BMS
                            bpm = 0.0
                            for line in f:
                                if "#BPM" in line:
                                    bpm = float(line.split()[-1])
                                if ":" in line and "#" in line:
                                    header, data = line[1:].split(":")
                                    channel = header[3:5]
                                    # kanał = lane
                                    mapping = {'11':0, '12':1, '13':2, '14':3, '15':4, '18':5, '19':6}
                                    lane_index = mapping.get(channel, -1)
                                    if lane_index != -1:
                                        measure = int(header[:3])
                                        data = data.strip()
                                        for i in range(0, len(data), 2):
                                            if data[i:i+2] != "00": # 00 - brak note
                                                # obliczenie czasu pojawienia się note
                                                timestamp = ((measure * 4) + (i / len(data) * 4)) * (60/bpm)
                                                note_list.append({"lane": lane_index, "time": timestamp, "active": True})
                        pygame.mixer.music.load(target["mp3_path"])
                        start_time = time.time()
                        game_state = "GAME"

            elif game_state == "GAME":

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    game_state = "MENU"

                for i in range(7): #trafienia note
                    if event.key == lane_keys[i]:
                        lane_flash[i] = 180
                        current_time = time.time() - start_time

                        for note in note_list: #najblizszy note na lane
                            if note["active"] and note["lane"] == i:
                                diff = current_time - note["time"]

                                if abs(diff) < missed: # sprawdzenie czy note zostal trafiony lub missnięty
                                    note["active"] = False
                                    current_combo += 1
                                    if current_combo > max_combo: max_combo = current_combo
                                    hit_offsets.append(diff * 1000) # opoznienie trafienia
                                    judgment_timer = time.time()
                                    if abs(diff) < perfect: # judgment trafienia <45ms -> perfect, 45-150ms -> great
                                        perfect_hits += 1
                                        judgment_text = "PERFECT"
                                        judgment_color = (ingame_colors["BLUE"])
                                    else:
                                        great_hits += 1
                                        judgment_text = "GREAT" 
                                        judgment_color = (ingame_colors["GREEN"])
                                    break

    screen.fill((ingame_colors["FILLCOLOR"]))

    #renderowanie menu  

    if game_state == "MENU":
        all_scores = loadScores()
        #tytuły
        screen.blit(font_title.render("NoteMania iiXD", True, (ingame_colors["BLUE"])), (50, 50))
        screen.blit(font_small.render("Autor: Kewin Worobiec", True, (ingame_colors["GRAY"])), (600, 130))
        #lista piosenek
        pygame.draw.rect(screen, (ingame_colors["SONGMENUCOLOR"]), (50, 180, 400, 400))
        for i in range(len(songs)):
            color = (ingame_colors["WHITE"]) if i == selected_song else (ingame_colors["GRAY"])
            text = (">> " if i == selected_song else "   ") + songs[i]["name"]
            screen.blit(font_menu.render(text, True, color), (70, 200 + i*55))
        #panel informacji
        info_x, info_y = 500, 180
        pygame.draw.rect(screen, (ingame_colors["GAMECOLOR"]), (info_x, info_y, 450, 400))
        pygame.draw.rect(screen, (ingame_colors["BLUE"]), (info_x, info_y, 450, 400), 1)
        cur = songs[selected_song]
        best = all_scores.get(cur['name'], None)
        #tekst informacji
        lines = ["--- Wybrana piosenka ---", f"Tytuł: {cur['name']}", f"Offset: {int(cur['offset']*1000)}ms", ""]
        if best:
            lines += [
                "--- NAJLEPSZY WYNIK ---",
                f"ACCURACY: {best['accuracy']:.2f}%",
                f"MAX COMBO: {best['max_combo']}",
                f"AVG ERR: {best['avg_err']:.1f}ms",
                f"P:{best['perfect']} G:{best['great']} M:{best['miss']}",
                ""
            ]
        else:
            lines += ["--- BRAK REKORDU ---", "Zagraj, aby zapisać wynik!", ""]

        lines += ["Strzałki: Wybór", "Enter: START", "Escape: Wyjście"]
        #podswietlenie najlepszego wyniku
        for i, line in enumerate(lines):
            c = (ingame_colors["GREEN"]) if "NAJLEPSZY WYNIK" in line else (ingame_colors["WHITE"])
            screen.blit(font_small.render(line, True, c), (info_x+20, info_y+30+i*22))

    elif game_state == "GAME":
        elapsed_time = time.time() - start_time
        #start muzyki z konfigurowalnym opoznieniem
        if not music_playing and elapsed_time >= songs[selected_song]["offset"]:
            pygame.mixer.music.play()
            music_playing = True

        pygame.draw.rect(screen, (ingame_colors["SONGMENUCOLOR"]), (80, 0, 420, 800))
        for lp in lane_positions: pygame.draw.line(screen, (ingame_colors["LANEDIVIDIER"]), (lp, 0), (lp, 800), 1)
        pygame.draw.rect(screen, (ingame_colors["WHITE"]), (80, 680, 420, 4)) #hitline

        for i in range(7): #efekt podswietlenia lane po nacisnieciu klawiszy
            if lane_flash[i] > 0:
                overlay = pygame.Surface((59, 800), pygame.SRCALPHA)
                overlay.fill((*ingame_colors["WHITE"], lane_flash[i])) #* rozpakowuje kolor
                screen.blit(overlay, (lane_positions[i], 0))
                lane_flash[i] -= 15

        for note in note_list: #renderowanie note
            if note["active"]:
                dist = note["time"] - elapsed_time # czas do trafienia
                if -0.2 < dist < 1.8: #renderowanie note w widocznym zasięgu
                    y_pos = 680 - (dist * 650)
                    pygame.draw.rect(screen, lane_note_colors[note["lane"]], (lane_positions[note["lane"]]+2, int(y_pos), 56, 18))
                    pygame.draw.rect(screen, (ingame_colors["WHITE"]), (lane_positions[note["lane"]]+5, int(y_pos)+2, 45, 2))
                    if dist < -missed: # sprawdzenie czy note został nietrafiony
                        note["active"] = False
                        miss_count += 1
                        current_combo = 0
                        judgment_text = "MISS"
                        judgment_color = (ingame_colors["RED"])
                        judgment_timer = time.time()

        #wyswietlania combo na ekranie
        if current_combo > 0:
            combo_on_screen = font_combo.render(str(current_combo), True, (ingame_colors["WHITE"]))
            screen.blit(combo_on_screen, (290 - combo_on_screen.get_width()//2, 150))
        #wyswietlanie judgmentu na ekranie
        if time.time() - judgment_timer < 0.4:
            judge_on_screen = font_judge.render(judgment_text, True, judgment_color)
            screen.blit(judge_on_screen, (290 - judge_on_screen.get_width()//2, 560))
        #obliczanie statystyk
        total = perfect_hits + great_hits + miss_count
        acc = ((perfect_hits + great_hits * 0.7) / total * 100) if total > 0 else 0
        avg_err = (sum(hit_offsets) / len(hit_offsets)) if hit_offsets else 0
        #wyswietlanie statystyk
        stats = [
            (f"ACCURACY: {acc:.2f}%", (ingame_colors["BLUE"])),
            (f"COMBO: {current_combo}", (ingame_colors["WHITE"])),
            (f"MAX COMBO: {max_combo}", (ingame_colors["WHITE"])),
            (f"MEAN ERR: {avg_err:+.1f}ms", (ingame_colors["WELCOMEGOLDEN"])),
            (f"PERFECT: {perfect_hits}", (ingame_colors["BLUE"])),
            (f"GREAT: {great_hits}", (ingame_colors["GREEN"])),
            (f"MISS: {miss_count}", (ingame_colors["RED"])),
            (f"FPS: {int(clock.get_fps())}", (ingame_colors["WHITE"]))
        ]

        for i, (txt, col) in enumerate(stats):
            screen.blit(font_stats.render(txt, True, col), (540, 100 + i*32))
        #koniec piosenki, zapisanie wyniku i wrocenie do menu
        if not pygame.mixer.music.get_busy() and elapsed_time > 5 and music_playing:
            saveScore(songs[selected_song]["name"], {
                "accuracy": acc,
                "max_combo": max_combo,
                "avg_err": avg_err,
                "perfect": perfect_hits,
                "great": great_hits,
                "miss": miss_count
            })
            game_state = "MENU"
    pygame.display.flip()
    clock.tick(60)
pygame.quit()