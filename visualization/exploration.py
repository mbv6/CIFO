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
                            "crossover": crossover_method,
                            "selection": selection_method,
                            "mutation": mutation_method,
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
        .sort_values("generations_mean")
    )

    grouped_df.columns = [
        "Selection",
        "Crossover",
        "Mutation",
        "Average Generations",
        "Solved Puzzles",
    ]

    return grouped_df


def crossover_results():
    return (
        combination_results()
        .groupby("Crossover")
        .agg(overall_average_generations=("Average Generations", "mean"))
        .reset_index()
    )


def selection_results():
    return (
        combination_results()
        .groupby("Selection")
        .agg(overall_average_generations=("Average Generations", "mean"))
        .reset_index()
    )


def mutation_results():
    return (
        combination_results()
        .groupby("Mutation")
        .agg(overall_average_generations=("Average Generations", "mean"))
        .reset_index()
    )


print(crossover_results().to_markdown())
