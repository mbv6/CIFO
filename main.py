if __name__ == "__main__":
    from classes.population import Population
    from library.selection import tournament_selection
    from library.xo import single_point_xo, row_single_point_xo, uniform_xo
    from library.constants import INITIAL_VALUES
    from library.mutation import swap_mutation, row_swap_mutation

    pop = Population(INITIAL_VALUES, 2000)

    pop.evolve(
        generations=10000,
        selection=tournament_selection,
        xo_prob=0.8,
        xo=uniform_xo,
        mutation=row_swap_mutation,
        mut_prob=0.1,
        generations_without_improvement=10,
        elitism_range=10,
    )


# TODO: do something when reaching local minima
# - Add a counter to the population class that counts the number of generations without improvement
# - If the counter reaches a certain threshold, reset the population
# - If the population is reset, add a mutation rate increase
# - If the population is reset, add a crossover rate decrease
