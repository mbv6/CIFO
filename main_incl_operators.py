from random import shuffle, choice, sample, randint
import random as rnd
from copy import copy, deepcopy
import numpy as np
from operator import attrgetter

rnd.seed()  # Correctly call the seed method from the renamed random module

class SudokuGenerator:
    @staticmethod
    def generate_full_grid():
        grid = np.zeros((9, 9), dtype=int)
        SudokuGenerator.fill_grid(grid)
        return grid

    @staticmethod
    def fill_grid(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    rnd.shuffle(values := list(range(1, 9 + 1)))
                    for value in values:
                        if not SudokuGenerator.is_duplicate(grid, i, j, value):
                            grid[i][j] = value
                            if SudokuGenerator.check_grid_full(grid) or SudokuGenerator.fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    @staticmethod
    def is_duplicate(grid, row, col, value):
        if value in grid[row] or value in grid[:, col]:
            return True
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if value in grid[start_row:start_row + 3, start_col:start_col + 3]:
            return True
        return False

    @staticmethod
    def check_grid_full(grid):
        return not any(0 in row for row in grid)

    @staticmethod
    def remove_elements(grid, num_elements):
        puzzle = grid.copy()
        filled_positions = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] != 0]
        rnd.shuffle(filled_positions)
        
        for _ in range(num_elements):
            if len(filled_positions) == 0:
                break

            row, col = filled_positions.pop()
            temp = puzzle[row][col]
            puzzle[row][col] = 0

            if not SudokuGenerator.is_valid_puzzle(puzzle):
                puzzle[row][col] = temp
            else:
                continue

        return puzzle

    @staticmethod
    def is_valid_puzzle(puzzle):
        for i in range(9):
            if np.count_nonzero(puzzle[i, :]) < 3 or np.count_nonzero(puzzle[:, i]) < 3:
                return False
        return True

    @staticmethod
    def generate_puzzle(difficulty):
        full_grid = SudokuGenerator.generate_full_grid()
        if difficulty == 'easy':
            num_elements_to_remove = 30
        elif difficulty == 'medium':
            num_elements_to_remove = 40
        elif difficulty == 'hard':
            num_elements_to_remove = 50
        else:
            raise ValueError("Invalid difficulty level. Choose 'easy', 'medium', or 'hard'.")
        return SudokuGenerator.remove_elements(full_grid, num_elements_to_remove)


class Individual:
    def __init__(self, representation=None):
        self.values = np.zeros((9, 9), dtype=int) if representation is None else representation
        self.fitness = None

    def get_fitness(self):
        row_count = np.zeros(9)
        column_count = np.zeros(9)
        block_count = np.zeros(9)
        row_sum = 0
        column_sum = 0
        block_sum = 0

        for i in range(9):
            for j in range(9):
                row_count[self.values[i][j]-1] += 1
            row_sum += (1.0 / len(set(row_count))) / 9
            row_count = np.zeros(9)

        for i in range(9):
            for j in range(9):
                column_count[self.values[j][i]-1] += 1
            column_sum += (1.0 / len(set(column_count))) / 9
            column_count = np.zeros(9)

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

        if (int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1):
            fitness = 1.0
        else:
            fitness = column_sum * block_sum
        
        self.fitness = fitness

    def mutate(self, mutation_rate, max_attempts=100):
        if rnd.random() < mutation_rate:
            for row in range(9):
                attempts = 0
                while attempts < max_attempts:
                    col1, col2 = rnd.sample(range(9), 2)
                    if self.values[row][col1] != 0 and self.values[row][col2] != 0:
                        self.values[row][col1], self.values[row][col2] = self.values[row][col2], self.values[row][col1]
                        break
                    attempts += 1
                if attempts == max_attempts:
                    self.random_reset_mutation()

    def random_reset_mutation(self):
        row = rnd.randint(0, 8)
        col = rnd.randint(0, 8)
        while self.values[row][col] != 0:
            row = rnd.randint(0, 8)
            col = rnd.randint(0, 8)
        valid_values = list(range(1, 10))
        rnd.shuffle(valid_values)
        for value in valid_values:
            if not SudokuGenerator.is_duplicate(self.values, row, col, value):
                self.values[row][col] = value
                break

