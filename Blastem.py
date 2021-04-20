import pygame
import sys
import random
import json


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.images = [(pygame.image.load("blastem-dependencies/player.PNG")), (pygame.image.load("blastem-dependencies/player_death.PNG"))]
        self.dead = False
        self.delete = 0.0
        self.move = 0
        self.height = height
        self.width = width
        self.alive = True
        self.bullet1 = None
        self.bullet2 = None
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos

    def collide(self):
        if self.rect.top < self.height/2:
            self.rect.top = self.height/2

        if self.rect.bottom > screen_height - self.height/2:
            self.rect.bottom = screen_height - self.height/2

    def check_kill(self):
        if not self.dead and (pygame.sprite.spritecollide(self, enemy_group, False) or pygame.sprite.spritecollide(self, enemy_bullet_group, True)):
            pygame.mixer.Sound.play(player_kill)
            self.dead = True
            self.image = self.images[1]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.delete >= 2.6:
            if not self.alive:
                self.alive = True
                self.rect.x, self.rect.y = self.x_pos, self.y_pos
                self.delete = 0.0
                self.dead = False
                self.image = self.images[0]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            else:
                self.alive = False

    def create_bullets(self):
        self.bullet1 = PlayerBullet(self.rect.x + 46, self.rect.y + 10, 4, 2)
        self.bullet2 = PlayerBullet(self.rect.x + 46, self.rect.y + 38, 4, 2)

    def update(self):
        if not self.dead:
            self.rect.y += self.move
            self.collide()
        else:
            self.delete += 0.1
            self.rect.x -= 6

        self.check_kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.images = [(pygame.image.load("blastem-dependencies/enemy_1.PNG")), (pygame.image.load("blastem-dependencies/enemy_death.PNG"))]
        self.dead = False
        self.delete = 0.0
        self.width = width
        self.height = height
        self.bullet1 = None
        self.bullet2 = None
        self.spawn_enemy_bullet = 10
        self.y_move = random.choice([-2, 2])

        self.image = self.images[0]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos

    def check_kill(self):
        global score

        if self.rect.x < 0 - self.width:
            self.kill()

        if (pygame.sprite.spritecollide(self, player_bullet_group, True) or pygame.sprite.spritecollide(self, player_group, False)) and not self.dead and self.rect.x <= screen_width - self.width:
            pygame.mixer.Sound.play(enemy_kill)
            self.dead = True
            self.image = self.images[1]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.y_move *= -1
            score += 10

        if not player.alive:
            self.kill()

        if self.delete >= 1.6:
            self.kill()

    def create_bullets(self):
        pygame.mixer.Sound.play(shoot_sound)
        self.bullet1 = EnemyBullet(self.rect.x + 12, self.rect.y + 10, 4, 2)
        self.bullet2 = EnemyBullet(self.rect.x + 12, self.rect.y + 38, 4, 2)
        enemy_bullet_group.add(self.bullet1)
        enemy_bullet_group.add(self.bullet2)
        self.spawn_enemy_bullet = 0

    def move_y(self):
        if self.rect.top < 25:
            self.y_move = 2

        if self.rect.bottom > screen_height - 25:
            self.y_move = -2

        self.rect.y += self.y_move

    def update(self):
        if not self.dead:
            if self.rect.x <= screen_width - 150:
                self.rect.x -= 2
            else:
                self.rect.x -= 6

            if self.spawn_enemy_bullet > 48:
                self.create_bullets()

            self.spawn_enemy_bullet += 1
        else:
            self.delete += 0.1
            self.rect.x += 6

        self.move_y()
        self.check_kill()


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.speed = 8

        self.image = pygame.image.load("blastem-dependencies/player_bullet.PNG")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos

    def check_kill(self):
        if self.rect.x > screen_width:
            self.kill()

        if not player.alive:
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.check_kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.speed = 6
        self.width = width

        self.image = pygame.image.load("blastem-dependencies/enemy_bullet.PNG")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos

    def check_kill(self):
        if self.rect.x < 0 - self.width:
            self.kill()

        if not player.alive:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.check_kill()


# Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
menu = "main"

# Window
screen_height = 620
screen_width = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blast'em!")
background = (0, 0, 0)

icon = pygame.image.load("blastem-dependencies/window_icon.PNG")
pygame.display.set_icon(icon)

# Scores
score = 0
high_score = 0

data = {
    "high": 0
}

try:
    with open("blastem-dependencies/save_data.txt") as save_file:
        data = json.load(save_file)
        high_score = data["high"]
        print("File loaded successfully!")
except:
    print("No file found. Scores reset.")


# Enemies
enemy_group = pygame.sprite.Group()
spawn_enemy = 60
spawn_rate = 160

