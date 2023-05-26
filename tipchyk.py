from itertools import product

import numpy as np
import random
import pygame
import math
import time


class States:
    hungry = 'hungry'
    horny = 'horny'
    exploring = 'exploring'
    rage = 'rage'
    dead = 'dead'

class Races:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    GREEN = (0, 255, 0)

class World:
    def __init__(self, size, people) -> None:
        self.food_count = 0
        self.max_food_count = 0
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        for i, race in enumerate(people):
            for person in race:
                self.grid[person.cords[0]][person.cords[1]] = person
        self.generate_havka(10)
        self.recharge()

    def generate_havka(self, radius,):
        def _create_cluster_spawn(grid, center_coords, radius,prob_decrease):
            '''
            Takes the center of cluster and radius.
            Further from center means less probability of spawning food.
            '''

            for loc_rad in range(1,radius):
                for i in range(center_coords[1]-loc_rad,center_coords[1]+loc_rad):
                    for j in range(center_coords[0]-loc_rad,center_coords[0]+loc_rad):
                        try:
                            if random.random() < 1/loc_rad-prob_decrease and grid[i][j] == 0:
                                grid[i][j] = Havka()
                                self.food_count += 1
                        except IndexError:
                            continue

        for tup in [(radius//2, radius//2),
                    (self.size-radius//2-1, radius//2-1),
                    (radius//2-1, self.size-radius//2-1),
                    (self.size-radius//2-1, self.size-radius//2-1)]:
            _create_cluster_spawn(self.grid, tup, radius, 0.05)
        # [_create_cluster_spawn(self.grid, (coord1//2, coord2//2),random.randint(5,10), random.random()/10) for coord1, coord2 in zip([random.choice([i for i in range(10)]) for _ in range(10)], [random.choice([i for i in range(10)]) for _ in range(10)])]
        rand_y = []
        for _ in range(3):
            rand_y.append(random.choice(list(range(-10,5))))
        for _ in range(3):
            rand_y.append(random.choice(list(range(-5,0))))
        for _ in range(3):
            rand_y.append(random.choice(list(range(0,5))))
        for _ in range(3):
            rand_y.append(random.choice(list(range(5,10))))
        print(rand_y)
        rand_x = []
        for _ in range(3):
            rand_x.append(random.choice(list(range(-10,5))))
        for _ in range(3):
            rand_x.append(random.choice(list(range(-5,0))))
        for _ in range(3):
            rand_x.append(random.choice(list(range(0,5))))
        for _ in range(3):
            rand_x.append(random.choice(list(range(5,10))))
        print(rand_x)
        for coord_y, coord_x in zip(rand_y, rand_x):
            _create_cluster_spawn(self.grid, ((self.size//10)*coord_y, (self.size//10)*coord_x//2),random.randint(5,10), random.random()/10)

        _create_cluster_spawn(self.grid, (self.size//2, self.size//2), 15, 0.01)

    def recharge(self):
        if self.food_count < (self.size ** 2)//8:
            for _ in range((self.size**2)//10000):
                x = random.randint(0,self.size - 1)
                y = random.randint(0,self.size - 1)
                if self.grid[y][x] == 0:
                    self.grid[y][x] = Havka()

    def run_day(self):
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.grid[i][j], Tip4yk):
                    self.grid[i][j].run(self)
        self.recharge()

    def __str__(self):
        return str('\n'.join(str(line) for line in self.grid))
    

class Havka():
    def __init__(self) -> None:
        self.recharge = 40

class Tip4yk:
    def __init__(self, genom, race, cords, start_energy, start_state = States.hungry) -> None:
        self.genom = genom
        self.race = race
        self.cords = cords
        self.state = start_state
        self.energy = start_energy

    def find_nearby_food(self, world):
        grid = world.grid
        ans = []
        for r in range(1,3):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Havka) \
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            ans.append((self.cords[0]+i, self.cords[1]+j))
                    except IndexError:
                        continue
        if not ans:
            return None
        return random.choice(ans)
    def find_nearby_enemy(self, grid):
        for r in range(1,5):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk)\
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            if grid[self.cords[0]+i][self.cords[1]+j].race != self.race:
                                return (self.cords[0]+i, self.cords[1]+j)
                    except IndexError:
                        continue
        return None

    def move(self, world, new_cords):
        world.grid[self.cords[0]][self.cords[1]] = 0
        self.cords[0] = new_cords[0]
        self.cords[1] = new_cords[1]
        if isinstance(world.grid[new_cords[0]][new_cords[1]], Havka):
            self.energy += world.grid[new_cords[0]][new_cords[1]].recharge
            world.food_count -= 1
        world.grid[new_cords[0]][new_cords[1]] = self
        self.energy -= 1

    def random_move(self, world):
        grid = world.grid
        for _ in range(1000):
            new_y = self.cords[0] + random.randint(0, 2) - 1 
            new_x = self.cords[1] + random.randint(0, 2) - 1
            if 0<= new_y<=len(grid) - 1 and 0<= new_x<=len(grid) - 1:
                if (new_y,new_x) != self.cords and not isinstance(grid[new_y][new_x], Tip4yk):
                    self.move(world,(new_y, new_x))
                    break

    def die(self, grid):
        grid[self.cords[0]][self.cords[1]] = 0


    def short_distance(self, grid, goal_cords):
        possible_x = []
        possible_y = []
        moves = []
        for i in range(-1, 2):
            possible_y.append(self.cords[0]+i)
        for j in range(-1, 2):
            possible_x.append(self.cords[1]+j)

        for p in product(possible_y, possible_x):
            moves.append(p)

        possible_moves = []
        for move in moves:
            if 0 <= move[0] < len(grid) and 0 <= move[1] < len(grid):
                possible_moves.append(move)
        best_move = possible_moves[0]
        for move in possible_moves:
            if math.dist(move, goal_cords) < math.dist(best_move, goal_cords):
                best_move = move
        return move


    def fight(self, enemy):
        if random.random() > 0.5:
            return enemy
        return self.cords

    def decide_state(self, world):
        if self.energy < 0:
            self.state = States.dead
        if self.state == States.hungry and self.energy >80:
            self.state = States.rage

    def decide_action(self, world):
        if self.state == States.dead:
            self.die(world.grid)
        if self.state == States.hungry:
            nearby = self.find_nearby_food(world)
            if nearby:
                diffy = nearby[0] - self.cords[0]
                diffx = nearby[1] - self.cords[1]
                if diffx < -1:
                    diffx = -1
                if diffx > 1:
                    diffx = 1
                if diffy < -1:
                    diffy = -1
                if diffy > 1:
                    diffy = 1
                self.move(world,(self.cords[0] + diffy, self.cords[1] + diffx))
            else:
                self.random_move(world)


        if self.state == States.rage:
            grid = world.grid
            nearby_enemy = self.find_nearby_enemy(grid)
            if nearby_enemy:
                if int(math.dist(nearby_enemy, self.cords)) == 1:
                    loser = self.fight(nearby_enemy)
                    print(f'Hope negro was killed')
                    grid[loser[0]][loser[1]] = 0
                else:
                    move = self.short_distance(grid, nearby_enemy)
                    self.move(world, move)
            else:
                self.state = States.hungry
                move = self.random_move(world)


    def run(self, world):
        self.decide_action(world)
        self.decide_state(world)

def main(size):
    WINDOW_SIZE = (700, 700)
    CELL_SIZE = 40
    GAP_SIZE = 0
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Cell Life Simulator")   
    world = World(size, [[Tip4yk([], Races.BLACK,[0+i, 0+i],100) for i in range(8)],
                        [Tip4yk([], Races.WHITE,[size - 1 - i, size - 1 - i],100) for i in range(8)],
                              [Tip4yk([], Races.YELLOW,[0 + i,size - 1 - i],100) for i in range(8)],
                                  [Tip4yk([], Races.ORANGE,[size - 1 - i, 0 + i],100) for i in range(8)]])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualize(world, CELL_SIZE, GAP_SIZE, WINDOW_SIZE, window)
        world.run_day()
    pygame.quit()





def visualize(world, CELL_SIZE, GAP_SIZE, WINDOW_SIZE, window):
    # Calculate the grid dimensions based on the world size
    grid_width = world.size * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
    grid_height = world.size * (CELL_SIZE + GAP_SIZE) + GAP_SIZE

    # Create a surface for the grid
    grid_surface = pygame.Surface((grid_width, grid_height))

    # Clear the grid surface
    grid_surface.fill(Races.BLACK)

    # Draw the cells on the grid surface
    for i in range(world.size):
        for j in range(world.size):
            cell = world.grid[i][j]

            # Define the color based on the cell's race
            color = None
            if isinstance(cell, Havka):
                color = Races.GREEN
            elif cell == 0:
                color = (100,100,100)
            else:
                color = cell.race

            # Calculate the cell position on the grid surface
            cell_x = j * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            cell_y = i * (CELL_SIZE + GAP_SIZE) + GAP_SIZE

            # Draw the cell rectangle on the grid surface
            pygame.draw.rect(grid_surface, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

    # Scale the grid surface to fit the window
    scaled_surface = pygame.transform.scale(grid_surface, WINDOW_SIZE)

    # Update the window
    window.blit(scaled_surface, (0, 0))
    pygame.display.flip()

main(100)