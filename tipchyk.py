import numpy as np
import random
import pygame
import time


class States:
    hungry = 'hungry'
    horny = 'horny'
    exploring = 'exploring'
    rage = 'rage'

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
        self.generate_havka()

    def generate_havka(self):
        def _create_cluster_spawn(grid, center_coords, radius):
            '''
            Takes the center of cluster and radius.
            Further from center means less probability of spawning food.
            '''
            for loc_rad in range(1,radius):
                for i in range(center_coords[1]-loc_rad,center_coords[1]+loc_rad):
                    for j in range(center_coords[0]-loc_rad,center_coords[0]+loc_rad):
                        if  random.random() < 1/loc_rad-0.05 and grid[i][j] == 0:
                            grid[i][j] = Havka()
                            self.food_count += 1
                            if self.food_count == self.max_food_count:
                                break
        for tup in [(self.size//4, self.size//4),
                    (self.size-(self.size//4), self.size//4),
                    (self.size//4, self.size-self.size//4),
                    (self.size - self.size//4, self.size-self.size//4),
                    (self.size//2, self.size//2)]:
            _create_cluster_spawn(self.grid, tup, 20)

    def run_day(self):
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.grid[i][j], Tip4yk):
                    self.grid[i][j].run(self.grid)

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
    def find_nearby_food(self, grid):
        for r in range(1,3):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Havka):
                            return (self.cords[0]+i, self.cords[1]+j)
                    except IndexError:
                        continue
        return None
    def move(self, grid, new_cords):
        grid[self.cords[0]][self.cords[1]] = 0
        self.cords[0] = new_cords[0]
        self.cords[1] = new_cords[1]
        grid[new_cords[0]][new_cords[1]] = self
    def decide_state(self):
        if self.state == States.hungry:
            pass
    def decide_action(self, grid):
        if self.state == States.hungry:
            nearby = self.find_nearby_food(grid)
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
                self.move(grid,(self.cords[0] + diffy, self.cords[1] + diffx))
            while True:
                new_y = self.cords[0] + random.randint(0, 2) - 1 
                new_x = self.cords[1] + random.randint(0, 2) - 1
                if 0<= new_y<=len(grid) - 1 and 0<= new_x<=len(grid) - 1:
                    if (new_y,new_x) != self.cords and not isinstance(grid[new_y][new_x], Tip4yk):
                        self.move(grid,(new_y, new_x))
                        break

    def run(self, grid):
        self.decide_action(grid)

def main(size):
    WINDOW_SIZE = (700, 700)
    CELL_SIZE = 40
    GAP_SIZE = 10
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