#-------------------------#
#----- Farming Tasks -----#
#-------------------------#

def till_all():
	if (get_ground_type() == Grounds.Grassland):
		for i in range (get_world_size()):
			for j in range (get_world_size()):
				till()
				move(North)
			move(East)

def harvest_all():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			while not can_harvest():
				if get_entity_type() == None:
					break 
				do_a_flip()
			harvest()
			move(North)
		move(East)

def harvest_all_v2():
	harvest_map = []
	#Generate initial map coordinates
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			harvest_map.append((i,j))

	while(len(harvest_map) > 0):
		move_to(harvest_map[0][0], harvest_map[0][1])
		if(can_harvest()):
			harvest()
		#If object can't be harvested, add it to the end of the list to come back later
		elif(get_entity_type() != None):
			harvest_map.append(harvest_map[0])
		#Remove current location in list, harvest or not
		harvest_map.pop(0)

def harvest_all_rev():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			while not can_harvest():
				if get_entity_type() == None:
					break 
				do_a_flip()
			harvest()
			move(South)
		move(West)

def clear_tilled():
	harvest_map = []
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			harvest_map.append((i,j))

	while(len(harvest_map) > 0):
		move_to(harvest_map[0][0], harvest_map[0][1])
		if(can_harvest()):
			harvest()
			if (get_ground_type() == Grounds.Grassland):
				till()
		elif(get_entity_type() != None):
			harvest_map.append(harvest_map[0])
		elif (get_ground_type() == Grounds.Grassland):
			till()
		harvest_map.pop(0)

def clear_turf():
	harvest_map = []
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			harvest_map.append((i,j))

	while(len(harvest_map) > 0):
		move_to(harvest_map[0][0], harvest_map[0][1])
		if(can_harvest()):
			harvest()
			if (get_ground_type() == Grounds.Soil):
				till()
		elif(get_entity_type() != None):
			harvest_map.append(harvest_map[0])
		elif (get_ground_type() == Grounds.Soil):
			till()
		harvest_map.pop(0)

#--------------------#
#----- Movement -----#
#--------------------#

def calc_move(curr, dest):
	movement = ((dest + get_world_size()) - curr) % get_world_size()
	if (movement >= 0 and movement <= (get_world_size()/2)):
		return movement
	else:
		movement = ((curr + get_world_size()) - dest) % (get_world_size()/2)
		movement *= -1
		return movement

def move_x(x):
	x_move = calc_move(get_pos_x(), x)
	while (x_move != 0):
		if x_move > 0:
			move(East)
			x_move -= 1
		else:
			move(West)
			x_move += 1

def move_y(y):
	y_move = calc_move(get_pos_y(), y)
	while (y_move != 0):
		if y_move > 0:
			move(North)
			y_move -= 1
		else:
			move(South)
			y_move += 1
	
def move_to(x, y):
	move_x (x)
	move_y(y)
			
def reset():
	move_to(0, 0)

#-----------------#
#----- Water -----#
#-----------------#

def water_check(minimum, maximum):
	if get_water() < minimum:
		while get_water() < maximum:
			use_item(Items.Water)

def water_all():	#Create overflow method with min/max?
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			water_check(.8, 1)
			move(North)
		move(East)

def buy_fertilizer():
	if (num_items(Items.Fertilizer) < get_world_size() * get_world_size()):
		trade(Items.Fertilizer, (get_world_size() * get_world_size()) - num_items(Items.Fertilizer))

#-------------------#
#----- Sorting -----#
#-------------------#

def merge_sort(sort_list):
	if(len(sort_list) > 1):
		mid = len(sort_list) // 2
		left = sort_list[:mid]
		right = sort_list[mid:]

		merge_sort(left)
		merge_sort(right)

		i = 0
		j = 0
		k = 0

		while((i < len(left)) and (j < len(right))):
			if(left[i] < right[j]):
				sort_list[k] = left[i]
				i += 1
			else:
				sort_list[k] = right[j]
				j += 1
			k += 1
		
		while i < len(left):
			sort_list[k] = left[i]
			i += 1
			k += 1

		while j < len(right):
			sort_list[k] = right[j]
			j += 1
			k += 1

