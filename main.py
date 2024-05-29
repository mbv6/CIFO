from classes.population import Population
from library.selection import (
    tournament_selection,
    fitness_proportionate_selection,
    boltzmann_selection,
)
from library.xo import (
    block_single_point_xo,
    row_single_point_xo,
    row_partially_mapped_xo,
    row_uniform_xo,
)
from library.constants import (
    EASY_INITIAL_VALUES,
    MEDIUM_INITIAL_VALUES,
    HARD_INITIAL_VALUES,
)
from library.mutation import (
    block_swap_mutation,
    row_swap_mutation,
    row_random_mutation,
)
import os


def simplify_function_name(selection: object):
    name = selection.__name__

    if name == "tournament_selection":
        return "ts"
    elif name == "fitness_proportionate_selection":
        return "fps"
    elif name == "boltzmann_selection":
        return "bs"
    elif name == "block_single_point_xo":
        return "bspxo"
    elif name == "row_single_point_xo":
        return "rspxo"
    elif name == "row_partially_mapped_xo":
        return "rpmxo"
    elif name == "row_uniform_xo":
        return "uxo"
    elif name == "block_swap_mutation":
        return "bsm"
    elif name == "row_swap_mutation":
        return "rsm"
    elif name == "row_random_mutation":
        return "rrm"
    else:
        return "ERROR"


POPULATION_SIZE = 200
GENERATIONS = 1000
SELECTION = tournament_selection
TOURNAMENT_SIZE = 10
BOLTZMANN_TEMPERATURE = 50
XO_PROB = 0.8
XO = row_partially_mapped_xo
MUTATION = row_swap_mutation
MUT_PROB = 0.1
GENERATIONS_WITHOUT_IMPROVEMENT = 10
GENERATIONS_BEFORE_RESET = 30
ELITISM_RANGE = 10

COMBINATIONS_LEFT = [
    [tournament_selection, row_single_point_xo, row_swap_mutation],
    [tournament_selection, row_single_point_xo, row_random_mutation],
    [tournament_selection, row_partially_mapped_xo, row_random_mutation],
    [tournament_selection, row_uniform_xo, row_swap_mutation],
    [fitness_proportionate_selection, row_single_point_xo, row_swap_mutation],
    [fitness_proportionate_selection, row_single_point_xo, row_random_mutation],
    [fitness_proportionate_selection, row_uniform_xo, row_swap_mutation],
    [fitness_proportionate_selection, row_uniform_xo, row_random_mutation],
    [boltzmann_selection, row_uniform_xo, row_swap_mutation],
    [boltzmann_selection, row_uniform_xo, row_random_mutation],
]


for sel, xo, mut in COMBINATIONS_LEFT:
    SELECTION = sel
    XO = xo
    MUTATION = mut

    FILE_PATH = f"results/{POPULATION_SIZE}_{GENERATIONS}_{simplify_function_name(SELECTION)}_{TOURNAMENT_SIZE}_{BOLTZMANN_TEMPERATURE}_{int(XO_PROB*10)}_{simplify_function_name(XO)}_{simplify_function_name(MUTATION)}_{int(MUT_PROB*10)}_{GENERATIONS_WITHOUT_IMPROVEMENT}_{GENERATIONS_BEFORE_RESET}_{ELITISM_RANGE}"

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
