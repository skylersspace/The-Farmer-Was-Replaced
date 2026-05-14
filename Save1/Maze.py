from Utility import *
from Weird import *

def gold(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2

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

	def gen_move_map():
		move_map = []
		for i in range(WORLD_SIZE):
			move_map.append([])
			for j in range(WORLD_SIZE):
				move_map[i].append(False)

		return move_map
	
	def gen_flood_fill(wall_map, destination):
		# Create distance map. Unset distances are None
		distance_map = []
		for i in range(WORLD_SIZE):
			distance_map.append([])
			for j in range(WORLD_SIZE):
				distance_map[i].append(None)

		# Set destination to a distance of 0
		distance_map[destination[0]][destination[1]] = 0

		# The destination is the starting point
		queue = [destination]
		head = 0

		while head < len(queue):
			# Set next queue coordinates
			qx, qy = queue[head]
			head = head + 1

			# Check each direction
			for i in range(4):
				# Get the next coordinate
				dx, dy = compass[i]["offset"]
				nx = qx + dx
				ny = qy + dy

				# Perform checks to ensure it is a valid target
				if nx < 0 or nx >= WORLD_SIZE:
					continue
				if ny < 0 or ny >= WORLD_SIZE:
					continue
				if distance_map[nx][ny] != None:
					continue
				if (wall_map[nx][ny][compass[i]["reverse"]] == False) or (wall_map[nx][ny][compass[i]["reverse"]] == None):
					continue

				# Set the distance value
				distance_map[nx][ny] = distance_map[qx][qy] + 1
				# Add next coordinate to queue
				queue.append((nx, ny))
		
		return distance_map
	
	def update_flood_fill(wall_map, distance_map, pos, dir):
		# Update the map when a wall is discovered

		# Get the now blocked neighbor
		pos_x, pos_y = pos
		dx, dy = compass[dir]["offset"]
		nx = pos_x + dx
		ny = pos_y + dy

		# Gather cells that need invalidated
		to_invalidate = []
		inv_head = 0
		if (distance_map[pos_x][pos_y] != None) and (distance_map[nx][ny] != None):
			# Check which side is further from the destination and is now blocked off
			if distance_map[pos_x][pos_y] > distance_map[nx][ny]:
				to_invalidate.append((pos_x, pos_y))
			else:
				to_invalidate.append((nx, ny))
		
		# Invalidate affected cells that could have passed through this cell, starting at the head
		distance_map[to_invalidate[0][0]][to_invalidate[0][1]] = None
		
		while inv_head < len(to_invalidate):
			# Set the current coordinates at the head of the list
			cx, cy = to_invalidate[inv_head]
			inv_head = inv_head + 1

			# Check the directions for a route from this cell
			for i in range(4):
				dx, dy = compass[i]["offset"]
				ax = cx + dx
				ay = cy + dy
				
				if (ax < 0) or (ax >= WORLD_SIZE):
					continue
				if (ay < 0) or (ay >= WORLD_SIZE):
					continue
				if distance_map[ax][ay] == None:
					continue
				if (wall_map[ax][ay][compass[i]["reverse"]] == False) or (wall_map[ax][ay][compass[i]["reverse"]] == None):
					continue
				# Invalidate if it could have routed through this cell
				if distance_map[ax][ay] == distance_map[cx][cy] + 1:
					distance_map[ax][ay] = None
					to_invalidate.append((ax, ay))
		
		# Re-flood the invalidated cells from a valid neighbor
		queue = []
		head = 0

		for i in range(len(to_invalidate)):
			# Set the current coordinates 
			cx, cy = to_invalidate[i]
			for j in range(4):
				dx, dy = compass[j]["offset"]
				ax = cx + dx
				ay = cy + dy

				if (ax < 0) or (ax >= WORLD_SIZE):
					continue
				if (ay < 0) or (ay >= WORLD_SIZE):
					continue
				if distance_map[ax][ay] == None:
					continue
				if (wall_map[ax][ay][compass[j]["reverse"]] == False) or (wall_map[ax][ay][compass[j]["reverse"]] == None):
					continue
				
				# Valid neighbor present, queue for re-flood
				distance_map[cx][cy] = distance_map [ax][ay] +1
				queue.append((cx, cy))
				break

		# BFS outward from the re-flood seeds to restore all invalidated distances
		while head < len(queue):
			cx, cy = queue[head]
			head = head + 1

			for i in range(4):
				dx, dy = compass[i]["offset"]
				ax = cx + dx
				ay = cy + dy

				if (ax < 0) or (ax >= WORLD_SIZE):
					continue
				if (ay < 0) or (ay >= WORLD_SIZE):
					continue
				if distance_map[ax][ay] == None:
					continue
				if (wall_map[ax][ay][compass[i]["reverse"]] == False) or (wall_map[ax][ay][compass[i]["reverse"]] == None):
					continue

				# Propagate distance outward to unset neighbors
				distance_map[cx][cy] = distance_map [ax][ay] +1
				queue.append((cx, cy))

		return distance_map

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

	def blind_solve_path(map, destination):
		quick_print("Blind Path")

		move_map = gen_move_map()

		distance_map = gen_flood_fill(map, destination)
		quick_print(distance_map)
		
		pos = (get_pos_x(), get_pos_y())
		while (pos != destination):
			if not move_map[pos[0]][pos[1]]:
				for i in range(4):
					if can_move(compass[i]["direction"]):
						continue
					set_wall(map, pos, i, can_move(compass[i]["direction"]))
					update_flood_fill(map, distance_map, pos, i)
				move_map[pos[0]][pos[1]] = True

			# Move in a valid direction, towards the destination
			test_move = []
			best_distance = None
			move_dir = None
			for i in range(4):
				if not (map[pos[0]][pos[1]][i] == True):
					test_move.append(None)
					continue
				test_move.append(distance_map[pos[0] + compass[i]["offset"][0]][pos[1] + compass[i]["offset"][1]])
				if best_distance == None or test_move[i] < best_distance:
					move_dir = i
					best_distance = test_move[i]

			# Move	
			move(compass[i]["direction"])
			pos = (get_pos_x(), get_pos_y())

	def solve_path(map, destination):
		# Calculate the path to the goal, checking for new open paths along the way
		quick_print("Solve Path")

		move_map = gen_move_map()

		distance_map = gen_flood_fill(map, destination)
		quick_print(distance_map)

		# pos = (get_pos_x(), get_pos_y())
		# while (pos != destination):
		# 	if not move_map[pos[0]][pos[1]]:
		# 		for i in range(4):
		# 			map[pos[0]][pos[1]][i] = can_move(compass[i]["direction"])
		# 		move_map[pos[0]][pos[1]] = True

			# Begin DFS algorithm

	def maze():
		substance = WORLD_SIZE * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		# Use same amount of substance to reuse maze on treasure
		# Max reuse 300 times
		weird(substance * 301)

		# Spawn the maze
		plant(Entities.Bush)
		use_item(Items.Weird_Substance,  substance)
		
		# Entities.Hedge vs Entities.Treasure

		destination = measure()
		map = gen_wall_map()

		#Begin solving blindly, while mapping

		# blind_solve_left(map, destination)
		# blind_solve_right(map, destination)
		blind_solve_path(map, destination)
	
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