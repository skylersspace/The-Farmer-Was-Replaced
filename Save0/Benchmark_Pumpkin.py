from Pumpkin import *

def benchmark_pumpkin(goal):
	#NORMAL PUMPKINS
	quick_print("")
	quick_print("Normal Pumpkins")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_normal()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def benchmark_pumpkin_watered(goal):
	#WATERED PUMPKINS
	quick_print("")
	quick_print("Pumpkins Watered")
	clear_tilled()
	reset()
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_watered()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def benchmark_pumpkin_map(goal):
	#PUMPKINS MAPPED
	quick_print("")
	quick_print("Pumpkins Mapped")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_map()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def benchmark_pumpkin_watered_map(goal):
	#WATERED PUMPKINS MAPPED
	quick_print("")
	quick_print("Pumpkins Watered Mapped")
	clear_tilled()
	reset()
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_map_watered()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def benchmark_pumpkin_fertilized(goal):
	#WATERED PUMPKINS MAPPED
	quick_print("")
	quick_print("Pumpkins Fertilized")
	clear_tilled()
	reset()
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_fertilized()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def benchmark_pumpkin_fertilized_map(goal):
	#WATERED PUMPKINS MAPPED
	quick_print("")
	quick_print("Pumpkins Fertilized Mapped")
	clear_tilled()
	reset()
	
	start_num = num_items(Items.Pumpkin)
	mazes_completed = 0
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Pumpkin) < (start_num + goal)):
		pumpkin_map_fertilized()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Pumpkin) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def pumpkin_benchmark(benchGoal):
	benchmark_pumpkin(benchGoal)
	benchmark_pumpkin_map(benchGoal)
	benchmark_pumpkin_watered(benchGoal)
	benchmark_pumpkin_watered_map(benchGoal)
	benchmark_pumpkin_fertilized(benchGoal)
	benchmark_pumpkin_fertilized_map(benchGoal)
	
clear()
pumpkin_benchmark(100000)