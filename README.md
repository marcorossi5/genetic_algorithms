# Van-shop problem with genetic algorithms

For an introduction to genetic algorithms and related resources follow
[this link](https://github.com/Ishikawa7/Quick-paths-to-start/tree/main/Genetic%20algorithms).

## The problem

A van in a shop must be filled to transport household appliances, its load must
be optimized by maximizing the value of what is transported for a given volume.

## Data

Find the inventory of available products along wth their specifics at
[this file](./data/products.xlsx).

## Install

Download the code cloning the present repository and install its dependencies
in a fresh new python environment.

Follow the commands below to create a new virtual environment using venv.

```bash
git clone https://github.com/marcorossi5/genetic_algorithms.git
cd genetic_algorithms
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements
```

## Run the code

The code to solve the given problem can be run with the following command:

```bash
./start.sh <van_space>
```

where `van_space` is the space availble in the van.  
The allowed values for this parameter are the range `[1,5]`.

The program shows as output the list of products and their picked quantity to be
loaded on the van to maximize the transported value.

Additionally, the program saves a plot describing how the best fitness changes
with the different generations of the genetic algorithm, like the one below

![fitness vs generation plot](./assets/fitness_vs_generation.png)

## Experiment with different hyperparameters

The model's hyperparameters can be tuned modifying the values in the `src/settings.yaml`
configuration file.

Feel free to experiment around by changing the values of the algorithm.
