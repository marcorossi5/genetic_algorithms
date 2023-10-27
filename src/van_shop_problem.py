"""Solution to van-shop problem with genetic algorithms.

The van space can be chosen specifying a value in the [1; 5] range

Usage:

```bash
python solutions.py <van_space>
```
"""
import argparse

import matplotlib.pyplot as plt
import pandas as pd
import pygad
import yaml

#######################
# parse arguments
#######################

parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("van_volume", type=float, help="the van free space volume.")
VAN_VOLUME = parser.parse_args().van_volume
assert (
    1 <= VAN_VOLUME <= 5
), f"The van free space value should be in the [1;5] range, got {VAN_VOLUME}"


#######################
# load config
#######################

with open("./src/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

#######################
# load data
#######################


def read_xlsx(xlsx_path: str):
    return pd.read_excel(xlsx_path)


df = read_xlsx(config["data_path"])

num_products = int(df["Quantity"].sum())

# unroll df to show all possible products in the shop
new_idx = df.index.repeat(df["Quantity"])
df_unrolled = df.loc[new_idx].drop(columns="Quantity")

# value array of shape=(num products,)
values = df_unrolled["Price"].values
# space array of shape=(num products,)
spaces = df_unrolled["Space"].values


def fitness_func(ga_instance, solution, solution_idx):
    """Fitness function"""
    if (space := (solution * spaces).sum()) > VAN_VOLUME:
        return -space
    return (solution * values).sum()


ga = pygad.GA(
    num_genes=num_products,
    num_generations=config["num_generations"],
    num_parents_mating=config["num_parents_mating"],
    fitness_func=fitness_func,
    sol_per_pop=config["sol_per_pop"],
    gene_space=config["gene_space"],
    init_range_low=config["init_range_low"],
    init_range_high=config["init_range_high"],
    parent_selection_type=config["parent_selection_type"],
    keep_parents=config["keep_parents"],
    crossover_type=config["crossover_type"],
    mutation_type=config["mutation_type"],
    mutation_percent_genes=config["mutation_percent_genes"],
)

ga.run()


def plot_fitness(ga, output_path):
    """Plots a fitness value vs generation diagram."""
    plt.figure(figsize=[6.4, 4.8])
    ax = plt.subplot()
    ax.plot(range(ga.generations_completed + 1), ga.best_solutions_fitness, lw=1)
    ax.set_title(
        f"Van shop problem (van volume: {VAN_VOLUME})\ngenetic algorithm optimization"
    )
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Saved fitness vs generation figura at {output_path}")
    plt.close()


plot_fitness(ga, config["output_img"])

solution, solution_fitness, solution_idx = ga.best_solution()

df_best_solution = (
    df_unrolled[solution.astype(bool)]
    .value_counts(subset="Product")
    .reset_index()
    .rename(columns={"count": "Picked"})
)

df_best_solution = df_best_solution.merge(df, how="left", on="Product")

# order cols for better display
cols = ["Product", "Space", "Price", "Picked", "Quantity"]
df_best_solution = df_best_solution[cols]

print(f"Predicted output based on the best solution:")
print(df_best_solution)

print(f"Solution fitness:\n{df_best_solution.drop(columns='Product').sum(axis=0)}")
