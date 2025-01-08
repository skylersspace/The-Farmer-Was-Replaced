from Utility import *

def plant_carrot_all():
	reset()
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			harvest()
			plant(Entities.Carrot)
			move(North)
		move(East)

#VERSION 1
def carrot_all():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			if can_harvest():
				harvest()
				plant(Entities.Carrot)
			move(North)
		move(East)

#VERSION 2 - SLOWEST
def carrot_all_wait():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			while not can_harvest():
				do_a_flip()
			harvest()
			plant(Entities.Carrot)
			move(North)
		move(East)

#VERSION 3 - FASTEST
def carrot_all_water():
	for i in range (get_world_size()):
		for j in range (get_world_size()):
			while not can_harvest():
				quick_print(get_water())
				do_a_flip()
			harvest()
			water_check(.22, 1)
			plant(Entities.Carrot)
			move(North)
		move(East)
		
#Fertilizer is not necessary for this crop
		
def farm_x_Carrot(number):
	till_all()
	reset()
	
	water_all()
	plant_carrot_all()
	
	start_num = num_items(Items.Carrot)
	while (num_items(Items.Carrot) < (start_num + number)):
		carrot_all_water()
	harvest_all()
	
def farm_to_x_Carrot(number):
	till_all()
	reset()
	
	water_all()
	plant_carrot_all()
	
	while (num_items(Items.Carrot) < number):
		carrot_all_water()
	harvest_all()

	quick_print ("Carrot")