from random import shuffle, choice, sample, random, randint
from copy import copy, deepcopy
import numpy as np
from operator import attrgetter
#import functions from Operations.py
from Operations import tournament_selection, single_point_crossover, binary_mutation

# 1) Create a Grid Generator whith different difficulty levels

random.seed()

class SudokuGenerator:
    #generate valid unsolved grid
    @staticmethod
    #static methods can be called on the class itself, rather than on an instance of the class
    def generate_full_grid():
        grid = np.zeros((9, 9), dtype=int)
        SudokuGenerator.fill_grid(grid)
        return grid

    #fill the grid with valid solution
    @staticmethod
    def fill_grid(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    random.shuffle(values := list(range(1, 9 + 1)))
                    for value in values:
                        if not SudokuGenerator.is_duplicate(grid, i, j, value):
                            grid[i][j] = value
                            if SudokuGenerator.check_grid_full(grid) or SudokuGenerator.fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    #check for duplicate values
    @staticmethod
    def is_duplicate(grid, row, col, value):
        if value in grid[row]:
            return True
        if value in grid[:, col]:
            return True
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if value in grid[start_row:start_row + 3, start_col:start_col + 3]:
            return True
        return False

    #check if grid is filled out completely
    @staticmethod
    def check_grid_full(grid):
        return not any(0 in row for row in grid)

    #randomly remove num_elements from the grid
    @staticmethod
    def remove_elements(grid, num_elements):
        puzzle = grid.copy()
        for _ in range(num_elements):
            row, col = random.randint(0, 9 - 1), random.randint(0, 9 - 1)
            while puzzle[row][col] == 0:
                row, col = random.randint(0, 9 - 1), random.randint(0, 9 - 1)
            puzzle[row][col] = 0
        return puzzle

    #define how many elements are removed for each difficulty level
    @staticmethod
    def generate_puzzle(difficulty):
        full_grid = SudokuGenerator.generate_full_grid()
        if difficulty == 'easy':
            num_elements_to_remove = 51
        elif difficulty == 'medium':
            num_elements_to_remove = 55
        elif difficulty == 'hard':
            num_elements_to_remove = 60
        else:
            raise ValueError("Invalid difficulty level. Choose 'easy', 'medium', or 'hard'.")
        return SudokuGenerator.remove_elements(full_grid, num_elements_to_remove)
    


# 2) initialize the individual class
class Individual:
    #innitialize with a 9x9 grid filled with 0 or use representation
    def __init__(self, representation=None):
        self.values = np.zeros((9, 9), dtype=int) if representation is None else representation
        self.fitness = None

    #define fitness function to evaluate how close a grid is to being a valid solution
    #fitness function checks for unique values in rows, columns, and 3x3 blocks and calculates the fitness score
    def get_fitness(self):
        row_count = np.zeros(9)
        column_count = np.zeros(9)
        block_count = np.zeros(9)
        row_sum = 0
        column_sum = 0
        block_sum = 0

        #row
        for i in range(9):
            for j in range(9):
                row_count[self.values[i][j]-1] += 1
            row_sum += (1.0 / len(set(row_count))) / 9
            row_count = np.zeros(9)

        #column
        for i in range(9):
            for j in range(9):
                column_count[self.values[j][i]-1] += 1
            column_sum += (1.0 / len(set(column_count))) / 9
            column_count = np.zeros(9)

        #block
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block_count[self.values[i][j]-1] += 1
                block_count[self.values[i][j+1]-1] += 1
                block_count[self.values[i][j+2]-1] += 1
                block_count[self.values[i+1][j]-1] += 1
                block_count[self.values[i+1][j+1]-1] += 1
                block_count[self.values[i+1][j+2]-1] += 1
                block_count[self.values[i+2][j]-1] += 1
                block_count[self.values[i+2][j+1]-1] += 1
                block_count[self.values[i+2][j+2]-1] += 1
                block_sum += (1.0 / len(set(block_count))) / 9
                block_count = np.zeros(9)

        #overall
        if (int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1):
            fitness = 1.0
        else:
            fitness = column_sum * block_sum
        
        self.fitness = fitness
    
    def mutate(self, mutation_rate):
        r = random()
        if r < mutation_rate:
            while True:
                row = randint(0, 8)
                col1, col2 = sample(range(9), 2)
                if self.values[row][col1] != 0 and self.values[row][col2] != 0:
                    self.values[row][col1], self.values[row][col2] = self.values[row][col2], self.values[row][col1]
                    break


# 3) initialize the population class
class Population:
    def __init__(self, size, optim, **kwargs):
        self.size = size
        self.optim = optim
        self.individuals = [Individual() for _ in range(size)]

    def evolve(self, gens, xo_prob, mut_prob, select, xo, mutate, elitism):
        for i in range(gens):
            new_pop = []
            if elitism:
                elite = max(self.individuals, key=attrgetter('fitness')) if self.optim == "max" else min(self.individuals, key=attrgetter('fitness'))
                new_pop.append(deepcopy(elite))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                if random() < xo_prob:
                    offspring1, offspring2 = xo(parent1, parent2)
                else:
                    offspring1, offspring2 = deepcopy(parent1), deepcopy(parent2)
                if random() < mut_prob:
                    mutate(offspring1)
                if random() < mut_prob:
                    mutate(offspring2)
                new_pop.append(offspring1)
                if len(new_pop) < self.size:
                    new_pop.append(offspring2)

            self.individuals = new_pop
            best = max(self.individuals, key=attrgetter('fitness')) if self.optim == "max" else min(self.individuals, key=attrgetter('fitness'))
            print(f"Best individual of gen #{i + 1}: {best.fitness}")

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
    


# 4) Monkey patching to add the fitness function to the individual class
Individual.get_fitness = Individual().get_fitness

# 5) generate puzzle
difficulty = 'easy'  # Choose difficulty: 'easy', 'medium', 'hard'
puzzle = SudokuGenerator.generate_puzzle(difficulty)
print(f"Generated puzzle (difficulty {difficulty}):\n{puzzle}")

# 6) initialize & evolve population
# here we are using the in Operations.py defined functions
pop = Population(size=20, optim="max", sol_size=81, valid_set=[0, 1], repetition=True)
pop.evolve(gens=100, xo_prob=0.9, mut_prob=0.1, select=tournament_selection, xo=single_point_crossover, mutate=binary_mutation, elitism=True)
    



