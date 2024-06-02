from classes.population import Population
from library.constants import (
    EASY_INITIAL_VALUES,
    MEDIUM_INITIAL_VALUES,
    HARD_INITIAL_VALUES,
)
from library.utils import simplify_function_name
from library.constants import COMBINATIONS
import os


POPULATION_SIZE = 200
GENERATIONS = 1000
TOURNAMENT_SIZE = 10
BOLTZMANN_TEMPERATURE = 50
XO_PROB = 0.8
MUT_PROB = 0.1
GENERATIONS_WITHOUT_IMPROVEMENT = 10
GENERATIONS_BEFORE_RESET = 30
ELITISM_RANGE = 0

for SELECTION, XO, MUTATION in COMBINATIONS:
    FILE_PATH = f"results_no_elitism/{POPULATION_SIZE}_{GENERATIONS}_{simplify_function_name(SELECTION)}_{TOURNAMENT_SIZE}_{BOLTZMANN_TEMPERATURE}_{int(XO_PROB*10)}_{simplify_function_name(XO)}_{simplify_function_name(MUTATION)}_{int(MUT_PROB*10)}_{GENERATIONS_WITHOUT_IMPROVEMENT}_{GENERATIONS_BEFORE_RESET}_{ELITISM_RANGE}"

    for i in range(10):
        pop = Population(EASY_INITIAL_VALUES, POPULATION_SIZE)

        df = pop.evolve(
            generations=GENERATIONS,
            selection=SELECTION,
            tournament_size=TOURNAMENT_SIZE,
            boltzmann_temperature=BOLTZMANN_TEMPERATURE,
            xo_prob=XO_PROB,
            xo=XO,
            mutation=MUTATION,
            mut_prob=MUT_PROB,
            generations_without_improvement=GENERATIONS_WITHOUT_IMPROVEMENT,
            generations_before_reset=GENERATIONS_BEFORE_RESET,
            elitism_range=ELITISM_RANGE,
        )

        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)

        df.to_csv(f"{FILE_PATH}/{i}.csv")
