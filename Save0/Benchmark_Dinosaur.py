from Dinosaur import *

def benchmark_dinosaur(goal):
	#NORMAL DINOSAUR
	quick_print("")
	quick_print("Normal Dinosaur")
	till_all()
	harvest_all()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_num = num_items(Items.Bone)
	start_ops = get_op_count()
	start_time = get_time()
	
	while (num_items(Items.Bone) < (start_num + goal)):
		dinosaur()
	
	quick_print("Time Elapsed:", (get_time() - start_time))
	quick_print("Operations Used:", (get_op_count() - start_ops))
	quick_print("Items Produced:", (num_items(Items.Bone) - start_num))

def dinosaur_benchmark(benchGoal):
	benchmark_dinosaur(benchGoal)
	
clear()
dinosaur_benchmark(100000)