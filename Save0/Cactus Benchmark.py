def benchmark_cactus_bubble(goal):
	#BUBBLE CACTUS
	quick_print("")
	quick_print("Bubble Cactus")
	till_all()
	harvest_all()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Cactus)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Cactus) < (start_num + goal)):
		cactus_bubble()
	
	quick_print("Time Elapsed:", (get_time() - start_time))
	quick_print("Operations Used:", (get_op_count() - start_ops))
	quick_print("Items Produced:", (num_items(Items.Cactus) - start_num))
	
def cactus_benchmark(benchGoal):
	benchmark_cactus_bubble(benchGoal)
	
clear()
cactus_benchmark(100000)