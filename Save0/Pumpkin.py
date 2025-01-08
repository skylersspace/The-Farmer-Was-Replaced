from Utility import *

def plant_pumpkin():
	reset()

	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant(Entities.Pumpkin)
			move(North)
		move(East)

def plant_pumpkin_watered():
	reset()

	for i in range(get_world_size()):
		for j in range(get_world_size()):
			water_check(.33, 1)
			plant(Entities.Pumpkin)
			move(North)
		move(East)

def pumpkin_normal():	
	plant_pumpkin()

	reset()
	count = 0
	isActive = True
	while(isActive):
		for i in range(get_world_size()):
			if not isActive:
					break
			for j in range(get_world_size()):
				if not isActive:
					break
				elif can_harvest():
					count = count + 1
					if (count >= (get_world_size() * get_world_size())):
						harvest()
						isActive = False
				else:
					plant(Entities.Pumpkin)
					count = 0
				move(North)
			move(East)
		
	
def pumpkin_watered():
	plant_pumpkin_watered()
	
	reset()
	count = 0
	isActive = True
	while(isActive):
		for i in range(get_world_size()):
			if not isActive:
					break
			for j in range(get_world_size()):
				if not isActive:
					break
				elif can_harvest():
					count = count + 1
					if (count >= (get_world_size() * get_world_size())):
						harvest()
						isActive = False
				else:
					water_check(.33, 1)
					plant(Entities.Pumpkin)
					count = 0
				move(North)
			move(East)

def pumpkin_map():
	plant_pumpkin()
	
	#Array will switch between the active map, and creating the next map
	field_map = [[],[]]
	
	#Initial Map
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				plant(Entities.Pumpkin)
				field_map[0].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				field_map[0].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest
	count = 0
	while(True):
		#Reset other map
		field_map[(count + 1) % 2] = []
		for i in range(len(field_map[count % 2])):
			move_to(field_map[count % 2][i][0], field_map[count % 2][i][1])
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				plant(Entities.Pumpkin)
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
		
		if (len(field_map[(count + 1) % 2]) == 0):
			harvest()
			break
		count += 1

def pumpkin_map_watered():
	plant_pumpkin_watered()
	
	#Array will switch between the active map, and creating the next map
	field_map = [[],[]]
	
	#Initial Map
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				water_check(.33, 1)
				plant(Entities.Pumpkin)
				field_map[0].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				field_map[0].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest
	count = 0
	while(True):
		#Reset other map
		field_map[(count + 1) % 2] = []
		for i in range(len(field_map[count % 2])):
			move_to(field_map[count % 2][i][0], field_map[count % 2][i][1])
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				water_check(.33, 1)
				plant(Entities.Pumpkin)
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
		
		if (len(field_map[(count + 1) % 2]) == 0):
			harvest()
			break
		count += 1

#WORK IN PROGRESS
def pumpkin_fertilized():
	plant_pumpkin_watered()
	
	reset()
	count = 0
	isActive = True
	while(isActive):
		for i in range(get_world_size()):
			if not isActive:
					break
			for j in range(get_world_size()):
				if not isActive:
					break
				elif can_harvest():
					count = count + 1
					if (count >= (get_world_size() * get_world_size())):
						harvest()
						isActive = False
				elif get_entity_type() == Entities.Pumpkin:
					use_item(Items.Fertilizer)
				else:
					water_check(.33, 1)
					plant(Entities.Pumpkin)
					count = 0
				move(North)
			move(East)

#WORK IN PROGRESS
def pumpkin_map_fertilized():
	plant_pumpkin_watered()
	
	#Array will switch between the active map, and creating the next map
	field_map = [[],[]]
	
	#Initial Map
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				water_check(.33, 1)
				plant(Entities.Pumpkin)
				field_map[0].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				field_map[0].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest
	count = 0
	while(True):
		#Reset other map
		field_map[(count + 1) % 2] = []
		for i in range(len(field_map[count % 2])):
			move_to(field_map[count % 2][i][0], field_map[count % 2][i][1])
			if(not can_harvest() and (get_entity_type() != Entities.Pumpkin)):
				water_check(.33, 1)
				plant(Entities.Pumpkin)
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
			elif(not can_harvest()):
				use_item(Items.Fertilizer)
				field_map[(count + 1) % 2].append((get_pos_x(), get_pos_y()))
		
		if (len(field_map[(count + 1) % 2]) == 0):
			harvest()
			break
		count += 1
