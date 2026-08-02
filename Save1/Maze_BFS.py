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

	def set_wall(pos, dir, value):
		# When setting a wall, it needs to set both (N/S, and E/W)
		if dir not in compass:
			quick_print("Set Wall: ERROR! Invalid direction provided")
			return
		if wall_map[pos[0]][pos[1]][dir] == None:
			return
		dx, dy = compass[dir]["offset"]

		wall_map[pos[0]][pos[1]][dir] = value
		wall_map[pos[0] + dx][pos[1] + dy][compass[dir]["reverse"]] = value

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
			use_item(Items.Weird_Substance, substance)

			# Get and set initial positions
			pos = (get_pos_x(), get_pos_y())
			x, y = pos
			destination = measure()

			# Full Map Reset, generate initial value map
			full_reset()
			full_flood()

			# Solve current maze
			while (pos != destination):
				# Wall check
				if not move_map[x][y]:
					for i in range(4):
						wall_value = compass[i]["direction"]
						if (can_move(wall_value) != wall_map[x][y]):
							set_wall(pos, wall_value, i)
					move_map[x][y] = True


				# Check for lowest value
				lowest = None
				for i in range(4):
					dx, dy = compass[i]["offset"]
					# Check wall for valid move
					if (wall_map[x][y] in (False, None)):
						continue
					# Ensure option is in value map
					if (value_map[x + dx][y + dy] == None):
						continue
					# Check if a value has already been set
					if (lowest == None):
						lowest = value_map[x + dx][y + dy]
						continue
					# Set lower value
					lowest = min(lowest, value_map[x + dx][y + dy])



				# Begin following value map
					# Lowest value > Remap if none
					# Remove from value map when moved to

				# A

				



		harvest()
	

	while (num_items(Items.Gold) < goal):
		maze()

gold_BFS(num_items(Items.Gold) + 1)