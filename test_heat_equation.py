import unittest
import json
import os
from heat_equation import HeatEquationSolver

class TestHeatEquationSolver(unittest.TestCase):
    """
    Unit tests for the HeatEquationSolver class.
    """

    def setUp(self):
        """
        Set up test fixtures. Creates a temporary config file.
        """
        self.test_config_filename = "test_config.json"
        self.test_output_filename = "test_output.csv"
        self.config_data = {
            "length": 1.0,
            "total_time": 0.01,
            "alpha": 0.01,
            "num_points_x": 10,
            "num_points_t": 10,
            "output_file": self.test_output_filename
        }
        with open(self.test_config_filename, 'w') as f:
            json.dump(self.config_data, f)

    def tearDown(self):
        """
        Clean up test fixtures. Removes temporary files.
        """
        if os.path.exists(self.test_config_filename):
            os.remove(self.test_config_filename)
        if os.path.exists(self.test_output_filename):
            os.remove(self.test_output_filename)

    def test_load_config(self):
        """
        Test that configuration is loaded correctly.
        """
        solver = HeatEquationSolver(self.test_config_filename)
        self.assertEqual(solver.config, self.config_data)

    def test_load_config_file_not_found(self):
        """
        Test that FileNotFoundError is raised for missing config file.
        """
        with self.assertRaises(FileNotFoundError):
            HeatEquationSolver("non_existent_config.json")

    def test_initialize_grid(self):
        """
        Test that the grid is initialized correctly.
        """
        solver = HeatEquationSolver(self.test_config_filename)
        self.assertEqual(len(solver.u), self.config_data['num_points_x'])
        # Check initial condition (spike in the middle)
        mid_point = self.config_data['num_points_x'] // 2
        self.assertEqual(solver.u[mid_point], 1.0)
        self.assertEqual(solver.u[0], 0.0)

    def test_solve_runs(self):
        """
        Test that the solve method runs and returns results of expected shape.
        """
        solver = HeatEquationSolver(self.test_config_filename)
        results = solver.solve()
        # Expected number of time steps + initial state
        expected_steps = self.config_data['num_points_t'] + 1
        self.assertEqual(len(results), expected_steps)
        self.assertEqual(len(results[0]), self.config_data['num_points_x'])

    def test_save_results(self):
        """
        Test that results are saved to a file.
        """
        solver = HeatEquationSolver(self.test_config_filename)
        results = solver.solve()
        solver.save_results(results)
        self.assertTrue(os.path.exists(self.test_output_filename))
        
        # Verify content roughly
        with open(self.test_output_filename, 'r') as f:
            lines = f.readlines()
            # Header + (num_points_t + 1) lines of data
            self.assertEqual(len(lines), self.config_data['num_points_t'] + 2)

if __name__ == '__main__':
    unittest.main()
