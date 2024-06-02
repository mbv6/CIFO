# Objective
The project explores Genetic Algorithms (GAs) to develop a solution for Sudoku puzzles. The goal is to define a fitness function and various GA techniques to find the most effective combination for solving Sudoku puzzles.


## Without Elistism 
## Selection Results 

| Selection                       |   overall_average_generations |
|:--------------------------------|------------------------------:|
| boltzmann_selection             |                       816.022 |
| fitness_proportionate_selection |                       837.388 |
| tournament_selection            |                       966.666 |

## Crossover Results

| Crossover               |   overall_average_generations |
|:------------------------|------------------------------:|
| row_partially_mapped_xo |                      854.1888 |
| row_single_point_xo     |                      980.9444 |
| row_uniform_xo          |                      784.9444 |

## Mutation Results

| Mutation               |   overall_average_generations |
|:-----------------------|------------------------------:|
| row_inversion_mutation |                       906.044 |
| row_random_mutation    |                       870.488 |
| row_swap_mutation      |                       843.544 |


## Combination Results
| Selection                       | Crossover               | Mutation               |   Average Generations |   Solved Puzzles |
|:--------------------------------|:------------------------|:-----------------------|----------------------:|-----------------:|
| boltzmann_selection             | row_uniform_xo          | row_random_mutation    |                 578.1 |                6 |
| fitness_proportionate_selection | row_uniform_xo          | row_random_mutation    |                 672   |                5 |
| boltzmann_selection             | row_uniform_xo          | row_swap_mutation      |                 526.1 |                5 |
| fitness_proportionate_selection | row_uniform_xo          | row_inversion_mutation |                 713.9 |                4 |
| fitness_proportionate_selection | row_partially_mapped_xo | row_inversion_mutation |                 630.1 |                4 |
| boltzmann_selection             | row_partially_mapped_xo | row_swap_mutation      |                 616.8 |                4 |
| fitness_proportionate_selection | row_partially_mapped_xo | row_random_mutation    |                 788.2 |                3 |
| fitness_proportionate_selection | row_uniform_xo          | row_swap_mutation      |                 810.7 |                2 |
| tournament_selection            | row_uniform_xo          | row_random_mutation    |                 956.2 |                1 |
| tournament_selection            | row_partially_mapped_xo | row_random_mutation    |                 934   |                1 |
| fitness_proportionate_selection | row_single_point_xo     | row_swap_mutation      |                 921.6 |                1 |
| tournament_selection            | row_partially_mapped_xo | row_swap_mutation      |                 907.1 |                1 |
| boltzmann_selection             | row_single_point_xo     | row_swap_mutation      |                 906.9 |                1 |
| boltzmann_selection             | row_partially_mapped_xo | row_random_mutation    |                 905.9 |                1 |
| boltzmann_selection             | row_partially_mapped_xo | row_inversion_mutation |                 905.6 |                1 |
| boltzmann_selection             | row_uniform_xo          | row_inversion_mutation |                 904.8 |                1 |
| tournament_selection            | row_uniform_xo          | row_swap_mutation      |                 902.7 |                1 |
| boltzmann_selection             | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| boltzmann_selection             | row_single_point_xo     | row_random_mutation    |                1000   |                0 |
| fitness_proportionate_selection | row_partially_mapped_xo | row_swap_mutation      |                1000   |                0 |
| fitness_proportionate_selection | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| fitness_proportionate_selection | row_single_point_xo     | row_random_mutation    |                1000   |                0 |
| tournament_selection            | row_partially_mapped_xo | row_inversion_mutation |                1000   |                0 |
| tournament_selection            | row_single_point_xo     | row_inversion_mutation |                1000   |                0 |
| tournament_selection            | row_single_point_xo     | row_random_mutation    |                1000   |                0 |
| tournament_selection            | row_single_point_xo     | row_swap_mutation      |                1000   |                0 |
| tournament_selection            | row_uniform_xo          | row_inversion_mutation |                1000   |                0 |

## With Elitism
## Selection Results

| Selection                       |   overall_average_generations |
|:--------------------------------|------------------------------:|
| boltzmann_selection             |                       614.611 |
| fitness_proportionate_selection |                       738.733 |
| tournament_selection            |                       888.011 |

## Crossover Results

| Crossover               |   overall_average_generations |
|:------------------------|------------------------------:|
| row_partially_mapped_xo |                       559.933 |
| row_single_point_xo     |                       976.756 |
| row_uniform_xo          |                       704.667 |

## Mutation Results

| Mutation               |   overall_average_generations |
|:-----------------------|------------------------------:|
| row_inversion_mutation |                       794.667 |
| row_random_mutation    |                       775.1   |
| row_swap_mutation      |                       671.589 |

## Combination Results

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