enemy_bullet_group = pygame.sprite.Group()
spawn_enemy_bullet = 10

# Player
player = Player(31, screen_height/2 - 25, 62, 50)
player_group = pygame.sprite.Group()
player_group.add(player)

player_bullet_group = pygame.sprite.Group()
shoot = False
spawn_bullet = 10

# Sounds
enemy_kill = pygame.mixer.Sound("blastem-dependencies/explode1.wav")
player_kill = pygame.mixer.Sound("blastem-dependencies/explode2.wav")
shoot_sound = pygame.mixer.Sound("blastem-dependencies/shoot2.wav")
select_sound = pygame.mixer.Sound("blastem-dependencies/select1.wav")
shoot_sound.set_volume(0.2)
select_sound.set_volume(0.4)

# Fonts
main_font = pygame.font.Font("blastem-dependencies/PressStart2P.ttf", 16)

# Main Menu
title_surf = main_font.render(f"BLAST'EM!", True, (255, 255, 255))
title_rect = title_surf.get_rect(center=(screen_width/2, screen_height/2 - 48))

play_but_surf = main_font.render(f"PLAY", True, (255, 255, 255))
play_but_rect = play_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 16))

if high_score > 0:
    reset_but_color = (239, 75, 63)
else:
    reset_but_color = (50, 50, 50)

reset_but_surf = main_font.render(f"RESET HISCORE", True, reset_but_color)
reset_but_rect = reset_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 48))

# Reset Y/N Menu
reset_title_surf = main_font.render(f"ARE YOU SURE?", True, (255, 255, 255))
reset_title_rect = reset_title_surf.get_rect(center=(screen_width/2, screen_height/2 - 48))

reset_yes_but_surf = main_font.render(f"YES", True, (239, 75, 63))
reset_yes_but_rect = reset_yes_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 16))

reset_no_but_surf = main_font.render(f"NO", True, (255, 255, 255))
reset_no_but_rect = reset_no_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 48))

# Death Menu
dead_title_surf = main_font.render(f"YOU DIED!", True, (239, 75, 63))
dead_title_rect = dead_title_surf.get_rect(center=(screen_width/2, screen_height/2 - 48))

retry_but_surf = main_font.render(f"RETRY", True, (255, 255, 255))
retry_but_rect = retry_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 16))

