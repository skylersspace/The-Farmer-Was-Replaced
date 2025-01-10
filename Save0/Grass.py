from Utility import *

def grass(goal, benchmark = False, verbose = False):
	HARVEST_LEVELS = (0, 100, 200, 300, 400,
				  		500, 600, 700, 800, 900,
				 		1000, 1100, 1200, 1300, 1400)
	GROWTH_RATE_GRASS = (0.5, 0.5)
	world_size = get_world_size()
	full_world_size = pow(world_size, 2)
	
	unit_harvest = num_unlocked(Unlocks.Grass)
	full_harvest = unit_harvest * full_world_size

	# Grass is consistent with no variability for full harvests.
	# Harvest amount is determined by upgrades and the world size.

	# Continuous
	def grass_all():
		for i in range (get_world_size()):
			for j in range (get_world_size()):
				if can_harvest():
					harvest()
					plant(Entities.Grass)
				else:
					plant(Entities.Grass)
				move(North)
			move(East)

	#This will leave a full field behind
	def grass_full():
		mark = num_items(Items.Hay) + goal
		while (num_items(Items.Hay) < mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					plant(Entities.Grass)
					move(North)
				move(East)

	def grass_clean():
		mark = num_items(Items.Hay) + goal
		while ((num_items(Items.Hay)) < mark):
			for i in range (get_world_size()):
				if (num_items(Items.Hay) >= mark):
					break
				for j in range (get_world_size()):
					if (num_items(Items.Hay) >= mark):
						break
					if can_harvest():
						harvest()
					plant(Entities.Grass)
					move(North)
				move(East)
		
		harvest_all_v2()
	
	def grass_precise_v2():
		mark = num_items(Items.Hay) + goal

		harvest_map = []

		# --------------
		# PRE - PLANTING
		# --------------
		# Pre-planting removes some variability and complexity from the code
		# Three possible conditions for pre-planting
		#	Full Plant: Either one or more full harvests are required
		#	Partial Plant: Less than one full harvest is required
		#	No plant is not a condition to be acocunted for as this function should not be called if none are required
		
		if ((num_items(Items.Hay) + full_harvest) <= mark):
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					plant(Entities.Grass)
					move(North)
				move(East)

			#--------------
			# HARVESTING 1+
			#--------------

			# 2+ rounds are required.
			# Replace grass as they are harvested until less than a full harvest is required
			while ((num_items(Items.Hay) + (full_harvest * 2)) <= mark):
				for i in range (get_world_size()):
					for j in range (get_world_size()):
						if can_harvest():
							harvest()
						plant(Entities.Grass)
						move(North)
					move(East)

			# Will always run if at least one full harvest is required
			# Replace grass as they are havested until the mark will be reached with what is planted
			# If an even harvest is all that's required, nothing will be planted
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if can_harvest():
						harvest()
					# If more than a full harvest is required, plant
					if ((num_items(Items.Hay) + full_harvest) <= mark):
						harvest_map.append((get_pos_x(),get_pos_y()))
						plant(Entities.Grass)
					move(North)
				move(East)

		# Plant and map partial field
		else:
			for i in range (get_world_size()):
				for j in range (get_world_size()):
					if (len(harvest_map) * unit_harvest + num_items(Items.Hay)) < mark:
						plant(Entities.Grass)
						harvest_map.append((get_pos_x(),get_pos_y()))
						move(North)
					else:
						break
				if (num_items(Items.Hay) < mark):
					move(East)
				else:
					break

		# Harvest any remaining grass
		while (len(harvest_map) > 0):
			move_to(harvest_map[0][0], harvest_map[0][1])
			if (can_harvest()):
				harvest()
			else:
				harvest_map.append((get_pos_x(), get_pos_y()))
			harvest_map.pop(0)
	
	def grass_benchmark():
		def run_benchmark(tester):
			clear_tilled()
			reset()
			if verbose:
				quick_print("")
				quick_print(tester[1])
				quick_print("Starting Water:", get_water())
			
			start_num = num_items(Items.Hay)
			start_ops = get_tick_count()
			start_time = get_time()
			
			tester[0]()
			
			ops_used = get_tick_count() - start_ops
			time_elapsed = get_time() - start_time
			items_produced = num_items(Items.Hay) - start_num

			if verbose:
				quick_print("Goal:", goal, "Items Produced:", items_produced)
				quick_print("Time Elapsed:", time_elapsed)
				quick_print("     Items per second:", (items_produced / time_elapsed))
				quick_print("Operations Used:", ops_used)
				quick_print("     Operations per item:", (ops_used / items_produced))
			return (time_elapsed, ops_used, items_produced/time_elapsed, ops_used/items_produced)

		func_list = [[grass_full, "Full Grass", 0],
			[grass_clean, "Clean Grass", 0],
			[grass_precise_v2, "Precision Grass", 0]]
		
		for i in func_list:
			i[2] = run_benchmark(i)

		quick_print("")
		quick_print("-----------------")
		quick_print("Benchmark Results")
		quick_print("-----------------")
		quick_print("Name : Time : Operations: Items/Sec : Ops/Item")
		for i in func_list:
			quick_print(i[1], ":", i[2][0], ":", i[2][1], ":", i[2][2], ":", i[2][3])

	#Full benchmark for all world sizes?

	if benchmark:
		grass_benchmark()
	else:
		grass_precise_v2()

grass(5000, True, True)