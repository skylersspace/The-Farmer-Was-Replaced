from Cactus import *

def benchmark_cactus_bubble(goal):
	#BUBBLE CACTUS
	quick_print("")
	quick_print("Bubble Cactus")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Cactus)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Cactus) < (start_num + goal)):
		cactus_bubble()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = num_items(Items.Cactus) - start_num

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Items Produced:", items_produced)
	quick_print("Items per second:", (items_produced / time_elapsed))
	quick_print("Operations per item:", (ops_used / items_produced))
	
def cactus_benchmark(benchGoal):
	benchmark_cactus_bubble(benchGoal)
	
clear()
cactus_benchmark(100000)