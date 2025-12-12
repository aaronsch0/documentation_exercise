import json
import csv
import os
from typing import List, Dict, Any

class HeatEquationSolver:
    """
    A class to solve the 1D heat equation using the Finite Difference Method.

    The equation solved is: du/dt = alpha * d^2u/dx^2

    Attributes:
        config (Dict[str, Any]): Configuration parameters.
        u (List[float]): The temperature distribution at the current time step.
        dx (float): Spatial step size.
        dt (float): Time step size.
    """

    def __init__(self, config_path: str):
        """
        Initializes the solver by loading configuration from a file.

        Args:
            config_path (str): Path to the JSON configuration file.
        """
        self.config = self._load_config(config_path)
        self.u: List[float] = []
        self.dx: float = 0.0
        self.dt: float = 0.0
        self._initialize_grid()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Loads configuration parameters from a JSON file.

        Args:
            config_path (str): Path to the JSON configuration file.

        Returns:
            Dict[str, Any]: A dictionary containing configuration parameters.

        Raises:
            FileNotFoundError: If the config file does not exist.
            json.JSONDecodeError: If the config file is not valid JSON.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)

    def _initialize_grid(self):
        """
        Initializes the spatial grid and initial conditions.
        
        Calculates dx and dt based on configuration.
        Sets the initial temperature distribution (e.g., a sine wave or step function).
        Here we use a simple initial condition: u(x, 0) = 0 everywhere, 
        except boundary conditions if specified, or maybe a peak in the middle.
        For this example, let's assume u(x,0) = sin(pi*x/L).
        """
        length = self.config['length']
        nx = self.config['num_points_x']
        total_time = self.config['total_time']
        nt = self.config['num_points_t']

        self.dx = length / (nx - 1)
        self.dt = total_time / nt
        
        # Initialize u with 0.0
        self.u = [0.0] * nx
        
        # Set a simple initial condition: a spike in the middle
        # This is just for demonstration purposes.
        mid_point = nx // 2
        self.u[mid_point] = 1.0

    def solve(self) -> List[List[float]]:
        """
        Solves the heat equation over the specified time steps.

        Uses the Forward Time Centered Space (FTCS) scheme.

        Returns:
            List[List[float]]: A list of temperature distributions at each time step (or selected steps).
        """
        alpha = self.config['alpha']
        nx = self.config['num_points_x']
        nt = self.config['num_points_t']
        
        r = alpha * self.dt / (self.dx ** 2)
        
        # Check stability condition for explicit method
        if r > 0.5:
            print(f"Warning: Stability condition violated (r={r:.4f} > 0.5). The solution may be unstable.")

        results = [self.u[:]] # Store initial state

        for _ in range(nt):
            u_new = self.u[:]
            for i in range(1, nx - 1):
                u_new[i] = self.u[i] + r * (self.u[i+1] - 2*self.u[i] + self.u[i-1])
            
            # Boundary conditions (Dirichlet u=0 at ends) are implicitly handled 
            # by not updating indices 0 and nx-1 (they remain 0.0)
            
            self.u = u_new
            results.append(self.u[:])
            
        return results

    def save_results(self, results: List[List[float]]):
        """
        Saves the simulation results to a CSV file.

        Args:
            results (List[List[float]]): The history of temperature distributions.
        """
        output_file = self.config.get('output_file', 'output.csv')
        
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([f"x_{i}" for i in range(self.config['num_points_x'])])
                writer.writerows(results)
            print(f"Results successfully saved to {output_file}")
        except IOError as e:
            print(f"Error writing to file {output_file}: {e}")

if __name__ == "__main__":
    # Example usage
    try:
        solver = HeatEquationSolver("config.json")
        results = solver.solve()
        solver.save_results(results)
    except Exception as e:
        print(f"An error occurred: {e}")
