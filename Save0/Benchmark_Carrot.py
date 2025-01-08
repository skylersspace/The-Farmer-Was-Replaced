from Carrot import *

def benchmark_carrot_normal(goal):
	#NORMAL CARROTS
	quick_print("")
	quick_print("Normal Carrots")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	plant_carrot_all()
	while (num_items(Items.Carrot) < (start_num + goal)):
		carrot_all()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Carrot) - start_num

	quick_print("Items Produced:", items_produced)
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Items per second:", (items_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Operations per item:", (ops_used / items_produced))

def benchmark_carrot_wait(goal):
	#WAITING CARROTS
	quick_print("")
	quick_print("Waiting Carrots")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	plant_carrot_all()
	while (num_items(Items.Carrot) < (start_num + goal)):
		carrot_all_wait()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Carrot) - start_num

	quick_print("Items Produced:", items_produced)
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Items per second:", (items_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Operations per item:", (ops_used / items_produced))

def benchmark_carrot_water(goal):
	#WATERING CARROTS
	quick_print("")
	quick_print("Watering Carrots")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	water_all()
	plant_carrot_all()
	while (num_items(Items.Carrot) < (start_num + goal)):
		carrot_all_water()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Carrot) - start_num

	quick_print("Items Produced:", items_produced)
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Items per second:", (items_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Operations per item:", (ops_used / items_produced))

def carrot_benchmark(benchGoal):
	benchmark_carrot_normal(benchGoal)
	benchmark_carrot_wait(benchGoal)
	benchmark_carrot_water(benchGoal)

clear()
carrot_benchmark(100000)