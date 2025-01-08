# ------------------------------
# GROW TIME DICTIONARY
# ------------------------------
grow_time = dict()
# The amount of time required for a plant to grow. Key: (Min, Max)
grow_time[Entities.Grass] =     (0.5,   0.5)
grow_time[Entities.Bush] =      (3.2,   4.8)
grow_time[Entities.Carrot] =   (4.8,   7.2)
grow_time[Entities.Tree] =      (5.6,   8.4)
grow_time[Entities.Pumpkin] =   (0.2,   3.8)
grow_time[Entities.Cactus] =    (0.9,   1.1)
grow_time[Entities.Sunflower] = (4.0,   6.0)
grow_time[Entities.Dinosaur] =  (0.18,  0.22)
#Treasure and Hedges are not a part of this

#Example to get the minimum grow time for a bush
#quick_print(grow_time[Entities.Bush][0])

# ------------------------------
# COST DICTIONARY
# ------------------------------
def convert_cost(entry):
    entry_list = []
    for i in entry:
        entry_list.append((i,entry[i]))

    return entry_list

item_cost = dict()
item_cost[Items.Fertilizer] = [convert_cost(get_cost(Items.Fertilizer))]
#Seeds have been removed, need to reassess their cost here if even needed

#Example to get the first item for the cost of the carrot seed
#quick_print(item_cost[Items.Carrot_Seed][0][0][0])

# ------------------------------
# CROP FUNCTION DICTIONARY
# ------------------------------
crop_func = dict()
crop_func[Items.Hay] = hay_farmer
crop_func[Items.Wood] = hay_farmer
crop_func[Items.Pumpkin] = hay_farmer
crop_func[Items.Carrot] = hay_farmer
crop_func[Items.Power] = hay_farmer
crop_func[Items.Cactus] = hay_farmer
crop_func[Items.Bone] = hay_farmer



#Maze Mapping
#Better Cactus
#Dinosaurs

# ------------------------------
# REPLACE THE FARMER
# ------------------------------
def replace_the_farmer():
    timed_reset()

    upgrade_path = []
    #Set the upgrade path
    for i in list(Unlocks):
        #I am operating under the assumption that initially, everything which is already unlocked is maxed out.
        if num_unlocked(i) == 0:
            #Add upgrade item, and it's next cost
            upgrade_path.append((i, convert_cost(get_cost(i))))
    
    for i in upgrade_path:
        quick_print(i)
    
    #Identify unlock to pursue
    #


        

# ------------------------------
# REPLACE THE FARMER - 100%
# ------------------------------
def completely_replace_the_farmer():
    timed_reset()

replace_the_farmer()
