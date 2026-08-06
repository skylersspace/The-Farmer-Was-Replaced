from Utility import *
from Weird import *

# 301 worked fine
reuse = 300

def gold_BFS(goal):
	quick_print("BFS Maze function called")

	# Ensure a run is required before continuing
	if (num_items(Items.Gold) > goal):
		quick_print("Goal already met, exiting")
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
	value_map = []
		# Contains the distance to the goal
		# None = No value, default

	# START RESET
		# Refreshes each run of the maze, and every time the route needs recalculated
	start_map = []
		# True == Cell in map
		# False == Cell not in map, default
	end_map = []
		# True == Cell in map
		# False == Cell not in map, default

	# Generate all maps
	for i in range(WORLD_SIZE):
		wall_map.append([])
		move_map.append([])
		end_map.append([])
		start_map.append([])
		value_map.append([])
		for j in range(WORLD_SIZE):
			wall_map[i].append([True, True, True, True])
			move_map[i].append(False)
			end_map[i].append(False)
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

	# Reset all maps
	def total_reset():
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				wall_map[i][j] = [True, True, True, True]
				move_map[i][j] = False
				start_map[i][j] = False
				end_map[i][j] = False
				value_map[i][j] = None
		# Set wall map edges
		for i in range(WORLD_SIZE):
			# North
			wall_map[i][max_map][0] = None
			# East
			wall_map[max_map][i][1] = None
			# South
			wall_map[i][0][2] = None
			# West
			wall_map[0][i][3] = None

	# Refresh move, start, end, and value maps
	def full_reset():
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				move_map[i][j] = False
				start_map[i][j] = False
				end_map[i][j] = False
				value_map[i][j] = None
	
	# Refresh start and end map
	def recalc_reset():
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				start_map[i][j] = False
				end_map[i][j] = False
	
	# Full flood function
	def full_flood(start, end):
		full_reset()

		x1, y1 = start
		x2, y2 = end

		value_map[x2][y2] = 0

		start_map[x1][y1] = True
		end_map[x2][y2] = True

		start_queue = [start]
		end_queue = [end]

		junction = None
		# quick_print("Beginning initial flood")
		while (junction == None):
			# quick_print("Start:", len(start_queue), "End:", len(end_queue))
			start_curr = start_queue.pop(0)
			end_curr = end_queue.pop(0)
			x1, y1 = start_curr
			x2, y2 = end_curr
			value_curr_end = value_map[x2][y2]

			for i in compass:
				dx1, dy1 = (x1 + compass[i]["offset"][0], y1 + compass[i]["offset"][1])
				dx2, dy2 = (x2 + compass[i]["offset"][0], y2 + compass[i]["offset"][1])

				# Check for possible movement, then possible junction, then map if present
				# Goal side
				if (wall_map[x2][y2][i] not in (False, None)):
					if (start_map[dx2][dy2]):
						junction = (x2, y2)
						break
					if (not end_map[dx2][dy2]):
						end_queue.append((dx2, dy2))
						value_map[dx2][dy2] = value_curr_end + 1
						end_map[dx2][dy2] = True
				# Drone side
				if (wall_map[x1][y1][i] not in (False, None)):
					if (end_map[dx1][dy1]):
						junction = (dx1, dy1)
						break
					if (not start_map[dx1][dy1]):
						start_queue.append((dx1, dy1))
						start_map[dx1][dy1] = True

		# Reverse the start map to point to the end
		# quick_print("Junction found:", junction)
		start_queue = [junction]
		while (len(start_queue) > 0):
			# quick_print("Current queue:", len(start_queue))
			current = start_queue.pop(0)
			x, y = current
			curr_value = value_map[x][y]

			for i in compass:
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])

				# Check for possible movement within start map
				if (wall_map[x][y][i] in (False, None)):
					continue
				# Check for drone location
				if ((dx, dy) == start):
					start_queue = []
					break
				if (start_map[dx][dy] == True):
					start_queue.append((dx, dy))
					start_map[dx][dy] = False
					value_map[dx][dy] = curr_value + 1

	# Partial flood function
	def recalc_flood(start, end):
		recalc_reset()
		end_queue = []
		end_map[end[0]][end[1]] = True

		queue = [end]
		
		while (len(queue) > 0):
			current = queue.pop(0)
			x, y = (current[0], current[1])

			for i in compass:
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])

				# Check for valid movement option
				if (wall_map[x][y][i] in (None, False)):
					continue
				# Check if already in end map, add if not
				if (end_map[dx][dy]):
					continue
				end_map[dx][dy] = True
				# If there's already a value, add to queue. If a border value, queue for later propagation
				if (value_map[dx][dy] != None):
					queue.append((dx, dy))
				else:
					end_queue.append((dx, dy))
					value_map[dx][dy] = value_map[x][y] + 1

		# Begin bidirectional flood
		x1, y1 = start
		x2, y2 = end

		start_map[x1][y1] = True

		start_queue = [start]

		junction = None
		# quick_print("Beginning initial flood")
		while (junction == None):
			start_curr = start_queue.pop(0)
			end_curr = end_queue.pop(0)
			x1, y1 = start_curr
			x2, y2 = end_curr
			value_curr_end = value_map[x2][y2]

			for i in compass:
				dx1, dy1 = (x1 + compass[i]["offset"][0], y1 + compass[i]["offset"][1])
				dx2, dy2 = (x2 + compass[i]["offset"][0], y2 + compass[i]["offset"][1])

				# Check for possible movement, then possible junction, then map if present
				# Goal side
				if (wall_map[x2][y2][i] not in (False, None)):
					if (start_map[dx2][dy2]):
						junction = (x2, y2)
						break
					if (not end_map[dx2][dy2]):
						end_queue.append((dx2, dy2))
						value_map[dx2][dy2] = value_curr_end + 1
						end_map[dx2][dy2] = True
				# Drone side
				if (wall_map[x1][y1][i] not in (False, None)):
					if (end_map[dx1][dy1]):
						junction = (dx1, dy1)
						break
					if (not start_map[dx1][dy1]):
						start_queue.append((dx1, dy1))
						start_map[dx1][dy1] = True

		# Reverse the start map to point to the end
		start_queue = [junction]
		# quick_print("Junction found:", junction)
		while (len(start_queue) > 0):
			current = start_queue.pop(0)
			x, y = current
			curr_value = value_map[x][y]

			for i in compass:
				dx, dy = (x + compass[i]["offset"][0], y + compass[i]["offset"][1])

				# Check for possible movement within start map
				if (wall_map[x][y][i] in (False, None)):
					continue
				# Check for drone location
				if ((dx, dy) == start):
					start_queue = []
					break
				if (start_map[dx][dy] == True):
					start_queue.append((dx, dy))
					start_map[dx][dy] = False
					value_map[dx][dy] = curr_value + 1

	def set_wall(pos, dir, value):
		# When setting a wall, it needs to set both (N/S, and E/W)
		if dir not in compass:
			quick_print("Set Wall: ERROR! Invalid direction provided")
			return
		if wall_map[pos[0]][pos[1]][dir] == None:
			return
		quick_print("- - - Updating wall")
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
		quick_print("- Initial maze generation")

		# Reuse the same maze x times
		for i in range(reuse):
			quick_print("- - Iteration", i + 1)
			use_item(Items.Weird_Substance, substance)

			# Get and set initial positions
			pos = (get_pos_x(), get_pos_y())
			x, y = pos
			destination = measure()

			# Full Map Reset, generate initial value map
			quick_print("- - - Full flood:", pos, "to", destination)
			full_flood(pos, destination)

			# Solve current maze
			quick_print("- - - Begin solving")
			while (pos != destination):
				# quick_print("Current position:", pos)
				# Wall check
				if not move_map[x][y]:
					for i in range(4):
						wall_value = can_move(compass[i]["direction"])
						if (wall_value != wall_map[x][y][i]):
							set_wall(pos, i, wall_value)
					move_map[x][y] = True

				# Check for lowest value
				lowest = None
				lowest_dir = None
				for i in range(4):
					dx, dy = compass[i]["offset"]
					# Check wall for valid move
					if (wall_map[x][y][i] in (False, None)):
						continue
					# Ensure option is in value map
					if (value_map[x + dx][y + dy] == None):
						# AI is saying the == should be 'is' instead? May need to revisit this.
						continue
					# Check and set new value
					value = value_map[x + dx][y + dy]
					if (lowest == None) or (lowest > value):
						lowest = value
						lowest_dir = i

				# If valid direction, proceed
				if (lowest_dir != None):
					move(compass[lowest_dir]["direction"])
					pos = (get_pos_x(), get_pos_y())
					x, y = pos
					value_map[x][y] = None
					end_map[x][y] = False
					continue

				# No valid path found. Recalculating
				quick_print("- - - - No movement available, recalculating")
				recalc_flood(pos, destination)

		harvest()
	
	while (num_items(Items.Gold) < goal):
		quick_print("Main loop")
		maze()

	quick_print("Main loop exited")

quick_print("Raw BFS maze function called")
gold_BFS(num_items(Items.Gold) + 1)