def bubble_sort(sort_list):
	n = len(sort_list)
	for i in range(n-1):
		for j in range(0, n-i-1):
			if sort_list[j] > sort_list[j+1]:
				sort_list[j], sort_list[j+1] = sort_list[j+1], sort_list[j]

#-------------------#
#----- Logical -----#
#-------------------#

def XOR(a, b):
	return a != b

#------------------------#
#----- Mathematical -----#
#------------------------#

def pow(number, exponent):
# Only supports 'unsigned' integers
	# a^(b + c) = a^b * a^c
	# a^(2b) = a^b * a^b = (a^b)^2
	if exponent == 0:
		return 1

	result = pow (number, (exponent // 2))

	if exponent % 2:
		return result * result * number
	else:
		return result * result

def round(number):
	remainder = number % 1
	if remainder == 0:
		return number
	elif remainder > .5:
		return ((number // 1) + 1)
	else:
		return (number // 1)

def ceil(number):
	if number % 1 == 0:
		return number
	else:
		return ((number // 1) + 1)

def floor(number):
	return (number // 1)

#-------------------#
#----- Mapping -----#
#-------------------#

def on_grid():
	x = get_pos_x()
	y = get_pos_y()
	if ((x % 2) == 0):
		if ((y % 2) == 0):
			return True
	else:
		if ((y % 2) == 1):
			return True
	return False

def map():
	reset()

	map_list = []

	for i in range (get_world_size()):
		map_list.append([])
		for j in range (get_world_size()):
			map_list[i].append((get_entity_type(), measure(), get_water(), get_ground_type(), get_pos_x(), get_pos_y()))
			move(North)
		move(East)
	
	return map_list

def map_v2():
	reset()

	map_list = []

	#Determine number of passes required
	passes = 0
	if ((get_world_size() % 3) != 0):
		passes = get_world_size() // 3 + 1
	else:
		passes = get_world_size() // 3

	for i in range (passes):
		#Get position to determine what type of pass is needed
		remains = get_world_size() - get_pos_x()
		if ((remains / 3) >= 1):
			move(East)
			x = get_pos_x()
			#quick_print("Triple Scan", x)
			map_list.append([])
			map_list.append([])
			map_list.append([])
			for j in range (get_world_size()):
				map_list[x-1].append((get_entity_type(), measure(), get_water(), get_ground_type(), x-1, get_pos_y()))
				map_list[x].append((get_entity_type(), measure(), get_water(), get_ground_type(), x, get_pos_y()))
				map_list[x+1].append((get_entity_type(), measure(), get_water(), get_ground_type(), x+1, get_pos_y()))
				move(North)
			move(East)
			move(East)
		elif ((remains % 3) == 2):
			x = get_pos_x()
			#quick_print("Double Scan", x)
			map_list.append([])
			map_list.append([])
			for j in range (get_world_size()):
				map_list[x].append((get_entity_type(), measure(), get_water(), get_ground_type(), x, get_pos_y()))
				map_list[x+1].append((get_entity_type(), measure(), get_water(), get_ground_type(), x+1, get_pos_y()))
				move(North)
			move(East)
			move(East)
		else:
			x = get_pos_x()
			#quick_print("Single Scan", x)
			map_list.append([])
			for j in range (get_world_size()):
				map_list[x].append((get_entity_type(), measure(), get_water(), get_ground_type(), x, get_pos_y()))
				move(North)
			move(East)

	return map_list

def swap_x(x, map):	#Map option is to update the map as object is moved
	quick_print(x - get_pos_x())
	quick_print(abs(x) * (1/x))
	for i in range(abs(x)):
		quick_print(i)

def swap_y(y, map):	# Same as above
	quick_print(y - get_pos_y())

def swap_to(x,y,map): #Same as above, but for both x and y
	swap_x(x,map)
	swap_y(y,map)