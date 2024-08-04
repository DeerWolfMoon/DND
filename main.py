import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_heigth))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('arial', 32)
        
        
       
      
        
        self.character_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\People2.png')
        self.terrain_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Outside_A4.png')
        self.terrain2_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Dungeon_A2.png')
        self.ground_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Dungeon_A4.png')
        self.Wall_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Outside_C.png')
        self.enemy_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Monster.png')
        self.attacks_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SlashSpecial1.png')
        self.attacksL_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SlashSpecialL.png')
        self.attacksU_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SlashSpecialU.png')
        self.attacksR_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SlashSpecialR.png')
        self.Bosque_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\tileset2.png')
        self.Suelo_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\World_A2.png')
        self.JAIL_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SF_Outside_C.png')
        self.CASCADA_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Water4.png')
        self.Mansion_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SF_Inside_A4.png')
        self.Walls_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SF_Outside_A4.png')
        self.Enrredaderas_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Dungeon_B.png')
        self.Cofres_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\!Chest.png')
        self.Tumbas_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\SF_Outside_B.png')
        self.Vegetacion_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\Outside_B.png')
        self.Portal_spritesheet = Spritesheet(r'C:\Users\DeerWolf\Desktop\Juego\img\!Door2.png')
        self.Intro_background = pygame.image.load(r'C:\Users\DeerWolf\Desktop\Juego\img\GrassMaze.png')
        self.go_background = pygame.image.load(r'C:\Users\DeerWolf\Desktop\Juego\img\diablo.jpg')
       

    
    def createTilemap(self):
        for i, filas  in enumerate(tilemap):
            for j, columnas in enumerate(filas):
                Ground(self, j , i)
                if columnas == "B":
                    Block(self, j , i)
                if columnas =="P":
                    self.player = Player(self, j, i)
                if columnas == "E":
                    Enemy(self, j, i)
                    Mansion(self, j, i)
                if columnas == "e":
                    Enemy2(self, j, i)
                if columnas == "h":
                    Enemy3(self, j, i)
                if columnas =="1":
                    Pared1(self, j, i)
                if columnas =="2":
                    Pared2(self, j, i)
                if columnas =="3":
                    Pared3(self, j, i)
                if columnas =="4":
                    Pared4(self, j, i)
                if columnas =="5":
                    Pared5(self, j, i)
                if columnas =="6":
                    Pared6(self, j, i)
                if columnas =="F":
                    Fuente(self, j, i)
                if columnas == "*":
                    Ground2(self, j, i)
                if columnas == "R":
                    Rock(self, j, i)
                if columnas == "G":
                    Suelo(self, j, i)
                if columnas == "J":
                    JAIL(self, j, i)
                if columnas == "X":
                    CASCADA(self, j, i)
                if columnas == "M":
                    Mansion(self, j, i)
                if columnas == "W":
                    Walls(self, j, i)
                if columnas == "q":
                    Enrredaderas(self, j, i)
                    Suelo(self, j, i)
                if columnas == "Q":
                    JAIL(self, j, i)
                    Enrredaderas(self, j, i)
                if columnas == "T":
                    TumbaC(self, j, i)
                if columnas == "t":
                    TumbaL(self, j, i)
                if columnas == "C":
                    CofreG(self, j, i)
                if columnas == "p":
                    Mansion(self, j, i)
                    Portal(self, j, i)
                if columnas == "c":
                    CofreR(self, j, i)
                if columnas == "A":
                    Arbol(self, j, i)
                if columnas == "O":
                    Enemy4(self, j, i)
                if columnas == "a":
                    ARBUSTO(self, j, i)
                if columnas == "f":
                    Enemy(self, j, i)
                 

    def new(self):
        # una nueva partida comienza
        self.playing = True
        self.Win = False
        self.CofreR = False
        self.CofreG = False
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.Portal = pygame.sprite.LayeredUpdates()
        self.Item1 = pygame.sprite.LayeredUpdates()
        self.Item2 = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap()

        
    
    
    def events(self):
        #loop de eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.Win = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x-72, self.player.rect.y-96)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x-72, self.player.rect.y-50)   
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x -96, self.player.rect.y-72)   
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x-48 , self.player.rect.y-72)  

          
    def update(self):
        # loop de actulizaciones del juego
        self.all_sprites.update()
    
    def draw(self):
        #loop de dibujo 
        self.screen .fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        #Loop del juego
        while self.playing:
            self.events()
            self.update()
            self.draw()
      

    def game_over(self):
       
        for sprite in self.all_sprites:
            sprite.kill()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.Win:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                text = self.font.render("GANASTE", True, BLACK)
                text_rect = text.get_rect(center=(win_width/2, (win_heigth-50)/2))
            else:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                text = self.font.render("GAME OVER", True, BLACK)
                text_rect = text.get_rect(center=(win_width/2, (win_heigth-50)/2))

            

            restart_button = boton(10, win_heigth -60,120,50,WHITE, BLACK,'RESTART',32)
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    
    def intro_screen(self):
        intro = True
         
        title = self.font.render('ETREUM',  True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        credits = self.font.render('®DeerWolf games',  True, BLACK)
        credits_rect = title.get_rect(x=700, y=670)

        play_boton = boton(455, 160, 100, 50, WHITE, Pantano, 'Iniciar', 32)

        while intro :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro= False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_boton.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.Intro_background, (0,0))
            self.screen.blit(title, title_rect)  
            self.screen.blit(credits, credits_rect)  
            self.screen.blit(play_boton.image, play_boton.rect)
            self.clock.tick(FPS)
            pygame.display.update()



  

   

g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()
    


pygame.quit()
sys.exit()