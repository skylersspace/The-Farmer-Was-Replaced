from Utility import *
from Grass import *
from Wood import *
#from Carrot import *

def polyculture(goal, benchmark = False, verbose = False):
    world_size = get_world_size()
    # Polyculture gets the plant's companion, plants, and then harvests when a loop would ocurr.
    #   Provides a multiplier of (5 + unlock level)

    # This algorithm uses a 'single thread' for the polyculture. Advancements would likely involve 'multi thread' polyculture
    def polyculture_normal():
        harvest_list = []

        # Plant list is a multi-dimensional array which tracks if something has been planted at that location
        plant_list = []
        for i in range(world_size):
            plant_list.append([])
            for j in range(world_size):
                plant_list[i].append(True)

        # Next position is random. Will not fill up entire field
        #   Grass is an arbitrary first crop
        #   Return got changed from two elements to a tuple
        #   X = next_crop[1][0], Y = next_crop[1][1]
        next_crop = (Entities.Grass, (0, 0))

        # Continue until all items are above the goal
        start_hay = num_items(Items.Hay)
        start_wood = num_items(Items.Wood)
        start_carrot = num_items(Items.Carrot)

        #Aquiring initial component costs for carrots (25% of world size)
        grass(round(world_size * .25) * num_unlocked(Unlocks.Carrots))
        wood(round(world_size * .25) * num_unlocked(Unlocks.Carrots))
        

        while(num_items(Items.Hay) < (start_hay + goal) or
         num_items(Items.Wood) < (start_wood + goal) or
         num_items(Items.Carrot) < (start_carrot + goal)):
            
            # Plant next companion crop
            if(plant_list[next_crop[1][0]][next_crop[1][1]]): 
                move_to(next_crop[1][0], next_crop[1][1])
                plant(next_crop[0])
                
                # Add planted crop to the harvest list for later
                harvest_list.append((get_pos_x(), get_pos_y()))
                plant_list[get_pos_x()] [get_pos_y()] = False
                next_crop = get_companion()

            # Overlap detected, harvest up to current crop
            #   This will need to vary from other similar methods due to needing last crop to remain intact.
            else:
                # Move the last element to the front, and don't touch it
                harvest_list.insert(0, harvest_list[len(harvest_list) - 1])
                harvest_list.pop()
                while (len(harvest_list) > 1):
                    x_curr = harvest_list[1][0]
                    y_curr = harvest_list[1][1]
                    move_to(x_curr, y_curr)
                    if (can_harvest()):
                        harvest()
                        plant_list[x_curr] [y_curr] = True
                    else:
                        harvest_list.append((x_curr, y_curr))
                    harvest_list.pop(1)

        # Final Harvest
        while (len(harvest_list) > 0):
            x_curr = harvest_list[0][0]
            y_curr = harvest_list[0][1]
            move_to(x_curr, y_curr)
            if (can_harvest()):
                harvest()
            else:
                harvest_list.append((x_curr, y_curr))
            harvest_list.pop(0)

    def polyculture_multi():
        plant_list = []
        for i in range(world_size):
            plant_list.append([])
            for j in range(world_size):
                plant_list[i].append(True)
        
        # Continue until all items are above the goal
        start_hay = num_items(Items.Hay)
        start_wood = num_items(Items.Wood)
        start_carrot = num_items(Items.Carrot)

        #Aquiring initial component costs for carrots (25% of world size)
        grass(round(world_size * .25) * num_unlocked(Unlocks.Carrots))
        wood(round(world_size * .25) * num_unlocked(Unlocks.Carrots))

        # Master list contains the various 'threads' of polyculture
        poly_list = []
        for i in range(world_size):
            #Go to and plant
            move_to(i,0)
            plant(Entities.Carrot)
            #Mark off in plant list
            plant_list[i] [0] = False
            #Add current location to harvest map, and get next plant
            poly_list.append([[(i,0)], get_companion()])
        current = 0

        while(num_items(Items.Hay) < (start_hay + goal) or
         num_items(Items.Wood) < (start_wood + goal) or
         num_items(Items.Carrot) < (start_carrot + goal)):

            #BEGIN THE THREADS

            next_crop = poly_list[current][1]
            
            quick_print (poly_list)
    
    def polyculture_benchmark():
        def run_benchmark(tester):
            clear_tilled()
            reset()
            if verbose:
                quick_print("")
                quick_print(tester[1])
                quick_print("Starting Water:", get_water())
            
            start_hay = num_items(Items.Hay)
            start_wood = num_items(Items.Wood)
            start_carrot = num_items(Items.Carrot)
            start_time = get_time()
            start_ops = get_tick_count()
            
            tester[0]()
            
            ops_used = get_tick_count() - start_ops
            time_elapsed = get_time() - start_time
            hay_produced = num_items(Items.Hay) - start_hay
            wood_produced = num_items(Items.Wood) - start_wood
            carrot_produced = num_items(Items.Carrot) - start_carrot
            items_produced = hay_produced + wood_produced + carrot_produced

            if verbose:

                quick_print("Goal:", goal, "Total Produced:", items_produced)
                quick_print("     Hay Produced:", hay_produced, "Percentage: ", ((hay_produced / items_produced) * 100))
                quick_print("     Wood Produced:", wood_produced, "Percentage: ", ((wood_produced / items_produced) * 100))
                quick_print("     Carrots Produced:", carrot_produced, "Percentage: ", ((carrot_produced / items_produced) * 100))
                quick_print("Time Elapsed:", time_elapsed)
                quick_print("     Items per second:", (items_produced / time_elapsed))
                quick_print("Operations Used:", ops_used)
                quick_print("     Operations per item:", (ops_used / items_produced))
            return (time_elapsed, items_produced, ops_used, items_produced/time_elapsed, ops_used/items_produced)

        func_list = [
                [polyculture_normal, "Normal Polyculture", 0],
                [polyculture_multi, "Threaded Polyculture", 0]
                # [polyculture_water, "Clean Carrots", 0]
            ]
        
        for i in func_list:
            i[2] = run_benchmark(i)

        quick_print("")
        quick_print("-----------------")
        quick_print("Benchmark Results")
        quick_print("-----------------")
        quick_print("Name : Time : Items : Operations: Items/Sec : Ops/Item")
        for i in func_list:
            quick_print(i[1], ":", i[2][0], ":", i[2][1], ":", i[2][2], ":", i[2][3], ":", i[2][4])

    if benchmark:
        #polyculture_benchmark()
        polyculture_multi()
    else:
        if (num_unlocked(Unlocks.Watering) > 0):
            quick_print("")
        else:
            quick_print("")



