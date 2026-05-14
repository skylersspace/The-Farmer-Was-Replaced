from Utility import *

def bone(goal):
	WORLD_SIZE = get_world_size()
	FIELD_SIZE = WORLD_SIZE ** 2

	def print_map(map_list):
		quick_print("Zig, World Size:", WORLD_SIZE, WORLD_SIZE ** 2)
		quick_print("")
		temp = gen_zig_list()
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				quick_print(i, j, temp[i][j])
			quick_print("")

	# Return new coordinates, set 'jump_list' dir to 1 and None
	def gen_point(main_list, coord, dir, index):
		main_list[coord[0]][coord[1]][0][dir] = 1
		main_list[coord[0]][coord[1]][1] = index
		
		if (dir == 0):
			# North
			new_coord = (coord[0], coord[1] + 1)
			main_list[new_coord[0]][new_coord[1]][0][(dir + 2) % 4] = None
			return new_coord
		elif (dir == 1):
			# East
			new_coord = (coord[0] + 1, coord[1])
			main_list[new_coord[0]][new_coord[1]][0][(dir + 2) % 4] = None
			return new_coord
		elif (dir == 2):
			# South
			new_coord = (coord[0], coord[1] - 1)
			main_list[new_coord[0]][new_coord[1]][0][(dir + 2) % 4] = None
			return new_coord
		elif (dir == 3):
			# West
			new_coord = (coord[0] - 1, coord[1])
			main_list[new_coord[0]][new_coord[1]][0][(dir + 2) % 4] = None
			return new_coord
		
	def gen_coord_list(x, y):
		return [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
	
	def find_adjacent(main_list):
		# main_list[x][y] == ([jump_north, jump_east, jump_south, jump_west], index)
		# coord == (x, y)
		
		# Go around the edges first
		for i in range(WORLD_SIZE):
			#Bottom
			main_list[i][0][0][2] = None
			#Top
			main_list[i][WORLD_SIZE - 1][0][0] = None
			#Left
			main_list[0][i][0][3] = None
			#Right
			main_list[WORLD_SIZE - 1][i][0][1] = None

		# Calculate the rest
		for i in range(WORLD_SIZE):
			for j in range(WORLD_SIZE):
				# Only alternating squares need to be calculated
				if on_grid_manual(i,j):
					index_1 = main_list[i][j][1]
					coord_list = gen_coord_list(i, j)
					jump_list = main_list[i][j][0]

					for k in range(4):
						# If unnassigned, continue
						if (jump_list[k] == -1):
							index_2 = main_list[coord_list[k][0]][coord_list[k][1]][1]
							value = index_2 - index_1
							if (value < 0):
								value += FIELD_SIZE
							main_list[i][j][0][k] = value
							value = (WORLD_SIZE ** 2) - value
							main_list[coord_list[k][0]][coord_list[k][1]][0][(k + 2) % 4] = value

	def gen_zig_list():
		# PSEUDO OBJECT EXPLINATION
		# path_list[x][y] == ([jump_north, jump_east, jump_south, jump_west], index)
		# Due to the limitations of this puzzle language, I am unable to create proper objects. This is an approximation of an object.
		# The objects would still be stored in a 2D array for easy location based access (or a similarly structured object)
		# Jump List stores four values for the four cardinal directions. North, East, South, West. 'None' indicates movement is never possible. This can be due to edges, or going backwards. The next step will always be a '1'. A '-1' value means nothing has been assigned yet, and is an illegal value.
		# Index is index number for the path. Jump list values are calculated by comparing the index. The target will be identified by it's index on the path. 'None' means nothing has been assigned and is an illegal value.

		# Generate adjacent tracker list
		zag_list = []
		for i in range(WORLD_SIZE):
			zag_list.append([])
			for j in range(WORLD_SIZE):
				zag_list[i].append([[-1, -1, -1, -1], None])

		# Starting point
		curr_point = (0, 0)
		index = -1
		dir = 0
		zag_list[curr_point[0]][curr_point[1]] = [[None, 1, None, None], 0]
		
		# Immediately move east
		index += 1
		curr_point = gen_point (zag_list, curr_point, 1, index)

		# Begin zig zag in reduced grid, moving north
		for i in range(1, WORLD_SIZE - 1):
			for j in range(WORLD_SIZE - 2):
				index += 1
				curr_point = gen_point (zag_list, curr_point, dir, index)

			#Move east and flip direction3
			index += 1
			curr_point = gen_point (zag_list, curr_point, 1, index)

			dir = (dir + 2) % 4
		
		# Loop around
		# Move North
		for i in range(1, WORLD_SIZE):
			index += 1
			curr_point = gen_point (zag_list, curr_point, 0, index)

		# Move West
		for i in range (WORLD_SIZE - 1, 0, -1):
			index += 1
			curr_point = gen_point (zag_list, curr_point, 3, index)
		
		# Move South
		for i in range(WORLD_SIZE - 1, 1, -1):
			index += 1
			curr_point = gen_point (zag_list, curr_point, 2, index)

		zag_list[0][1][1] = (WORLD_SIZE ** 2) - 1
		zag_list[0][1][0][2] = 1

		find_adjacent(zag_list)

		return zag_list
		
	def hilbert():
		quick_print("Hilbert")

	def gen_test_point():
		return ((random() * WORLD_SIZE) // 1, (random() * WORLD_SIZE) // 1)

	def snake(snake_path):
		reset()
		change_hat(Hats.Brown_Hat)
		#quick_print ("World Size", WORLD_SIZE, "Field size", FIELD_SIZE)

		
		# snake_length could possibly be replaced by len(jump_list) ?
		snake_length = 0
		goal_distance = None
		jump_list = []
		available_space = FIELD_SIZE - snake_length
		BUFFER_EXPONENT = 4
		buffer = None
		target = None
		jump_values = None

		# I THINK IT IS TRYING TO MOVE INTO ITSELF, TRYING TO DOUBLE BACK
		illegal_move = [False, False, False, False]

		move_dir = dict()
		move_dir[0] = North
		move_dir[1] = East
		move_dir[2] = South
		move_dir[3] = West

		change_hat(Hats.Dinosaur_Hat)

		while snake_length < (FIELD_SIZE - 1):
			target = measure()
			if (target == None):
				#quick_print("Endning run")
				break
			#jump_list.insert(0, 0)
			jump_list.append(1)
			available_space -= 1
			snake_length += 1
			for i in range (4):
				if snake_path[get_pos_x()][get_pos_y()][0][i] == 1:
					move(move_dir[i])
					
			
			#quick_print("")
			#quick_print("Target:", target, "Current Postion:", get_pos_x(), get_pos_y(), "Snake Length:", snake_length, "Buffer", buffer, "Target Index", snake_path[target[0]][target[1]][1], "Current Index", snake_path[get_pos_x()][get_pos_y()][1],)
			goal_distance = snake_path[target[0]][target[1]][1] - snake_path[get_pos_x()][get_pos_y()][1]
			if goal_distance < 0:
				goal_distance += FIELD_SIZE
			#quick_print("Goal distance:", goal_distance)

			# Calculate and move to target
			while goal_distance > 0:
				# Calculate move
				jump_values = snake_path[get_pos_x()][get_pos_y()][0]
				buffer = (((1 - (snake_length / FIELD_SIZE)) ** BUFFER_EXPONENT * FIELD_SIZE) + 1) // 1
				max_jump = None

				# Find jump value
				for i in range(4):
					curr_jump = jump_values[i]
					
					if illegal_move[i] == True:
						continue
					# Check for valid jump direction
					if (curr_jump == None):
						illegal_move[i] = True
						continue
					# Don't overshoot target
					if (curr_jump > goal_distance):
						continue
					# Buffer check
					if (curr_jump > buffer):
						continue
					# There's enough space for the jump
					if (curr_jump > available_space):
						continue
					# First valid or better direction found
					if (max_jump == None) or (curr_jump > jump_values[max_jump]):
						max_jump = i

				# Successful Move
				if (move(move_dir[max_jump])):
					jump_list.append(jump_values[max_jump])
					available_space -= jump_values[max_jump]
					goal_distance -= jump_values[max_jump]
					#quick_print("Moving", move_dir[max_jump], "Jumping", jump_values[max_jump], "Goal Distance:", goal_distance, "Current Postion:", get_pos_x(), get_pos_y())
					available_space += jump_list[0]
					jump_list.pop(0)
					illegal_move = [False, False, False, False]
				# Move failed
				else:
					illegal_move[max_jump] = True
					#quick_print (illegal_move)
					# IF ALL ARE TRUE, THEN SNAKE IS STUCK AND CANNOT CONTINUE. THIS IS A BUG IF THIS OCURRS
					if illegal_move[0] and illegal_move[1] and illegal_move[2] and illegal_move[3]:
						change_hat(Hats.Brown_Hat)
						quick_print("ERROR: Early harvest")
					break

		change_hat(Hats.Brown_Hat)
	
	move_map = gen_zig_list()
	while (num_items(Items.Bone) < goal):
		snake(move_map)