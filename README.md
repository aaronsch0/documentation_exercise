# Heat Equation Solver

I acknowledge the use of Gemini 3 Pro to implement the entirety of this code.  Unfortunately, the RAI website (https://rai.uni-stuttgart.de/) is not working. 

Prompt: 
1. Please write Python code to solve a heat equation. all the parameters should be taken in from a configuration file and the results written in an output file. The code should be commented as good as possible according to Python style guide. Every class, method, etc. needs a proper docstring, I also need a ReadME.md and I would like every function or method tested in an automatized test file

This project implements a 1D Heat Equation solver using the Finite Difference Method (Forward Time Centered Space - FTCS) in Python.

## Project Structure

- `heat_equation.py`: The main script containing the `HeatEquationSolver` class.
- `config.json`: Configuration file for simulation parameters.
- `test_heat_equation.py`: Unit tests for the solver.
- `README.md`: This documentation file.

## Requirements

- Python 3.6 or higher.
- No external libraries are required (uses standard `json`, `csv`, `unittest`, `os`).

## Configuration

The simulation parameters are defined in `config.json`. You can modify this file to change the simulation settings:

```json
{
    "length": 1.0,          // Length of the 1D domain
    "total_time": 0.1,      // Total simulation time
    "alpha": 0.01,          // Thermal diffusivity
    "num_points_x": 50,     // Number of spatial grid points
    "num_points_t": 1000,   // Number of time steps
    "output_file": "results.csv" // Output file name
}
```

## Usage

To run the simulation:

1.  Ensure `config.json` is present in the same directory (or provide the path).
2.  Run the script:

```bash
python heat_equation.py
```

The results will be saved to the file specified in `output_file` (default: `results.csv`).

## Output

The output is a CSV file where:
- The first row contains the spatial coordinates ($x_0, x_1, ...$).
- Each subsequent row corresponds to a time step.
- Values represent the temperature $u(x, t)$.

## Testing

To run the automated unit tests:

```bash
python -m unittest test_heat_equation.py
```

or simply:

```bash
python test_heat_equation.py
```

## License

This project is for educational purposes.
