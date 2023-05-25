import numpy as np
import random
import pygame



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
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        for i, race in enumerate(people):
            for person in race:
                print(person.cords)
                self.grid[person.cords[1]][person.cords[0]] = person
        self.generate_havka()
    def generate_havka(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0 and random.random()>0.95 and self.food_count < self.size*(self.size/4):
                    self.grid[i][j] = Havka()
                    self.food_count += 1
    def run_day(self):
        
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
    def decide_state(self):
        if self.state == States.hungry:
            pass
    def decide_action(self):
        pass
    def run(self, nearby):
        pass

def main(size):
    WINDOW_SIZE = (700, 700)
    CELL_SIZE = 40
    GAP_SIZE = 10
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Cell Life Simulator")   
    world = World(size, [[Tip4yk([], Races.BLACK,(0+i, 0+i),100) for i in range(4)],
                        [Tip4yk([], Races.WHITE,(size - 1 - i, size - 1 - i),100) for i in range(4)],
                              [Tip4yk([], Races.YELLOW,(size - 1 - i, 0 + i),100) for i in range(4)],
                                  [Tip4yk([], Races.ORANGE,(0 + i, size - 1 - i),100) for i in range(4)]])
    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Visualize the world
        visualize(world, CELL_SIZE, GAP_SIZE, WINDOW_SIZE, window)
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

main(50)