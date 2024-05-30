import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

# Directory containing the CSV files
csv_folders_path = [
    "results/200_1000_bs_10_50_8_rpmxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_rpmxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_rpmxo_rim_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_rspxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_rspxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_rspxo_rim_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_uxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_uxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_bs_10_50_8_uxo_rim_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rpmxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rpmxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rpmxo_rim_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rspxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rspxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_rspxo_rim_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_uxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_uxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_fps_10_50_8_uxo_rim_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rpmxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rpmxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rpmxo_rim_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rspxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rspxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_rspxo_rim_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_uxo_rrm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_uxo_rsm_1_10_30_10/*.csv",
    "results/200_1000_ts_10_50_8_uxo_rim_1_10_30_10/*.csv",
]


def expand_function_name(name: str) -> str:
    if name == "ts":
        return "tournament_selection"
    elif name == "fps":
        return "fitness_proportionate_selection"
    elif name == "bs":
        return "boltzmann_selection"
    elif name == "bspxo":
        return "block_single_point_xo"
    elif name == "rspxo":
        return "row_single_point_xo"
    elif name == "rpmxo":
        return "row_partially_mapped_xo"
    elif name == "uxo":
        return "row_uniform_xo"
    elif name == "bsm":
        return "block_swap_mutation"
    elif name == "rsm":
        return "row_swap_mutation"
    elif name == "rrm":
        return "row_random_mutation"
    elif name == "rim":
        return "row_inversion_mutation"
    else:
        return "ERROR"


def combination_results() -> pd.DataFrame:
    # List to hold data from each file
    df_main = pd.DataFrame()

    for csv_folder in csv_folders_path:
        df_folder = pd.DataFrame()
        for file in glob.glob(csv_folder):
            df_file = pd.read_csv(file)

            parts = file.split("_")
            crossover_method = parts[6]
            selection_method = parts[2]
            mutation_method = parts[7]

            final_generation = df_file["Generation"].iloc[-1]

            df_folder = pd.concat(
                [
                    df_folder,
                    pd.DataFrame(
                        {
                            "crossover": expand_function_name(crossover_method),
                            "selection": expand_function_name(selection_method),
                            "mutation": expand_function_name(mutation_method),
                            "generations": final_generation,
                            "solved": final_generation < 1000,
                        },
                        index=[0],
                    ),
                ],
            )

        df_main = pd.concat([df_main, df_folder])

    grouped_df = (
        df_main.groupby(["selection", "crossover", "mutation"])
        .agg(
            generations_mean=("generations", "mean"),  # Mean of generations
            solved_count=(
                "solved",
                lambda x: x.sum(),
            ),  # Count of True values in solved
        )
        .reset_index()
        .sort_values(["solved_count", "generations_mean"], ascending=False)
    )

    grouped_df.columns = [
        "Selection",
        "Crossover",
        "Mutation",
        "Average Generations",
        "Solved Puzzles",
    ]

    return grouped_df


def specific_results(operation: str):
    if operation not in ["Crossover", "Selection", "Mutation"]:
        raise ValueError(
            "Invalid operation, please use 'Crossover', 'Selection' or 'Mutation'"
        )
    return (
        combination_results()
        .groupby("Crossover")
        .agg(overall_average_generations=("Average Generations", "mean"))
        .reset_index()
    )


print(combination_results().to_markdown(index=False))
