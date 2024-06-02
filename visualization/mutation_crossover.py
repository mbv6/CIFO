import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

csv_files_path = [
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

data_list = []

for csv_file in csv_files_path:
    for file in glob.glob(csv_file):
        df = pd.read_csv(file)

        parts = file.split("_")
        crossover_method = parts[6]
        selection_method = parts[2]
        mutation_method = parts[7]

        final_generation = df["Generation"].iloc[-1]

        data_list.append(
            {
                "crossover": crossover_method,
                "selection": selection_method,
                "mutation": mutation_method,
                "generations": final_generation,
            }
        )

df = pd.DataFrame(data_list)

plt.figure(figsize=(16, 8))

# Boxplot to show the distribution of generations for each combination
sns.boxplot(x="mutation", y="generations", hue="crossover", data=df)

plt.title("Performance of Genetic Algorithm Configurations")
plt.xlabel("Mutation Method")
plt.ylabel("Number of Generations to Reach Solution")
plt.legend(title="Crossover Method")
plt.show()
