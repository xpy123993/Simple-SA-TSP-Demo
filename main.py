import algorithm
import problem


def test_case(map_width, map_cities):
    landscape = problem.Landscape(map_width=map_width, map_cities=map_cities)
    optimizer = algorithm.SimulatedAnnealingOptimizer()

    optimizer.load_problem(landscape)
    best_solution, solution_trace = optimizer.run(temperature=50, iterations=1000)

    print('Landscape data (Map size: %dx%d, # of cities: %d)' %
          (landscape.map_width, landscape.map_width, landscape.map_cities))
    print('TSP Map (0 for empty, 1 for nodes need to pass)')
    print(landscape.map_data)

    print('Distance Matrix')
    print(landscape.map_distance_matrix)

    print('Solution')
    start_point = best_solution.sequence[0]
    trace = ''
    for node in best_solution.sequence:
        trace += str(node) + '->'
    trace += str(start_point)
    print(trace)
    print('Solution cost = %d' % best_solution.evaluate(landscape))


if __name__ == '__main__':
    map_cities = int(input('Input # of cities:'))
    map_width = map_cities
    test_case(map_width=map_width, map_cities=map_cities)
