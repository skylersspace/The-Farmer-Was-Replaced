from Utility import *

def final_harvest(harvest_list):
    while(len(harvest_list) > 0):
        move_to(harvest_list[0] [0], harvest_list[0] [1])
        while(not can_harvest()):
            do_a_flip()
        harvest()
        harvest_list.pop(0)

def polyculture_normal(goal):
    reset()

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
                harvest()
                plant_list[harvest_list[0] [0]] [harvest_list[0] [1]] = True
                harvest_list.pop(0)  

    #Final Harvest
    final_harvest(harvest_list)

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