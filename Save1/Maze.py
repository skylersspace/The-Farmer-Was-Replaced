from Utility import *
from Weird import *

def gold(goal):
	WORLD_SIZE = get_world_size()
	# FIELD_SIZE = WORLD_SIZE ** 2

	def print_map(map):
		for i in range(WORLD_SIZE - 1, -1, -1):
			line_string = ""
			for j in range(WORLD_SIZE):
				line_string = line_string + str(map[j][i]) + ", "
			quick_print(line_string)

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
	
	def gen_wall_map():
		# True == Can move, default state
		# False == Cannot move
		# None == Out of bounds
		maze_map = []
		for i in range(WORLD_SIZE):
			maze_map.append([])
			for j in range(WORLD_SIZE):
				maze_map[i].append([True, True, True, True])

		max_map = WORLD_SIZE - 1
		# quick_print("Max map:", max_map)
		for i in range(WORLD_SIZE):
			# North
			maze_map[i][max_map][0] = None
			# East
			maze_map[max_map][i][1] = None
			# South
			maze_map[i][0][2] = None
			# West
			maze_map[0][i][3] = None

		return maze_map

	def set_wall(wall_map, pos, dir, wall_value):
		# When setting a wall, it needs to set both (N/S, and E/W)
		if dir not in compass:
			quick_print("ERROR! Invalid direction provided")
			return
		if wall_map[pos[0]][pos[1]][dir] == None:
			return
		dx, dy = compass[dir]["offset"]

		wall_map[pos[0]][pos[1]][dir] = wall_value
		wall_map[pos[0] + dx][pos[1] + dy][compass[dir]["reverse"]] = wall_value

	def gen_move_map():
		move_map = []
		for i in range(WORLD_SIZE):
			move_map.append([])
			for j in range(WORLD_SIZE):
				move_map[i].append(False)

		return move_map
		
	def gen_flood_fill(wall_map, destination):
		# Create distance map. Unset distances are None
		path_map = []
		for i in range(WORLD_SIZE):
			path_map.append([])
			for j in range(WORLD_SIZE):
				path_map[i].append(None)

		# Begin the DFS algorithm
		path_map[destination[0]][destination[1]] = 0
		queue = [destination]

		while len(queue) > 0:
			current = queue.pop(0)
			x, y = (current[0], current[1])
			curr_value = path_map[x][y]	
			
			for i in compass:
				x2, y2 = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
				
				# Check for possible movement, and that it hasn't already been mapped
				if (wall_map[x][y][i] and path_map[x2][y2] == None):
					path_map[x2][y2] = curr_value + 1
					queue.append((x2, y2))

		return path_map
	
	def flood_fill_add_wall (wall_map, distance_map, pos):
		quick_print("Flood Fill: Adding Wall")
		# Find and invalidate affected paths
		root = None
		queue = [pos]
		while (len(queue) > 0):
			# Loop setup
			current = queue.pop(0)
			x, y = current
			current_value = distance_map[x][y]
			# Better logic to negate this?
			if (current_value == None):
				continue
			quick_print("Loop:", current, current_value, )

			for i in range(4):
				# Check for open path
				if (not wall_map[x][y][i]):
					continue
				dx, dy = (compass[i]["offset"][0], compass[i]["offset"][1])
				target_value = distance_map[x + dx][y + dy]
				# Check for alternate neighbor route
				if (target_value == current_value - 1):
					if (root == None or target_value < distance_map[root[0]][root[1]]):
						quick_print("Updating Root", root)
						root = (x + dx, y + dy)
					break
				# Check for child path
				if (target_value == current_value + 1):
					distance_map[x][y] = None
					queue.append((x + dx, y + dy))

		if (root != None):
			# Begin the DFS algorithm to reflood the cells
			queue = [root]

			while len(queue) > 0:
				current = queue.pop(0)
				x, y = (current[0], current[1])
				current_value = distance_map[x][y]	
				
				for i in compass:
					x2, y2 = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
					
					# Check for possible movement, and that it hasn't already been mapped
					if (wall_map[x][y][i] and distance_map[x2][y2] == None):
						distance_map[x2][y2] = current_value + 1
						queue.append((x2, y2))
	
	def flood_fill_del_wall (wall_map, distance_map, pos, dir):
		# Update the map when a wall is discovered to be missing


		return distance_map

	def blind_solve_left(map, destination):
		# Always follow the left wall
		# quick_print("Blind left")

		facing = 0
		
		move_map = gen_move_map()

		pos = (get_pos_x(), get_pos_y())
		while (pos != destination):
			if not move_map[pos[0]][pos[1]]:
				for i in range(4):
					set_wall(map, pos, i, can_move(compass[i]["direction"]))
				move_map[pos[0]][pos[1]] = True

			# Attempt to move Left > Forward > Right > Back
			for i in range(facing - 1, facing + 3):
				direction = i % 4
				if (move(compass[direction]["direction"])):
					facing = direction
					if (map[pos[0]][pos[1]][direction] == False):
						quick_print("ERROR! BAD MAPPING", pos, map[pos[0]][pos[1]], direction)
					break
				
			pos = (get_pos_x(), get_pos_y())

	def blind_solve_right(map, destination):
		# Always follow the left wall
		# quick_print("Blind right")

		facing = 0
		
		move_map = gen_move_map()

		pos = (get_pos_x(), get_pos_y())
		while (pos != destination):
			if not move_map[pos[0]][pos[1]]:
				for i in range(4):
					set_wall(map, pos, i, can_move(compass[i]["direction"]))
				move_map[pos[0]][pos[1]] = True

			# Attempt to move Right > Forward > Left > Back
			for i in range(facing + 1, facing - 3, -1):
				direction = i % 4
				if (move(compass[direction]["direction"])):
					facing = direction
					if (map[pos[0]][pos[1]][direction] == False):
						quick_print("ERROR! BAD MAPPING", pos, map[pos[0]][pos[1]], direction)
					break
				
			pos = (get_pos_x(), get_pos_y())

	def solve_path(map, destination):
		# Calculate the path to the goal, checking for new open paths along the way
		quick_print("Solve Path")

		move_map = gen_move_map()
		path_map = gen_flood_fill(map, destination)
		quick_print("Initial path map")
		print_map(path_map)

		x, y = (get_pos_x(), get_pos_y())
		pos = (x, y)
		while (pos != destination):
			quick_print("")
			# If unvisited, check for walls
			if not move_map[x][y]:
				quick_print("New cell, checking for walls")
				for i in range(4):
					# Compare to existing wall map
					wall_check = can_move(compass[i]["direction"])
					if (map[x][y][i] == None):
						continue
					if (map[x][y][i] == wall_check):
						continue
					if (not wall_check):
						quick_print("Setting new wall")
						set_wall(map, pos, i, wall_check)
						flood_fill_add_wall(map, path_map, pos)
						quick_print("New path map")
						print_map(path_map)
					else:
						quick_print("ERROR: This shouldn't trigger yet.")
						set_wall(map, pos, i, wall_check)
						flood_fill_del_wall(map, path_map, pos, i)
						# THIS CODE CURRENTLY ISN'T FUNCTIONAL 
				move_map[x][y] = True

			# Find the lowest value
			lowest_val = FIELD_SIZE
			quick_print("Current Position:", x, y)
			for i in range(4):
				if (not map[x][y][i]):
					quick_print("Wall detected, invalid move path")
					continue
				quick_print("Dir:", i, "Neighbor value:", path_map[x + compass[i]["offset"][0]][y + compass[i]["offset"][1]])
				lowest_val = min(lowest_val, path_map[x + compass[i]["offset"][0]][y + compass[i]["offset"][1]])
			
			quick_print("Lowest val:", lowest_val)

			# Move along the fastest path
			for i in range(4):
				if (path_map[x + compass[i]["offset"][0]][y + compass[i]["offset"][1]] == lowest_val):
					quick_print("Moving:", compass[i]["direction"])
					move(compass[i]["direction"])
					break
			
			# Update for the next loop
			x, y = (get_pos_x(), get_pos_y())
			pos = (x, y)

	def maze():
		substance = WORLD_SIZE * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		# Use same amount of substance to reuse maze on treasure
		# Max reuse 300 times
		weird(substance * 301)

		# Spawn the maze
		plant(Entities.Bush)
		use_item(Items.Weird_Substance,  substance)
		
		# Entities.Hedge vs Entities.Treasure

		map = gen_wall_map()
		destination = measure()

		#Begin solving blindly, while mapping
		for i in range(5):
			blind_solve_left(map, destination)
			use_item(Items.Weird_Substance, substance)
			destination = measure()
		# blind_solve_right(map, destination)
		solve_path(map, destination)
	
		# quick_print(map)
		# After blindly solving, not all of the maze will be mapped.
		# Will need to re-map as the drone attempts to navigate to the target.
		# This will also potentially find modified walls

		# Reuse the maze
		# for i in range(300):
		# 	goal = measure()



	# while (num_items(Items.Gold) < goal):
	# 	maze()

	maze()

for test in range(1):
	quick_print("Run started")
	gold(1)
	quick_print("Run complete")

	harvest()
	quick_print("")
	# reset()