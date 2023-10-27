"""Solution to van-shop problem with genetic algorithms.

The van space can be chosen specifying a value in the [1; 5] range

Usage:

```bash
python solutions.py <van_space>
```
"""
import argparse
from typing import Callable, Dict

import matplotlib.pyplot as plt
import pandas as pd
import pygad
import yaml

MIN_VAN_VOLUME = 1
MAX_VAN_VOLUME = 5


def load_config() -> Dict:
    """Load configuration from file."""
    with open("./src/settings.yaml", "r") as f:
        config_dict = yaml.safe_load(f)
    return config_dict


def read_xlsx(xlsx_path: str) -> pd.DataFrame:
    return pd.read_excel(xlsx_path)


def load_data(config: Dict) -> Dict:
    """Loads data, saving results in a dictionary."""
    df = read_xlsx(config["data_path"])

    num_products = int(df["Quantity"].sum())

    # unroll df to show all possible products in the shop
    new_idx = df.index.repeat(df["Quantity"])
    df_unrolled = df.loc[new_idx].drop(columns="Quantity")

    # value array of shape=(num products,)
    prices = df_unrolled["Price"].values
    # space array of shape=(num products,)
    spaces = df_unrolled["Space"].values

    data_dict = {
        "data": df,
        "unrolled_data": df_unrolled,
        "num_genes": num_products,
        "prices_arr": prices,
        "spaces_arr": spaces,
    }
    return data_dict


def define_fitness_function(data_dict: Dict, config_dict: Dict) -> Callable:
    """Define the fitness function to be called by the genetic algorithm.

    :param data_dict: the dictionary of data dependent settings
    :type data_dict: np.ndarray
    :param config_dict: the configuration settings
    :type config_dict: np.ndarray

    :return: the fitness function
    :rtype: Callable
    """

    def fitness_func(ga_instance, solution, solution_idx):
        """Fitness function"""
        if (space := (solution * data_dict["spaces_arr"]).sum()) > config_dict[
            "van_volume"
        ]:
            return -space
        return (solution * data_dict["prices_arr"]).sum()

    return fitness_func


def run_genetic_algorithm(config_dict: Dict, data_dict: Dict) -> pygad.GA:
    # define fitness function
    fitness_func = define_fitness_function(data_dict, config_dict)

    # genetic algorithm instance
    ga = pygad.GA(
        num_genes=data_dict["num_genes"],
        num_generations=config_dict["num_generations"],
        num_parents_mating=config_dict["num_parents_mating"],
        fitness_func=fitness_func,
        sol_per_pop=config_dict["sol_per_pop"],
        gene_space=config_dict["gene_space"],
        parent_selection_type=config_dict["parent_selection_type"],
        keep_parents=config_dict["keep_parents"],
        crossover_type=config_dict["crossover_type"],
        mutation_type=config_dict["mutation_type"],
        mutation_percent_genes=config_dict["mutation_percent_genes"],
        random_seed=config_dict["random_seed"],
    )

    # run algorithm
    ga.run()

    return ga


def plot_fitness(ga: pygad.GA, output_path: str, van_volume: float):
    """Plots a fitness value vs generation diagram."""
    plt.figure(figsize=[6.4, 4.8])
    ax = plt.subplot()
    ax.plot(range(ga.generations_completed + 1), ga.best_solutions_fitness, lw=1)
    ax.set_title(
        f"Van shop problem (van volume: {van_volume})\ngenetic algorithm optimization"
    )
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.set_yscale("log")
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Saved fitness vs generation figure at {output_path}")
    plt.close()


def print_best_results(ga: pygad.GA, data_dict: Dict):
    """Print best results to stdout."""

    df = data_dict["data"]
    df_unrolled = data_dict["unrolled_data"]

    solution = ga.best_solution()[0]

    df_best_solution = (
        df_unrolled[solution.astype(bool)]
        .value_counts(subset="Product")
        .reset_index()
        .rename(columns={"count": "Picked"})
    )

    df_best_solution = df_best_solution.merge(df, how="left", on="Product")

    total_space = (df_best_solution["Space"] * df_best_solution["Picked"]).sum()
    total_price = (df_best_solution["Price"] * df_best_solution["Picked"]).sum()

    print("Best solution:")
    print(f"Predicted solution occupied space: {total_space:.3f}")
    print(f"Predicted total value: {total_price:.3f}")

    print(f"Predicted output based on the best solution:")
    print(df_best_solution[["Product", "Picked"]])


def render_results(ga: pygad.GA, config_dict: Dict, data_dict: Dict):
    plot_fitness(ga, config_dict["output_img"], config_dict["van_volume"])
    print_best_results(ga, data_dict)


def main(van_volume: float):
    # load config
    config_dict = load_config()

    # update user defined settings
    config_dict["van_volume"] = van_volume

    # load data
    data_dict = load_data(config_dict)

    # run genetic algorithm
    ga = run_genetic_algorithm(config_dict, data_dict)

    # plot results
    render_results(ga, config_dict, data_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("van_volume", type=float, help="the van free space volume.")
    van_volume = parser.parse_args().van_volume
    assert (
        MIN_VAN_VOLUME <= van_volume <= MAX_VAN_VOLUME
    ), f"The van free space value should be in the [{MIN_VAN_VOLUME};{MAX_VAN_VOLUME}] range, got {van_volume}"
    main(van_volume)
