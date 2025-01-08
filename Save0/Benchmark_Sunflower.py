from Sunflower import *

def benchmark_sunflower_normal(goal):
	#NORMAL SUNFLOWERS
	quick_print("")
	quick_print("Normal Sunflowers")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Power)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Power) < (start_num + goal)):
		flowers_plant()
		flowers_harvest()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Power) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def benchmark_sunflower_watered(goal):
	#WATERED SUNFLOWERS
	quick_print("")
	quick_print("Watered Sunflowers")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Power)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Power) < (start_num + goal)):
		flowers_plant_water()
		flowers_harvest()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Power) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def benchmark_sunflower_v2(goal):
	#WATERED SUNFLOWERS
	quick_print("")
	quick_print("Sunflowers V2")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Power)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Power) < (start_num + goal)):
		flowers_harvest_v2()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Power) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def benchmark_sunflower_v2_watered(goal):
	#WATERED SUNFLOWERS
	quick_print("")
	quick_print("Sunflowers V2 Watered")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Power)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Power) < (start_num + goal)):
		flowers_harvest_v2_watered()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Power) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
#Even when watered, this appeared to be too fast. Use fertilizer?
def benchmark_sunflower_fertilized(goal):
	#WATERED SUNFLOWERS
	quick_print("")
	quick_print("Sunflowers Fertilized")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Power)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Power) < (start_num + goal)):
		flowers_fertilized()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Power) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))

def sunflower_benchmark(benchGoal):
	benchmark_sunflower_normal(benchGoal)
	benchmark_sunflower_v2(benchGoal)
	benchmark_sunflower_watered(benchGoal)
	benchmark_sunflower_v2_watered(benchGoal)
	benchmark_sunflower_fertilized(benchGoal)
	
clear()
sunflower_benchmark(1000)