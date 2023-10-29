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

The following code block shows an example output of the program (the van volume
is set by default at 3.5):

```bash
(gad) $ ./start.sh
Saved fitness vs generation figure at ./assets/fitness_vs_generation.png
Best solution:
Predicted solution occupied space: 3.500
Predicted total value: 53466.480
Predicted output based on the best solution:
           Product  Picked
0   Refrigerator A       0
1       Cell phone       1
2            TV 55       3
3            TV 50       4
4            TV 42       4
5       Notebook A       3
6       Ventilator       0
7      Microwave A       4
8      Microwave B       0
9      Microwave C       5
10  Refrigerator B       0
11  Refrigerator C       0
12      Notebook B       0
13      Notebook C       0
```

Additionally, the program saves a plot describing how the best fitness changes
with the different generations of the genetic algorithm, like the one below

![fitness vs generation plot](./assets/fitness_vs_generation.png)

## Experiment with different hyperparameters

The model's hyperparameters can be tuned modifying the values in the `src/settings.yaml`
configuration file.

:warning: The settings file contains a seed value to ensure experiments
reproducibility. Set it to `null` to allow output randomness.

Feel free to experiment around by changing the values of the algorithm.
