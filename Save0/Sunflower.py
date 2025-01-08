from Utility import *

def flowers_plant():
	reset()
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			plant(Entities.Sunflower)
			move(North)
		move(East)
		
def flowers_plant_water():
	reset()
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			water_check(.29,1)
			plant(Entities.Sunflower)
			move(North)
		move(East)

def flowers_harvest():
	#Create a key for each petal count which is assigned an empty array
	#This array will store the xy location of the flower
	#Petal count ranges from 7 - 15
	sun_power_loc = dict()
	for i in range(7,15+1):
		sun_power_loc[i] = []
	
	#Map out the flower petal locations
	reset()
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			if measure() != None:
				sun_power_loc[measure()].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest all the flowers
	for i in range(15, 7-1, -1):
		for j in sun_power_loc[i]:
			move_to(j[0], j[1])
			while not can_harvest():
				#quick_print(get_water())
				do_a_flip()
			harvest()

def flowers_harvest_v2():
	#Create a key for each petal count which is assigned an empty array
	#This array will store the xy location of the flower
	#Petal count ranges from 7 - 15
	sun_power_loc = dict()
	for i in range(7,15+1):
		sun_power_loc[i] = []
	
	reset()
	#Plant and map out the flower petal locations
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			plant(Entities.Sunflower)
			sun_power_loc[measure()].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest all the flowers
	for i in range(15, 7-1, -1):
		for j in sun_power_loc[i]:
			move_to(j[0], j[1])
			while not can_harvest():
				#quick_print(get_water())
				do_a_flip()
			harvest()
			
def flowers_harvest_v2_watered():
	#Create a key for each petal count which is assigned an empty array
	#This array will store the xy location of the flower
	#Petal count ranges from 7 - 15
	sun_power_loc = dict()
	for i in range(7,15+1):
		sun_power_loc[i] = []
	
	reset()
	#Plant and map out the flower petal locations
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			water_check(.29,1)
			plant(Entities.Sunflower)
			sun_power_loc[measure()].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest all the flowers
	for i in range(15, 7-1, -1):
		for j in sun_power_loc[i]:
			move_to(j[0], j[1])
			while not can_harvest():
				#quick_print(get_water())
				do_a_flip()
			harvest()
			
def flowers_fertilized():
	#Create a key for each petal count which is assigned an empty array
	#This array will store the xy location of the flower
	#Petal count ranges from 7 - 15
	sun_power_loc = dict()
	for i in range(7,15+1):
		sun_power_loc[i] = []
	
	reset()
	buy_fertilizer()

	#Plant and map out the flower petal locations
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			water_check(.29,1)
			plant(Entities.Sunflower)
			sun_power_loc[measure()].append((get_pos_x(), get_pos_y()))
			move(North)
		move(East)

	#Harvest all the flowers
	for i in range(15, 7-1, -1):
		for j in sun_power_loc[i]:
			move_to(j[0], j[1])
			if (not can_harvest()):
				use_item(Items.Fertilizer)
				use_item(Items.Water)
			harvest()