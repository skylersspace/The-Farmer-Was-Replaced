#sInventory = {"cSeeds":num_items(Items.Carrot_Seed),
	#"pSeeds":num_items(Items.Pumpkin_Seed),
	#"sSeeds":num_items(Items.Sunflower_Seed)}

#mInventory = {"eWater":num_items(Items.Empty_Tank),
	#"fWater":num_items(Items.Water_Tank),
	#"Fertilizer":num_items(Items.Fertilizer)}

#def get_priority():
#print (cInventory["Hay"])
#print (min(cInventory[0], cInventory[2]))

def get_lowest():
	#0: Hay, 1: Wood, 2: Carrot, 3: Pumpkin, 4: Gold, 5: Power
	cInventory = [num_items(Items.Hay),
		num_items(Items.Wood),
		num_items(Items.Carrot),
		num_items(Items.Pumpkin),
		num_items(Items.Gold),
		num_items(Items.Power)]
		#num_items(Items.Cactus)
		
	minimum = 0
	for i in range(len(cInventory)):
		if (cInventory[minimum] <= cInventory[i]):
			continue
		else:
			minimum = i
	return minimum
	quick_print(minimum)
	
get_lowest()