def polyculture_watered(goal):
    reset()
    water_all()

    harvest_list = []

    plant_list = []
    for i in range(get_world_size()):
        plant_list.append([])
        for j in range(get_world_size()):
            plant_list[i].append(True)

    #Next position is random. Will not fill up entire field
    next_crop = (Entities.Grass, 0, 0)

    start_hay = num_items(Items.Hay)
    start_wood = num_items(Items.Wood)
    start_carrot = num_items(Items.Carrot)

    while(num_items(Items.Hay) < (start_hay + goal) or
          num_items(Items.Wood) < (start_wood + goal) or
          num_items(Items.Carrot) < (start_carrot + goal)):
        
        if(plant_list[next_crop[1]][next_crop[2]]):
            #Plant next companion crop
            move_to(next_crop[1], next_crop[2])
            water_check(.2,1)
            plant(next_crop[0])
            
            harvest_list.append((get_pos_x(), get_pos_y()))
            plant_list[get_pos_x()] [get_pos_y()] = False
            next_crop = get_companion()
        else:
            #Harvest up to current crop
            while(len(harvest_list) > 1):
                move_to(harvest_list[0] [0], harvest_list[0] [1])
                while(not can_harvest()):
                    do_a_flip()
                    #quick_print(get_water())
                harvest()
                plant_list[harvest_list[0] [0]] [harvest_list[0] [1]] = True
                harvest_list.pop(0)  

    #Final Harvest
    final_harvest(harvest_list)

def polyculture_fertilized(goal):
    reset()
    water_all()

    harvest_list = []

    plant_list = []
    for i in range(get_world_size()):
        plant_list.append([])
        for j in range(get_world_size()):
            plant_list[i].append(True)

    #Next position is random. Will not fill up entire field
    next_crop = (Entities.Grass, 0, 0)

    start_hay = num_items(Items.Hay)
    start_wood = num_items(Items.Wood)
    start_carrot = num_items(Items.Carrot)

    while(num_items(Items.Hay) < (start_hay + goal) or
        num_items(Items.Wood) < (start_wood + goal) or
        num_items(Items.Carrot) < (start_carrot + goal)):
        
        if(plant_list[next_crop[1]][next_crop[2]]):
            #Plant next companion crop
            move_to(next_crop[1], next_crop[2])
            water_check(.2,1)
            plant(next_crop[0])
            
            harvest_list.append((get_pos_x(), get_pos_y()))
            plant_list[get_pos_x()] [get_pos_y()] = False
            next_crop = get_companion()
        else:
            #Harvest up to current crop
            buy_fertilizer()
            while(len(harvest_list) > 1):
                move_to(harvest_list[0] [0], harvest_list[0] [1])
                if(not can_harvest()):
                    use_item(Items.Fertilizer)
                    harvest()
                else:
                    harvest()
                plant_list[harvest_list[0] [0]] [harvest_list[0] [1]] = True
                harvest_list.pop(0)  

    #Final Harvest
    final_harvest(harvest_list)