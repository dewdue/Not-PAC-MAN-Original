import pygame, sys, copy
from setting import *
from player_class import *
from enemy_class import *

pygame.init()
pygame.display.set_caption("This is not PACMAN")
vec = pygame.math.Vector2


class App:
	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True	
		self.state = "start"
		self.cell_width = MAZE_WIDTH // COLS
		self.cell_height = MAZE_HEIGHT // ROWS	
		self.walls = []
		self.coins = []
		self.enemies = []
		self.e_pos = []
		self.p_pos = None
		self.num_run_sound = 1

		self.load()

		self.player = Player(self, vec(self.p_pos))
		self.make_enemies()
		#self.load_image = 


	def run(self):
		while self.running:
			if self.state == "start":
				self.start_events()
				self.start_update()
				self.start_draw()
			elif self.state == "playing":
				self.playing_events()
				self.playing_update()
				self.playing_draw()
			elif self.state == "game over":
				self.game_over_events()
				self.game_over_update()
				self.game_over_draw()
			elif self.state == "game winner":
				self.game_winner_events()
				self.game_winner_update()
				self.game_winner_draw()
			else:
				self.running = False

			self.clock.tick(FPS)
		pygame.quit()
		sys.exit()


################ HELP #####################

	def draw_text(self, text, screen, pos, size, color, centered = False):
		font = pygame.font.SysFont("emulogic.ttf", size)
		sentence = font.render(text, True, color)
		text_size = sentence.get_size()
		#print(font)
		if centered:
			pos[0] = pos[0] - text_size[0] // 2
			pos[1] = pos[1] - text_size[1] // 2
		screen.blit(sentence, pos)

	def draw_image(self, load_image, screen, pos):
		
		screen.blit(load_image, pos)



		


	#open walls file
	#creatr walls list with co-ords of walls		
	def load(self):
		self.background = pygame.image.load("maze.png")
		self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
		with open("walls.txt", "r") as file:
			for yidx, line in enumerate(file):
				for xidx, char in enumerate(line):
					if char == "1":
						self.walls.append(vec(xidx, yidx))
					elif char == "C":
						self.coins.append(vec(xidx, yidx))
					elif char == "P":
						self.p_pos = [xidx, yidx]
						#print(len(self.walls))
					elif char in ["2", "3", "4", "5"]:
						#print(yidx, xidx)
						self.e_pos.append([xidx, yidx])
					elif char == "B":
						pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height, self.cell_width, self.cell_height))
											


	def make_enemies(self):
		for idx, pos in enumerate(self.e_pos):
			self.enemies.append(Enemy(self, vec(pos), idx))




	def draw_grid(self):
		for x in range(WIDTH // self.cell_width):
			pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
		for x in range(HEIGHT // self.cell_height):
			pygame.draw.line(self.background, GREY, (0, x * self.cell_height), (WIDTH, x * self.cell_height))
		#for wall in self.walls:
		#	pygame.draw.rect(self.background, (112, 56, 163), (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height))
		#for coin in self.coins:
		#	pygame.draw.rect(self.background, GREEN, (coin.x * self.cell_width, coin.y * self.cell_height, self.cell_width, self.cell_height))	

	def reset(self):
		self.player.lives = 3
		self.player.current_score = 0
		self.player.grid_pos = vec(self.player.starting_pos)
		self.player.pix_pos = self.player.get_pix_pos()
		self.player.direction *= 0
		for enemy in self.enemies:
			enemy.grid_pos = vec(enemy.starting_pos)
			enemy.pix_pos = enemy.get_pix_pos()
			enemy.direction *= 0

		self.coins = []
		with open("walls.txt", "r") as file:
			for yidx, line in enumerate(file):
				for xidx, char in enumerate(line):
					if char =="C":
						self.coins.append(vec(xidx, yidx))
		self.state = "playing"




################ INTRO #######################


	def start_events(self):
		for event in pygame.event.get():
			if self.num_run_sound == 1:
				pygame.mixer.music.load("sound_start.mp3")
				pygame.mixer.music.play(0)
				self.num_run_sound += 1
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.state = "playing"

	def start_update(self):
		pass

	def start_draw(self):
		self.screen.fill(BLACK)
		#font_1 = pygame.font.SysFont("emulogic.ttf", 30)
		#text_1 = font_1.render("Hello, World", True, (0, 128, 0))
		#.screen.blit(text_1, (WIDTH // 2, HEIGHT // 2))

		#pygame.image.load("PACMAN_LOGO.png")
		self.draw_image(PACMAN_LOGO, self.screen, [WIDTH // 2 - 408 // 2.1, HEIGHT // 2 - 232 * 1.2])
		self.draw_text("PUSH SPACE BAR", self.screen, [WIDTH // 2, HEIGHT // 2 + 25], START_TEXT_SIZE, ORANGE, centered = True)
		self.draw_text("1 PLAYER ONLY", self.screen, [WIDTH // 2, HEIGHT // 2 + 75], START_TEXT_SIZE, BLUE, centered = True)
		#self.draw_text("HIGH SCORE", self.screen, [4, 0], START_TEXT_SIZE, WHITE, START_FONT)

		pygame.display.update()



################ PLAYING FUNCTIONS #######################

	def playing_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.move(vec(-1,0))
				if event.key == pygame.K_RIGHT:
					self.player.move(vec(1,0))
				if event.key == pygame.K_UP:
					self.player.move(vec(0,-1))
				if event.key == pygame.K_DOWN:
					self.player.move(vec(0,1))



	def playing_update(self):
		self.player.update()
		for enemy in self.enemies:
			enemy.update()

		for enemy in self.enemies:
			if enemy.grid_pos == self.player.grid_pos:
				#print("hit")
				self.remove_life()

	def playing_draw(self):
		self.screen.fill(BLACK)
		self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
		self.draw_coins()
		#self.draw_grid()
		self.draw_text("CURRENT SCORE: {}".format(self.player.current_score), self.screen, [60,0], 30, WHITE)
		self.draw_text("HIGH SCORE: {}".format(self.player.high_score), self.screen, [WIDTH // 2 + 60,0], 30, WHITE)
		self.player.draw()
		for enemy in self.enemies:
			enemy.draw()
		pygame.display.update()

	def remove_life(self):
		self.player.lives -= 1
		if self.player.lives == 0:
			self.state = "game over"
			pygame.mixer.music.load("translate_sound_over.mp3")
			pygame.mixer.music.play(0)
		else:
			self.player.grid_pos = vec(self.player.starting_pos)
			self.player.pix_pos = self.player.get_pix_pos()
			self.player.direction *= 0
			for enemy in self.enemies:
				enemy.grid_pos = vec(enemy.starting_pos)
				enemy.pix_pos = enemy.get_pix_pos()
				enemy.direction *= 0
				
	##def score_winner(self):
	#	if self.current_score == 10:
	#		self.state = "game winner"


		

	def draw_coins(self):
		for coin in self.coins:
			pygame.draw.circle(self.screen, WHITE, (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2, int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 3)



############## GAME OVER FUNCTIONS ################

	def game_over_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.reset()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.running = False

	def game_over_update(self):
		pass


	def game_over_draw(self):
		self.screen.fill(BLACK)
		quit_text = "Press the escape botton to QUIT"
		play_again_text = "Press SPACE bar to PLAY AGAIN"
		#self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 36, RED, OVER_FONT, centered = True)
		self.draw_image(GAME_OVER_LOGO, self.screen, [WIDTH // 2 - 300 // 2.1, HEIGHT // 2 - 142 * 1.8])
		self.draw_text(play_again_text, self.screen, [WIDTH // 2, HEIGHT // 2 + 25], 36, WHITE, centered = True)
		self.draw_text(quit_text, self.screen, [WIDTH // 2, HEIGHT // 2 + 100], 36, WHITE, centered = True)
		pygame.display.update()

############## GAME WINNER FUNCTIONS #################

	def game_winner_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.reset()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.running = False

	def game_winner_update(self):
		pass


	def game_winner_draw(self):
		self.screen.fill(BLACK)
		quit_text = "Press the escape botton to QUIT"
		play_again_text = "Press SPACE bar to PLAY AGAIN"
		#self.draw_text("WINNER", self.screen, [WIDTH // 2, 100], 36, RED, OVER_FONT, centered = True)
		self.draw_image(WINNER_LOGO, self.screen, [WIDTH // 2 - 123 // 2  , HEIGHT // 2 - 165 * 1.5])
		self.draw_text(play_again_text, self.screen, [WIDTH // 2, HEIGHT // 2 + 25], 36, WHITE, centered = True)
		self.draw_text(quit_text, self.screen, [WIDTH // 2, HEIGHT // 2 + 100], 36, WHITE, centered = True)
		pygame.display.update()


