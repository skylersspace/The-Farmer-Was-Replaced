from Utility import *

def benchmark_map(bench_goal):
	#WATERED PUMPKINS MAPPED
	quick_print("")
	quick_print("Normal Map")
	clear_tilled()
	reset()
	flowers_plant()
	
	start_ops = get_op_count()
	start_time = get_time()
	
	for i in range(bench_goal):
		temp = map()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = bench_goal

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Tiles Mapped:", bench_goal * (get_world_size() * get_world_size()))
	quick_print("Seconds per map:", time_elapsed / bench_goal)
	quick_print("Operations per map:", ops_used / bench_goal)
	
	flowers_harvest_v2()
	
def benchmark_map_v2(bench_goal):
	#WATERED PUMPKINS MAPPED
	quick_print("")
	quick_print("Wide Map")
	clear_tilled()
	reset()
	flowers_plant()

	start_ops = get_op_count()
	start_time = get_time()
	
	for i in range(bench_goal):
		temp = map_v2()
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	items_produced = bench_goal

	quick_print("Time Elapsed:", time_elapsed)
	quick_print("Operations Used:", ops_used)
	quick_print("Tiles Mapped:", bench_goal * (get_world_size() * get_world_size()))
	quick_print("Seconds per map:", time_elapsed / bench_goal)
	quick_print("Operations per map:", ops_used / bench_goal)
	
	flowers_harvest_v2()

#NOTE: In this case, benchGoal is how many times it will map a given area
def map_benchmark(benchGoal):
	benchmark_map(benchGoal)
	benchmark_map_v2(benchGoal)
	

map_benchmark(100)