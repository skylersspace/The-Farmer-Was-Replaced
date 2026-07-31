from Utility import *
from Weird import *

reuse = 1

def gold_BFS(goal):
	# Ensure a run is required before continuing
	if (num_items(Items.Gold) > goal):
		return

	WORLD_SIZE = get_world_size()
	# FIELD_SIZE = WORLD_SIZE ** 2

	compass = {
		0: {
			"direction": North,
			"offset": (0, 1),
			"reverse": 2
		},
		1: {
			"direction": East,
			"offset": (1, 0),
			"reverse": 3
		},
		2: {
			"direction": South,
			"offset": (0, -1),
			"reverse": 0
		},
		3: {
			"direction": West,
			"offset": (-1, 0),
			"reverse": 1
		}
	}

	# TOTAL RESET
	# Wall map is persistent during the entire run
	wall_map = []
		# True == Can move, default
		# False == Cannot move
		# None == Out of bounds

	# FULL RESET
	# Refreshes each run of the maze
	move_map = []
		# True == Cell visited
		# False == Cell unvisited, default

	# END RESET
	# Refreshes each run of the maze, or if drone is in latter half of the route
	# ???

	# START RESET
	# Refreshes each run of the maze, and every time the route needs recalculated
	start_map = []
		# True == Cell in map
		# False == Cell not in map, default
	value_map = []
		# Contains the distance to the goal
		# None = No value, default

	# Refresh all maps
	def total_reset():
		meet_value = None
		for i in range(WORLD_SIZE):
			wall_map.append([])
			move_map.append([])
			end_map.append([])
			meet_map.append([])
			start_map.append([])
			value_map.append([])
			for j in range(WORLD_SIZE):
				wall_map[i].append([True, True, True, True])
				move_map[i].append(False)
				end_map[i].append(False)
				meet_map[i].append(False)
				start_map[i].append(False)
				value_map[i].append(None)
		# Set wall map edges
		max_map = WORLD_SIZE - 1
		for i in range(WORLD_SIZE):
			# North
			wall_map[i][max_map][0] = None
			# East
			wall_map[max_map][i][1] = None
			# South
			wall_map[i][0][2] = None
			# West
			wall_map[0][i][3] = None

	def full_reset():
		meet_value = None
		for i in range(WORLD_SIZE):
			move_map.append([])
			end_map.append([])
			meet_map.append([])
			start_map.append([])
			value_map.append([])
			for j in range(WORLD_SIZE):
				move_map[i].append(False)
				end_map[i].append(False)
				meet_map[i].append(False)
				start_map[i].append(False)
				value_map[i].append(None)
	
	def end_reset():
		meet_value = None
		for i in range(WORLD_SIZE):
			end_map.append([])
			meet_map.append([])
			start_map.append([])
			value_map.append([])
			for j in range(WORLD_SIZE):
				end_map[i].append(False)
				meet_map[i].append(False)
				start_map[i].append(False)
				value_map[i].append(None)
	
	def start_reset():
		for i in range(WORLD_SIZE):
			start_map.append([])
			value_map.append([])
			for j in range(WORLD_SIZE):
				start_map[i].append(False)
				value_map[i].append(None) # BUG! This isn't something I want to fully reset
	
	# Full flood function
	def full_flood():
		quick_print()

	# Partial flood function
	def partial_flood():
		quick_print()

	# Maze code
	def maze():
		substance = WORLD_SIZE * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		# Use same amount of substance to reuse maze on treasure
		# Max reuse 300 times -> Need to verify
		# Original value below for reuse == 301
		weird(substance * reuse)
	
		# Spawn the maze, reset maps
		plant(Entities.Bush)
		total_reset()

		# Reuse the same maze x times
		for i in range(reuse):
			use_item(Items.Weird_Substance,  substance)

			# Get and set initial positions
			pos = (get_pos_x(), get_pos_y())
			destination = measure()

			# Full Map Reset
			full_reset()
			full_flood()

			# Generate initial value map

			# Solve current maze
			while (pos != destination):
				quick_print()
				# Begin following value map
					# Lowest value > Remap if none
					# Remove from value map when moved to

				



		harvest()
	

	while (num_items(Items.Gold) < goal):
		maze()

gold_BFS(num_items(Items.Gold) + 1)