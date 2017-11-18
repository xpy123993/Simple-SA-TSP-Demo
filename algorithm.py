import math
import random

import problem

'''
SimulateAnnealing Optimizer

optimize using simulate annealing

def load_problem(landscape): load a landscape to solve tsp
def run(temperature, iterations): start to solve

more details about temperature in simulate annealing, please visit the following link: 
https://en.wikipedia.org/wiki/Simulated_annealing in chapter 'Acceptance probabilities'

'''


def event_happen(probability): return random.randint(0, 100) < 100 * probability


class SimulateAnnealingOptimizer:
    current_problem = None

    def load_problem(self, target):
        self.current_problem = target

    def run(self, temperature, iterations):

        current_solution = problem.Solution(self.current_problem.map_cities)
        current_solution_value = current_solution.evaluate(self.current_problem)

        best_solution = current_solution
        best_solution_value = current_solution_value

        initial_solution_value = best_solution_value

        current_solution_stacks = []

        for iteration in range(iterations):

            best_neighbor = current_solution.find_better_solution(self.current_problem)
            best_neighbor_value = best_neighbor.evaluate(self.current_problem)
            # if current cost < cost of best neighbor, accept probability will less than 1
            # if bigger differences between two costs, the more unlikely our algorithm accept the solution
            # https://en.wikipedia.org/wiki/Simulated_annealing in chapter 'Acceptance probabilities'
            accept_probability = math.exp((current_solution_value - best_neighbor_value) / temperature)

            if event_happen(accept_probability):
                current_solution = best_neighbor
                current_solution_value = best_neighbor_value
                if best_neighbor_value < best_solution_value:
                    best_solution_value = best_neighbor_value
                    best_solution = best_neighbor

            current_solution_stacks.append(current_solution)

        print('[SAOptimizer] Iteration finished, %g%% improved from %d to %d'
              % (round((100 * (initial_solution_value - best_solution_value) / initial_solution_value), 2),
                 initial_solution_value, best_solution_value))
        return best_solution, current_solution_stacks
