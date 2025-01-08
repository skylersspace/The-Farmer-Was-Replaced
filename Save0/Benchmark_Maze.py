from Maze import *

def benchmark_maze_left(goal):
	#NORMAL MAZE - LEFT WALL
	quick_print("")
	quick_print("Left Maze")
	till()
	
	start_num = num_items(Items.Gold)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Gold) < (start_num + goal)):
		lh_maze()
		mazes_completed += 1

	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Gold) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Mazes Solved:", mazes_completed)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def benchmark_maze_right(goal):
	#NORMAL MAZE - RIGHT WALL
	quick_print("")
	quick_print("Right Maze")
	till()
	
	start_num = num_items(Items.Gold)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Gold) < (start_num + goal)):
		rh_maze()
		mazes_completed += 1
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Gold) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Mazes Solved:", mazes_completed)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def maze_benchmark(benchGoal):
	benchmark_maze_left(benchGoal)
	benchmark_maze_right(benchGoal)
	
clear()
maze_benchmark(100000)