if __name__ == "__main__":
    from library.population import Population
    from library.selection import tournament_selection
    from library.xo import single_point_xo
    from library.constants import INITIAL_VALUES
    from library.mutation import swap_mutation

    pop = Population(INITIAL_VALUES, 5000)

    pop.evolve(
        generations=10000,
        selection=tournament_selection,
        xo_prob=0.8,
        xo=single_point_xo,
        mutation=swap_mutation,
        mut_prob=0.1,
    )

# TODO: do something when reaching local minima
# - Add a counter to the population class that counts the number of generations without improvement
# - If the counter reaches a certain threshold, reset the population
# - If the population is reset, add a mutation rate increase
# - If the population is reset, add a crossover rate decrease
