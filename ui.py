import tkinter
import tkinter.ttk

import algorithm
import problem

configure = route_color, city_color, best_route_color = ('red', 'blue', 'green')
canvas_size = (canvas_width, canvas_height) = (600, 480)
window_size = (window_width, window_height) = (640, 620)
landscape = problem.Landscape(map_width=10, map_cities=20)
optimizer = algorithm.SimulatedAnnealingOptimizer()
optimizer.load_problem(landscape)
solution, solution_trace = optimizer.run(temperature=50, iterations=100)
current_index = 0

message_terminate = False
status_text = None
visit_order_label = None


def canvas_update(canvas, width, height, solution):
    # canvas = tkinter.Canvas(main_frame)
    trace = ''
    for node in solution.sequence:
        trace += str(node) + '->'
    trace += str(solution.sequence[0])
    visit_order_label['text'] = trace
    status_text['text'] = 'Initial cost = ' + str(solution_trace[0].evaluate(landscape)) + ', Current cost = ' + str(
        solution.evaluate(landscape))
    canvas.delete('all')
    scale_x = int(width / (landscape.map_width + 1))
    scale_y = int(height / (landscape.map_width + 1))

    paddx = paddy = 10

    canvas.create_rectangle(0, 0, width, height, fill='white')

    for i in range(0, width, scale_x):
        for j in range(0, height, scale_y):
            canvas.create_rectangle(i + paddx, j + paddy, i + scale_x - paddx, j + scale_y - paddy, fill='lightgray')

    def draw_a_city(pos, label):
        fixed_pos_x = scale_x * pos[0] + scale_x
        fixed_pos_y = scale_y * pos[1] + scale_y
        canvas.create_oval(fixed_pos_x - paddx, fixed_pos_y - paddy, fixed_pos_x + paddx, fixed_pos_y + paddy,
                           fill=city_color)
        canvas.create_text(fixed_pos_x, fixed_pos_y, text=label, fill='white')

    def draw_a_route(pos_a, pos_b, best_solution=False):

        start_x = scale_x + pos_a[0] * scale_x
        start_y = scale_y + pos_a[1] * scale_y

        stop_x = scale_x + pos_b[0] * scale_x
        stop_y = scale_y + pos_b[1] * scale_y

        if not best_solution:
            canvas.create_line(start_x, start_y, start_x, stop_y, fill=route_color, width=3, arrow=tkinter.LAST)
            canvas.create_line(start_x, stop_y, stop_x, stop_y, fill=route_color, width=3, arrow=tkinter.LAST)
        else:
            canvas.create_line(start_x, start_y, start_x, stop_y, fill=best_route_color, width=3, arrow=tkinter.LAST)
            canvas.create_line(start_x, stop_y, stop_x, stop_y, fill=best_route_color, width=3, arrow=tkinter.LAST)

    # draw_a_route((0, 0), (landscape.map_width - 1, landscape.map_width - 1))

    for i in range(1, landscape.map_cities):
        draw_a_route(landscape.pos_of_city[solution.sequence[i - 1]], landscape.pos_of_city[solution.sequence[i]])
    draw_a_route(landscape.pos_of_city[solution.sequence[landscape.map_cities - 1]],
                 landscape.pos_of_city[solution.sequence[0]])

    for i in range(landscape.map_cities):
        draw_a_city(landscape.pos_of_city[i], str(i))


def auto_next_solution():
    global current_index, solution_trace, solution, message_terminate
    if current_index >= len(solution_trace): return
    solution = solution_trace[current_index]
    canvas_update(canvas, canvas_width, canvas_height, solution)
    current_index += 1
    if current_index < len(solution_trace) and not message_terminate:
        main_frame.after(500, lambda: auto_next_solution())
    if message_terminate:
        message_terminate = False
    progress['value'] = current_index


def auto_play():
    global current_index, message_terminate
    message_terminate = False
    current_index = 0
    auto_next_solution()


def reset_solution():
    global solution, solution_trace, landscape, optimizer, current_index

    def RepresentsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    text_input_width = input_width.get()
    text_input_cities = input_cities.get()

    if not RepresentsInt(text_input_width):
        status_text['text'] = 'ERROR: INPUT WIDTH MUST BE A INTEGER '
        return
    if not RepresentsInt(text_input_cities):
        status_text['text'] = 'ERROR: NUMBER OF CITIES MUST BE A INTEGER '
        return

    map_width = int(input_width.get())
    map_cities = int(input_cities.get())

    if map_width * map_width <= map_cities:
        status_text['text'] = 'ERROR: CITIES SHOULD BE LESS THAN WIDTH*WIDTH'
        return

    if map_cities > 25:
        status_text['text'] = 'ERROR: CITIES ARE TOO MANY (BETTER <= 25) FOR UI'
        return

    landscape = problem.Landscape(map_width=map_width, map_cities=map_cities)
    optimizer.load_problem(landscape)
    solution, solution_trace = optimizer.run(temperature=20, iterations=1000)
    current_index = 0
    canvas_update(canvas, canvas_width, canvas_height, solution_trace[0])


def stop_autoplay():
    global message_terminate
    message_terminate = True


# compared with global
main_frame = tkinter.Tk()
main_frame.title('TSP Simulator ver 1.02')
main_frame.geometry('%dx%d+0+0' % (window_size))

toolbox_bar = tkinter.Frame(main_frame, width=canvas_width)
toolbox_bar.grid(row=0, column=0, pady=10, sticky=tkinter.W)

configure_bar = tkinter.Frame(toolbox_bar)
configure_bar.grid(row=0, column=0, padx=10)

label_input_width = tkinter.Label(configure_bar, text='Map Width:')
label_input_width.grid(row=0, column=0)

input_width = tkinter.Entry(configure_bar, width=5)
input_width.grid(row=0, column=1)

label_input_cities = tkinter.Label(configure_bar, text='Cities:')
label_input_cities.grid(row=0, column=2, padx=5)

input_cities = tkinter.Entry(configure_bar, width=5)
input_cities.grid(row=0, column=3)

input_width.insert(0, '10')
input_cities.insert(0, '20')

reset_btn = tkinter.Button(configure_bar, text='Reset', command=lambda: reset_solution())
reset_btn.grid(row=0, column=4, padx=10)

demonstrate_bar = tkinter.Frame(toolbox_bar)
demonstrate_bar.grid(row=0, column=1, padx=15)

label_bar = tkinter.Frame(main_frame)
label_bar.grid(row=2, column=0)

status_text = tkinter.Label(label_bar, text='ready', justify=tkinter.LEFT)
status_text.grid(row=0)

visit_order_label = tkinter.Label(label_bar, justify=tkinter.LEFT)
visit_order_label.grid(row=1)

progress = tkinter.ttk.Progressbar(demonstrate_bar, length=200)
progress['maximum'] = 100
progress.grid()

next_btn = tkinter.Button(demonstrate_bar, text='Autoplay', command=lambda: auto_play())
next_btn.grid(row=0, column=1, padx=10)

stop_btn = tkinter.Button(demonstrate_bar, text='Stop', command=lambda: stop_autoplay())
stop_btn.grid(row=0, column=2, padx=5)

canvas = tkinter.Canvas(main_frame, width=canvas_width, height=canvas_height)
canvas.grid(row=1, pady=10)
canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill='white')
canvas_update(canvas, canvas_width, canvas_height, solution_trace[0])
main_frame.mainloop()