class Population:
    def __init__(self, size, optim, **kwargs):
        self.size = size
        self.optim = optim
        self.individuals = [self.generate_diverse_individual() for _ in range(size)]
        
        for individual in self.individuals:
            individual.get_fitness()

    def generate_diverse_individual(self):
        individual = Individual()
        for i in range(9):
            row = rnd.sample(range(1, 10), 9)
            individual.values[i] = row
        return individual

    def evolve(self, gens, xo_prob, mut_prob, select, xo, mutate, elitism):
        for i in range(gens):
            new_pop = []
            if elitism:
                elite = max(self.individuals, key=attrgetter('fitness')) if self.optim == "max" else min(self.individuals, key=attrgetter('fitness'))
                new_pop.append(deepcopy(elite))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                if rnd.random() < xo_prob:
                    offspring1, offspring2 = xo(parent1, parent2)
                else:
                    offspring1, offspring2 = deepcopy(parent1), deepcopy(parent2)
                if rnd.random() < mut_prob:
                    mutate(offspring1)
                if rnd.random() < mut_prob:
                    mutate(offspring2)
                new_pop.append(offspring1)
                if len(new_pop) < self.size:
                    new_pop.append(offspring2)

            self.individuals = new_pop
            
            for individual in self.individuals:
                individual.get_fitness()

            best = max(self.individuals, key=attrgetter('fitness')) if self.optim == "max" else min(self.individuals, key=attrgetter('fitness'))
            print(f"Best individual of gen #{i + 1}: {best.fitness}")

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

def get_fitness(self):
    row_count = np.zeros(9)
    column_count = np.zeros(9)
    block_count = np.zeros(9)
    row_sum = 0
    column_sum = 0
    block_sum = 0

    for i in range(9):
        for j in range(9):
            row_count[self.values[i][j]-1] += 1
        row_sum += (1.0 / len(set(row_count))) / 9
        row_count = np.zeros(9)

    for i in range(9):
        for j in range(9):
            column_count[self.values[j][i]-1] += 1
        column_sum += (1.0 / len(set(column_count))) / 9
        column_count = np.zeros(9)

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

    if int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1:
        fitness = 1.0
    else:
        fitness = column_sum * block_sum
    
    self.fitness = fitness

Individual.get_fitness = get_fitness

def tournament_selection(population, k=3):
    return max(sample(population.individuals, k), key=lambda ind: ind.fitness)

def single_point_crossover(parent1, parent2):
    point = randint(0, 8)
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    child1.values[point:], child2.values[point:] = parent2.values[point:], parent1.values[point:]
    return child1, child2

def binary_mutation(individual, mutation_rate=0.1, max_attempts=100):
    for row in range(9):
        if rnd.random() < mutation_rate:
            attempts = 0
            while attempts < max_attempts:
                col1, col2 = rnd.sample(range(9), 2)
                if individual.values[row][col1] != 0 and individual.values[row][col2] != 0:
                    individual.values[row][col1], individual.values[row][col2] = individual.values[row][col2], individual.values[row][col1]
                    break
                attempts += 1
            else:
                print(f"Mutation failed to find non-zero values in row {row} after {max_attempts} attempts.")

difficulty = 'easy'
puzzle = SudokuGenerator.generate_puzzle(difficulty)
print(f"Generated Sudoku (difficulty {difficulty}):\n{puzzle}")

pop = Population(size=30, optim="max")
for individual in pop.individuals:
    individual.get_fitness()

pop.evolve(gens=5000, xo_prob=0.9, mut_prob=0.1, select=tournament_selection, xo=single_point_crossover, mutate=binary_mutation, elitism=True)

best_individual = max(pop.individuals, key=attrgetter('fitness'))
print("Best solution grid:")
print(best_individual.values)