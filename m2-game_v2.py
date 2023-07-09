## Dungeons with Dragons

from random import randint, choice

SIZE_X = randint(5, 10)
SIZE_Y = randint(5, 10)


def check_state(generated_objects):

    end_flag = 0
    player_coordinates = []

    for obj in generated_objects:

        if obj['type'] == 'player':
            player_coordinates.append([obj['X'], obj['Y']])
        elif obj['type'] == 'enemy':
            if [obj['X'], obj['Y']] in player_coordinates:
                end_flag = 2
                obj['char_sign'] = 'L'      
                world_map = map_generate(generated_objects, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) # map render       
                print_map(world_map)           
                print(f'You LOST in {turns} turns!!!')      
                return end_flag                    
        elif obj['type'] == 'exit':
            if [obj['X'], obj['Y']] in player_coordinates:
                end_flag = 1
                obj['char_sign'] = 'W'
                world_map = map_generate(generated_objects, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) # map render  
                print_map(world_map)             
                print(f'You WON in {turns} turns!!!')  
                return end_flag

    world_map = map_generate(generated_objects, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) # map render       
    print_map(world_map)                             

    # if char_X == exit_X and char_Y == exit_Y:
    #     end_flag = 1
    # elif char_X == enemy_X and char_Y == enemy_Y:
    #     end_flag = 2        

    return end_flag


def generate_objects(objects_list, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y):
    generated_objects = []

    for obj in objects_list:
        i = 0
        while obj['number'] > i:
            generated_objects.append({'type': obj['type'], 
                                      'char_sign': obj['char_sign'], 
                                      'X': randint(0, SIZE_X - 1),
                                      'Y': randint(0, SIZE_Y - 1),
                                      'movable': obj['movable']})
            i += i + 1
    return generated_objects


def map_generate(generated_objects, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y):
    
    world_map = []

    for y in range(0, SIZE_Y):

        row = []

        for x in range(0, SIZE_X):

            row.append(' ')

        # row.append(' |')
        world_map.append(row)

    for obj in generated_objects:
        X = obj['X']
        Y = obj['Y']
        world_map[Y][X] = obj['char_sign']       

    return world_map



def move(direction, obj, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y):

    if direction == 'u' and obj['Y'] > 0:
        obj['Y'] -= 1
    elif direction == 'd' and obj['Y'] < SIZE_Y - 1:
        obj['Y'] += 1
    elif direction == 'l' and obj['X'] > 0:
        obj['X'] -= 1
    elif direction == 'r' and obj['X'] < SIZE_X - 1:
        obj['X'] += 1
    else:
        print('You are staing in place!')
    # moves


def print_map(world_map):
    
    for row in world_map:
        print(f'|{"|".join(row)}')

# def calculate_total_obj_number(objects_list):

#     object_total_number = 0
#     for item in objects_list:
#         object_total_number += item['number']
#     return object_total_number



objects_list = [{'type': 'player', 'char_sign': 'X', 'number': 1, 'movable': 1},
           {'type': 'enemy', 'char_sign': 'E', 'number': 1, 'movable': 1},
           {'type': 'exit', 'char_sign': 'O', 'number': 1, 'movable': 0}]

# object_total_number = calculate_total_obj_number(objects_list)

generated_objects = generate_objects(objects_list)
print(generated_objects)
# input('stop')
turns = 0

while True:

    end_flag = check_state(generated_objects)

    if end_flag:       
        break           

    for obj in generated_objects:
        if obj['type'] == 'player':
            direction = input('Please make your move (u/d/l/r): ')
        elif obj['type'] == 'enemy':
            direction = choice('lrud')
    
        
        if obj['movable']: 
            move(direction, obj)


    turns += 1

print('The game is over!')