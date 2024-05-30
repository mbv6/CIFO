# Selection Results

| Selection                       |   overall_average_generations |
|:--------------------------------|------------------------------:|
| boltzmann_selection             |                       614.611 |
| fitness_proportionate_selection |                       738.733 |
| tournament_selection            |                       888.011 |

# Crossover Results

| Crossover               |   overall_average_generations |
|:------------------------|------------------------------:|
| row_partially_mapped_xo |                       559.933 |
| row_single_point_xo     |                       976.756 |
| row_uniform_xo          |                       704.667 |

# Mutation Results

| Mutation               |   overall_average_generations |
|:-----------------------|------------------------------:|
| row_inversion_mutation |                       794.667 |
| row_random_mutation    |                       775.1   |
| row_swap_mutation      |                       671.589 |

# Combination Results

| Selection                       | Crossover               | Mutation               |   Average Generations |   Solved Puzzles |
|:--------------------------------|:------------------------|:-----------------------|----------------------:|-----------------:|
| fitness_proportionate_selection | row_partially_mapped_xo | row_swap_mutation      |                 311.2 |               10 |
| boltzmann_selection             | row_uniform_xo          | row_random_mutation    |                 268.8 |               10 |
| fitness_proportionate_selection | row_partially_mapped_xo | row_inversion_mutation |                 424.8 |                9 |
| boltzmann_selection             | row_uniform_xo          | row_swap_mutation      |                 408.1 |                9 |
| boltzmann_selection             | row_partially_mapped_xo | row_inversion_mutation |                 378   |                9 |
| boltzmann_selection             | row_partially_mapped_xo | row_swap_mutation      |                 349.2 |                8 |
| boltzmann_selection             | row_partially_mapped_xo | row_random_mutation    |                 499   |                7 |
| fitness_proportionate_selection | row_partially_mapped_xo | row_random_mutation    |                 744.9 |                6 |
| fitness_proportionate_selection | row_uniform_xo          | row_swap_mutation      |                 616.5 |                6 |
| tournament_selection            | row_partially_mapped_xo | row_swap_mutation      |                 576.2 |                6 |
| fitness_proportionate_selection | row_uniform_xo          | row_random_mutation    |                 715.2 |                5 |
| boltzmann_selection             | row_uniform_xo          | row_inversion_mutation |                 681.7 |                5 |
| tournament_selection            | row_partially_mapped_xo | row_random_mutation    |                 857.1 |                4 |
| fitness_proportionate_selection | row_uniform_xo          | row_inversion_mutation |                 836   |                4 |
| tournament_selection            | row_partially_mapped_xo | row_inversion_mutation |                 899   |                3 |
| tournament_selection            | row_uniform_xo          | row_random_mutation    |                 890.9 |                3 |
| tournament_selection            | row_single_point_xo     | row_swap_mutation      |                 844.1 |                2 |
| tournament_selection            | row_uniform_xo          | row_swap_mutation      |                 992.3 |                1 |
| boltzmann_selection             | row_single_point_xo     | row_swap_mutation      |                 946.7 |                1 |
| tournament_selection            | row_uniform_xo          | row_inversion_mutation |                 932.5 |                1 |
| boltzmann_selection             | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| boltzmann_selection             | row_single_point_xo     | row_random_mutation    |                1000   |                0 |
| fitness_proportionate_selection | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| fitness_proportionate_selection | row_single_point_xo     | row_random_mutation    |                1000   |                0 |
| fitness_proportionate_selection | row_single_point_xo     | row_swap_mutation      |                1000   |                0 |
| tournament_selection            | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| tournament_selection            | row_single_point_xo     | row_random_mutation    |                1000   |                0 |