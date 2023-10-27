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
import numpy as np
import pandas as pd
import pygad
import yaml

MIN_VAN_VOLUME = 1
MAX_VAN_VOLUME = 5


def load_config() -> Dict:
    """Load configuration from file."""
    with open("./src/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def read_xlsx(xlsx_path: str):
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
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Saved fitness vs generation figura at {output_path}")
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

    # order cols for better display
    cols = ["Product", "Space", "Price", "Picked", "Quantity"]
    df_best_solution = df_best_solution[cols]

    print(f"Predicted output based on the best solution:")
    print(df_best_solution)

    print(f"Solution fitness:\n{df_best_solution.drop(columns='Product').sum(axis=0)}")


def render_results(ga: pygad.GA, config_dict: Dict, data_dict: Dict):
    plot_fitness(ga, config_dict["output_img"], config_dict["van_volume"])

    print_best_results(ga, data_dict)


def main(van_volume: float):
    # load config
    config = load_config()

    # update user defined settings
    config["van_volume"] = van_volume

    # load data
    data_dict = load_data(config)

    # define fitness function
    fitness_func = define_fitness_function(data_dict, config)

    # genetic algorithm instance
    ga = pygad.GA(
        num_genes=data_dict["num_genes"],
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

    # run algorithm
    ga.run()

    # plot results
    render_results(ga, config, data_dict)


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
