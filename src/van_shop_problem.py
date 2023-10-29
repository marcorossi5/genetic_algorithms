"""Solution to van-shop problem with genetic algorithms.

The van space can be chosen specifying a value in the [1; 5] range

Usage:

```bash
python solutions.py <van_space>
```
"""
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


def load_data(config: Dict) -> pd.DataFrame:
    """Loads data, saving results in a dictionary."""
    df = read_xlsx(config["data_path"])
    return df

    num_products = len(df)

    prices = df["Price"].values
    spaces = df["Space"].values

    data_dict = {
        "data": df,
        "num_genes": num_products,
        "prices_arr": prices,
        "spaces_arr": spaces,
    }
    return data_dict


def define_fitness_function(df: pd.DataFrame, config_dict: Dict) -> Callable:
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
        if (space := (solution * df["Space"].values).sum()) > config_dict["van_volume"]:
            return -space
        return (solution * df["Price"].values).sum()

    return fitness_func


def run_genetic_algorithm(config_dict: Dict, df: pd.DataFrame) -> pygad.GA:
    # define fitness function
    fitness_func = define_fitness_function(df, config_dict)

    # genetic algorithm instance
    ga = pygad.GA(
        num_genes=len(df),
        num_generations=config_dict["num_generations"],
        num_parents_mating=config_dict["num_parents_mating"],
        fitness_func=fitness_func,
        sol_per_pop=config_dict["sol_per_pop"],
        gene_space=[range(q) for q in df["Quantity"].values],
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


def print_best_results(ga: pygad.GA, df: Dict):
    """Print best results to stdout."""

    solution = ga.best_solution()[0]

    df["Picked"] = solution.astype(int)

    total_space = (df["Space"] * df["Picked"]).sum()
    total_price = (df["Price"] * df["Picked"]).sum()

    print("Best solution:")
    print(f"Predicted solution occupied space: {total_space:.3f}")
    print(f"Predicted total value: {total_price:.3f}")

    print(f"Predicted output based on the best solution:")
    print(df[["Product", "Picked"]])


def render_results(ga: pygad.GA, config_dict: Dict, df: Dict):
    plot_fitness(ga, config_dict["output_img"], config_dict["van_volume"])
    print_best_results(ga, df)


def main():
    # load config
    config_dict = load_config()

    assert (
        MIN_VAN_VOLUME <= config_dict["van_volume"] <= MAX_VAN_VOLUME
    ), f"The van free space value should be in the [{MIN_VAN_VOLUME};{MAX_VAN_VOLUME}] range, got {config_dict['van_volume']}"

    # load data
    df = load_data(config_dict)

    # run genetic algorithm
    ga = run_genetic_algorithm(config_dict, df)

    # plot results
    render_results(ga, config_dict, df)


if __name__ == "__main__":
    main()
