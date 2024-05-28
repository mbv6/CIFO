if __name__ == "__main__":
    from library.population import Population
    from library.selection import tournament_selection, roulette_wheel_selection
    from library.xo import single_point_xo, two_point_xo
    from library.constants import INITIAL_VALUES
    from library.mutation import swap_mutation

pop = Population(INITIAL_VALUES, 100)

pop.evolve(
        generations=100,
        selection=tournament_selection,
        xo_prob=0.8,
        xo=single_point_xo,
        mut_prob=0.1,
        elite_len=10,
    )


