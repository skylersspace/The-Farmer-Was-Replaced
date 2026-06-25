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
			
	def blind_solve_left(map, destination):
		move_map = gen_move_map()

		facing = 0
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

	def gen_flood_full(wall_map, destination):
		# Create distance map. Unset distances are None
		path_map = []
		for i in range(WORLD_SIZE):
			path_map.append([])
			for j in range(WORLD_SIZE):
				path_map[i].append(None)

		# Begin the BFS algorithm
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

	def solve_full_flood(map, destination):
		move_map = gen_move_map()
		path_map = gen_flood_full(map, destination)

		x, y = (get_pos_x(), get_pos_y())
		pos = (x, y)
		while (pos != destination):
			# If unvisited, check for walls
			if not move_map[x][y]:
				for i in range(4):
					# Compare to existing wall map
					wall_check = can_move(compass[i]["direction"])
					# Guards against out of bound checks
					if (map[x][y][i] == None):
						continue
					# Compares wall values
					if (map[x][y][i] == wall_check):
						continue
					
					set_wall(map, pos, i, wall_check)
					path_map = gen_flood_full(map, destination)
				move_map[x][y] = True

			# Find the lowest value
			lowest_val = FIELD_SIZE
			for i in range(4):
				if (not map[x][y][i]):
					continue
				lowest_val = min(lowest_val, path_map[x + compass[i]["offset"][0]][y + compass[i]["offset"][1]])

			# Move along the fastest path
			for i in range(4):
				if (not map[x][y][i]):
					continue
				if (path_map[x + compass[i]["offset"][0]][y + compass[i]["offset"][1]] == lowest_val):
					move(compass[i]["direction"])
					break
			
			# Update for the next loop
			x, y = (get_pos_x(), get_pos_y())
			pos = (x, y)
	
	def find_flood_path_bi(wall_map, start, destination):
		# Initialize the maps
		quick_print("Starting bidirectional map")
		start_map = []
		end_map = []
		for i in range(WORLD_SIZE):
			start_map.append([])
			end_map.append([])
			for j in range(WORLD_SIZE):
				start_map[i].append(None)
				end_map[i].append(None)

		# Begin the BFS algorithm
		start_map[start[0]][start[1]] = 0
		end_map[destination[0]][destination[1]] = 0
		queue_start = [start]
		queue_end = [destination]

		junction = None
		while(junction == None):
			current_start = queue_start.pop(0)
			current_end = queue_end.pop(0)
			x1, y1 = (current_start[0], current_start[1])
			x2, y2 = (current_end[0], current_end[1])
			curr_value_start = start_map[x1][y1]
			curr_value_end = end_map[x2][y2]
			
			for i in compass:
				dx1, dy1 = (x1 + compass[i]["offset"][0], y1 + compass[i]["offset"][1])
				dx2, dy2 = (x2 + compass[i]["offset"][0], y2 + compass[i]["offset"][1])
				
				# Check for possible movement, and that it hasn't already been mapped
				if (wall_map[x1][y1][i] and start_map[dx1][dy1] == None):
					start_map[dx1][dy1] = curr_value_start + 1
					queue_start.append((dx1, dy1))
					# Check for junction point
					if (end_map[dx1][dy1] != None):
						junction = (dx1, dy1)
						break
				if (wall_map[x2][y2][i] and end_map[dx2][dy2] == None):
					end_map[dx2][dy2] = curr_value_end + 1
					queue_end.append((dx2, dy2))
					if (start_map[dx2][dy2] != None):
						junction = (dx2, dy2)
						break

		# Calculate path
		# Start at the junction, work out
		# Once done, merge and return list
		quick_print("Calculating path")

		# Drone List
		start_move = []
		x, y = junction
		dx, dy = (0, 0)
		pos = (x, y)
		while (pos != start):
			current_value = FIELD_SIZE
			for i in range(4):
				if (wall_map[x][y][i] != True):
					continue
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
				if start_map[dx][dy] == None:
					continue
				current_value = min(current_value, start_map[dx][dy])

			for i in range(4):
				if (wall_map[x][y][i] != True):
					continue
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
				if start_map[dx][dy] == current_value:
					start_move.insert(0, compass[i]["direction"])
					break
			
			x, y = (dx, dy)
			pos = (dx, dy)

		# Destination List
		end_move = []
		x, y = junction
		pos = (x, y)
		while (pos != destination):
			current_value = FIELD_SIZE
			for i in range(4):
				if (wall_map[x][y][i] == None):
					continue
				if (wall_map[x][y][i] == False):
					continue
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
				if end_map[dx][dy] == None:
					continue
				current_value = min(current_value, end_map[dx][dy])

			for i in range(4):
				if (wall_map[x][y][i] == None):
					continue
				if (wall_map[x][y][i] == False):
					continue
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])
				if end_map[dx][dy] == current_value:
					end_move.append(compass[i]["direction"])
					break

			x, y = (dx, dy)
			pos = (dx, dy)
		
		start_move.pop()
		answer = start_move + end_move
		return answer
	
	def follow_path(wall_map, destination):
		move_map = gen_move_map()
		pos = (get_pos_x(), get_pos_y())
		
		while (pos != destination):
			path = find_flood_path_bi(wall_map, pos, destination)
			for i in path:
				quick_print("Starting to follow path")
				
				# Ensure wall map is accurate
				update = False
				if not move_map[pos[0]][pos[1]]: # CHECK: IS THIS ACCURATE
					for j in range(4):
						quick_print("Checking wall", pos, compass[j]["direction"], wall_map[pos[0]][pos[1]][j], can_move(compass[j]["direction"]))
						if (wall_map[pos[0]][pos[1]][j] == None):
							quick_print("Skipping check. (None)")
							continue
						if (wall_map[pos[0]][pos[1]][j] != can_move(compass[j]["direction"])):
							quick_print("Updating wall")
							set_wall(wall_map, pos, j, can_move(compass[j]["direction"]))
							update = True
					move_map[pos[0]][pos[1]] = True
				
				pos = (get_pos_x(), get_pos_y())
				if update:
					quick_print("Break the loop!")
					path = find_flood_path_bi(wall_map, pos, destination)
					break

				# Move
				quick_print("Moving", i)
				move(i)
				
		quick_print("Finish")	
		harvest()


	def maze():
		substance = WORLD_SIZE * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		# Use same amount of substance to reuse maze on treasure
		# Max reuse 300 times
		weird(substance * 301)

		# Spawn the maze
		plant(Entities.Bush)
		use_item(Items.Weird_Substance,  substance)

		map = gen_wall_map()
		destination = measure()

		# UNDER DEVELOPMENT
		
		#Begin solving blindly, while mapping

		# blind_solve_left(map, destination)
		# blind_solve_right(map, destination)
		# solve_path(map, destination)
		# solve_full_flood(map, destination)

		# use_item(Items.Weird_Substance,  substance)
		# destination = measure()

		
		# for i in range(300):
		# 	quick_print("Running map iteration", i)
		# 	use_item(Items.Weird_Substance,  substance)
		# 	destination = measure()
		# 	THING FUNCTION
		# harvest()
		
		find_flood_path_bi(map, (get_pos_x(), get_pos_y()), destination) 
		# follow_path(map, destination)

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
	# quick_print("")
	# reset()