menu_but_surf = main_font.render(f"BACK TO MENU", True, (255, 255, 255))
menu_but_rect = menu_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 48))

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move -= 8
            if event.key == pygame.K_DOWN:
                player.move += 8
            if event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.move += 8
            if event.key == pygame.K_DOWN:
                player.move -= 8
            if event.key == pygame.K_SPACE:
                shoot = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_but_rect.collidepoint(event.pos) and menu == "main":
                pygame.mixer.Sound.play(select_sound)

                enemy_bullet_group.draw(screen)
                enemy_bullet_group.update()
                enemy_group.draw(screen)
                enemy_group.update()

                player_bullet_group.draw(screen)
                player_bullet_group.update()
                player_group.draw(screen)
                player_group.update()

                menu = "game"

            elif reset_but_rect.collidepoint(event.pos) and high_score > 0 and menu == "main":
                pygame.mixer.Sound.play(select_sound)
                menu = "reset_yn"

            elif reset_yes_but_rect.collidepoint(event.pos) and menu == "reset_yn":
                pygame.mixer.Sound.play(select_sound)
                menu = "main"
                data = {
                    "high": 0
                }

                with open("blastem-dependencies/save_data.txt", "w") as save_file:
                    json.dump(data, save_file)

                high_score = 0
                reset_but_color = (50, 50, 50)

            elif reset_no_but_rect.collidepoint(event.pos) and menu == "reset_yn":
                pygame.mixer.Sound.play(select_sound)
                menu = "main"

            elif menu_but_rect.collidepoint(event.pos) and menu == "death":
                pygame.mixer.Sound.play(select_sound)

                if high_score > 0:
                    reset_but_color = (239, 75, 63)
                else:
                    reset_but_color = (50, 50, 50)

                menu = "main"

            if retry_but_rect.collidepoint(event.pos) and menu == "death":
                pygame.mixer.Sound.play(select_sound)

                enemy_bullet_group.draw(screen)
                enemy_bullet_group.update()
                enemy_group.draw(screen)
                enemy_group.update()

                player_bullet_group.draw(screen)
                player_bullet_group.update()
                player_group.draw(screen)
                player_group.update()

                menu = "game"

        # Title Screen
        if play_but_rect.collidepoint(pygame.mouse.get_pos()):
            play_but_surf = main_font.render(f"> PLAY <", True, (255, 255, 255))
            play_but_rect = play_but_surf.get_rect(center=(screen_width/2, screen_height/2 + 16))
        else:
            play_but_surf = main_font.render(f"PLAY", True, (255, 255, 255))
            play_but_rect = play_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 16))

        if reset_but_rect.collidepoint(pygame.mouse.get_pos()) and high_score > 0:
            reset_but_surf = main_font.render(f"> RESET HISCORE <", True, reset_but_color)
            reset_but_rect = reset_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))
        else:
            reset_but_surf = main_font.render(f"RESET HISCORE", True, reset_but_color)
            reset_but_rect = reset_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))

        # Reset Y/N Screen
        if reset_no_but_rect.collidepoint(pygame.mouse.get_pos()):
            reset_no_but_surf = main_font.render(f"> NO <", True, (255, 255, 255))
            reset_no_but_rect = reset_no_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))
        else:
            reset_no_but_surf = main_font.render(f"NO", True, (255, 255, 255))
            reset_no_but_rect = reset_no_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))

        if reset_yes_but_rect.collidepoint(pygame.mouse.get_pos()):
            reset_yes_but_surf = main_font.render(f"> YES <", True, (239, 75, 63))
            reset_yes_but_rect = reset_yes_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 16))
        else:
            reset_yes_but_surf = main_font.render(f"YES", True, (239, 75, 63))
            reset_yes_but_rect = reset_yes_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 16))

        # Death Screen
        if menu_but_rect.collidepoint(pygame.mouse.get_pos()):
            menu_but_surf = main_font.render(f"> BACK TO MENU <", True, (255, 255, 255))
            menu_but_rect = menu_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))
        else:
            menu_but_surf = main_font.render(f"BACK TO MENU", True, (255, 255, 255))
            menu_but_rect = menu_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 48))

        if retry_but_rect.collidepoint(pygame.mouse.get_pos()):
            retry_but_surf = main_font.render(f"> RETRY <", True, (255, 255, 255))
            retry_but_rect = retry_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 16))
        else:
            retry_but_surf = main_font.render(f"RETRY", True, (255, 255, 255))
            retry_but_rect = retry_but_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 16))

    screen.fill(background)

    if menu == "game":
        if spawn_enemy > spawn_rate:
            enemy = Enemy(screen_width + 62, random.randrange(25, screen_height - 75), 62, 50)
            enemy_group.add(enemy)
            spawn_enemy = 0
        if shoot and player.alive and spawn_bullet > 16:
            player.create_bullets()
            pygame.mixer.Sound.play(shoot_sound)
            player_bullet_group.add(player.bullet1)
            player_bullet_group.add(player.bullet2)
            spawn_bullet = 0
        if spawn_rate > 60:
            spawn_rate -= 0.01

        enemy_bullet_group.draw(screen)
        enemy_bullet_group.update()
        enemy_group.draw(screen)
        enemy_group.update()
        spawn_enemy += 1

        player_bullet_group.draw(screen)
        player_bullet_group.update()
        player_group.draw(screen)
        player_group.update()
        spawn_bullet += 1

        # Restarting
        if not player.alive:
            # Enemies
            spawn_enemy = 60
            spawn_rate = 160

            spawn_enemy_bullet = 10

            # Player Bullets
            shoot = False
            spawn_bullet = 10

            # Resetting Score
            if score > high_score:
                data = {
                    "high": score
                }

                with open("blastem-dependencies/save_data.txt", "w") as save_file:
                    json.dump(data, save_file)

                high_score = score

            score = 0

            menu = "death"

        score_text = main_font.render(f"{'SCORE: ' + str(score)}", True, (255, 255, 255))
        high_score_text = main_font.render(f"{'HISCORE: ' + str(high_score)}", True, (255, 255, 255))
        high_score_text_rect = high_score_text.get_rect(topright=(screen_width - 11, 11))
        screen.blit(score_text, (11, 11))
        screen.blit(high_score_text, high_score_text_rect)
    elif menu == "main":
        screen.blit(play_but_surf, play_but_rect)
        screen.blit(reset_but_surf, reset_but_rect)
        screen.blit(title_surf, title_rect)
    elif menu == "reset_yn":
        screen.blit(reset_yes_but_surf, reset_yes_but_rect)
        screen.blit(reset_no_but_surf, reset_no_but_rect)
        screen.blit(reset_title_surf, reset_title_rect)
    elif menu == "death":
        screen.blit(menu_but_surf, menu_but_rect)
        screen.blit(retry_but_surf, retry_but_rect)
        screen.blit(dead_title_surf, dead_title_rect)

    # print(spawn_rate)
    pygame.display.flip()
    clock.tick(60)
