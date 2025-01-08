from Polyculture import *

def benchmark_polyculture_normal(goal):
    #NORMAL POLYCULTURE
	quick_print("")
	quick_print("Normal Polyculture")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_hay = num_items(Items.Hay)
	start_wood = num_items(Items.Wood)
	start_carrot = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	polyculture_normal(goal)
	
	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	hay_produced = num_items(Items.Hay) - start_hay
	wood_produced = num_items(Items.Wood) - start_wood
	carrot_produced = num_items(Items.Carrot) - start_carrot
	total_produced = hay_produced + wood_produced + carrot_produced

	quick_print("Total Produced:", total_produced)
	quick_print("     Hay Produced:", hay_produced, "Percentage: ", ((hay_produced / total_produced) * 100))
	quick_print("     Wood Produced:", wood_produced, "Percentage: ", ((wood_produced / total_produced) * 100))
	quick_print("     Carrots Produced:", carrot_produced, "Percentage: ", ((carrot_produced / total_produced) * 100))
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Average items per second (total):", (total_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Avcerage operations per item (total):", (ops_used / total_produced))
      
def benchmark_polyculture_watered(goal):
    #WATERED POLYCULTURE
	quick_print("")
	quick_print("Watered Polyculture")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_hay = num_items(Items.Hay)
	start_wood = num_items(Items.Wood)
	start_carrot = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	polyculture_watered(goal)

	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	hay_produced = num_items(Items.Hay) - start_hay
	wood_produced = num_items(Items.Wood) - start_wood
	carrot_produced = num_items(Items.Carrot) - start_carrot
	total_produced = hay_produced + wood_produced + carrot_produced
	
	quick_print("Total Produced:", total_produced)
	quick_print("     Hay Produced:", hay_produced, "Percentage: ", ((hay_produced / total_produced) * 100))
	quick_print("     Wood Produced:", wood_produced, "Percentage: ", ((wood_produced / total_produced) * 100))
	quick_print("     Carrots Produced:", carrot_produced, "Percentage: ", ((carrot_produced / total_produced) * 100))
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Average items per second (total):", (total_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Avcerage operations per item (total):", (ops_used / total_produced))
	
def benchmark_polyculture_fertilized(goal):
    #FERTILIZED POLYCULTURE
	quick_print("")
	quick_print("Fertilized Polyculture")
	clear_tilled()
	reset()
	quick_print("Starting Water:", get_water())
	
	start_hay = num_items(Items.Hay)
	start_wood = num_items(Items.Wood)
	start_carrot = num_items(Items.Carrot)
	start_ops = get_op_count()
	start_time = get_time()
	
	polyculture_fertilized(goal)

	ops_used = get_op_count() - start_ops
	time_elapsed = get_time() - start_time
	hay_produced = num_items(Items.Hay) - start_hay
	wood_produced = num_items(Items.Wood) - start_wood
	carrot_produced = num_items(Items.Carrot) - start_carrot
	total_produced = hay_produced + wood_produced + carrot_produced
	
	quick_print("Total Produced:", total_produced)
	quick_print("     Hay Produced:", hay_produced, "Percentage: ", ((hay_produced / total_produced) * 100))
	quick_print("     Wood Produced:", wood_produced, "Percentage: ", ((wood_produced / total_produced) * 100))
	quick_print("     Carrots Produced:", carrot_produced, "Percentage: ", ((carrot_produced / total_produced) * 100))
	quick_print("Time Elapsed:", time_elapsed)
	quick_print("     Average items per second (total):", (total_produced / time_elapsed))
	quick_print("Operations Used:", ops_used)
	quick_print("     Avcerage operations per item (total):", (ops_used / total_produced))
	
def polyculture_benchmark(benchGoal):
	#None of these benchmarks account for the materials (Hay/Wood) spend to purchase carrot seeds
    benchmark_polyculture_normal(benchGoal)
    benchmark_polyculture_watered(benchGoal)
    benchmark_polyculture_fertilized(benchGoal)

clear()
polyculture_benchmark(100000)