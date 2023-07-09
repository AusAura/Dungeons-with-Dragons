## Dungeons with Dragons

from random import randint, choice
from pathlib import Path

PATH = Path('.') # save path

objects_list = [{'type': 'player', 'char_sign': 'X', 'number': 1, 'movable': 1}, # obj types
           {'type': 'enemy', 'char_sign': 'E', 'number': 5, 'movable': 1},
           {'type': 'exit', 'char_sign': 'O', 'number': 1, 'movable': 0}]


def load(PATH=PATH) -> tuple:

    generated_objects = []
    with open(PATH / 'save.txt', 'r') as file:

        for i, line in enumerate(file):
            if i == 0:
                SIZE_X, SIZE_Y, turns = line.strip().split(' ')
            else:
                line_list = line.strip().split()
                generated_objects.append({'type': line_list[0], 
                                      'char_sign': line_list[1], 
                                      'X': int(line_list[2]),
                                      'Y': int(line_list[3]),
                                      'movable': int(line_list[4])})

    return generated_objects, int(SIZE_X), int(SIZE_Y), int(turns)


while True: 

    try:
        is_load = input('Do you want to load the game? (Y or N): ').casefold() # loading the game?

        if is_load != 'y' and is_load != 'n': # wrong symbol?
            raise ValueError
        
        if is_load == 'n':
            turns = 0
            SIZE_X = randint(5, 10) # if not - generate random map size
            SIZE_Y = randint(5, 10)
            print(SIZE_X)

    except:
        print('I do not understand!')
    else:
        break

if is_load == 'y': 
    generated_objects, SIZE_X, SIZE_Y, turns = load() # if Y load - restore data

## Sizes should be defined above this line or map will not generate correctly


def check_state(generated_objects: list) -> int:

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

    return end_flag


def generate_objects(objects_list: list, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) -> list:
    generated_objects = []

    for obj in objects_list:
        i = 0
        while obj['number'] > i:
            generated_objects.append({'type': obj['type'], 
                                      'char_sign': obj['char_sign'], 
                                      'X': randint(0, SIZE_X - 1),
                                      'Y': randint(0, SIZE_Y - 1),
                                      'movable': obj['movable']})
            i += 1
    return generated_objects


def map_generate(generated_objects: list, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) -> list:
    
    world_map = []

    for y in range(0, SIZE_Y):

        row = []

        for x in range(0, SIZE_X):

            row.append(' ')

        world_map.append(row)

    for obj in generated_objects:
        X = obj['X']
        Y = obj['Y']
        world_map[Y][X] = obj['char_sign']       

    return world_map


def move(direction: str, obj: dict, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y) -> None:

    if direction == 'u' and obj['Y'] > 0:
        obj['Y'] -= 1
    elif direction == 'd' and obj['Y'] < SIZE_Y - 1:
        obj['Y'] += 1
    elif direction == 'l' and obj['X'] > 0:
        obj['X'] -= 1
    elif direction == 'r' and obj['X'] < SIZE_X - 1:
        obj['X'] += 1
    else:
        print(f'{obj["type"].upper()} is staing in place!')
    # moves


def print_map(world_map: list) -> None:
    
    for row in world_map:
        print(f'|{"|".join(row)}|')


def save(generated_objects: list,  turns: int, SIZE_X=SIZE_X, SIZE_Y=SIZE_Y, PATH=PATH) -> None:

    with open(PATH / 'save.txt', 'w') as file:
        file.write(' '.join([str(SIZE_X), str(SIZE_Y), str(turns), '\n'])) # sizes and turns

        # OBJs
        for obj in generated_objects:
            obj_val_dict = obj.values() 
            obj_val_list = list(obj_val_dict)

            # serialize to str
            obj_val_list[2] = str(obj_val_list[2])
            obj_val_list[3] = str(obj_val_list[3])
            obj_val_list[4] = str(obj_val_list[4])

            obj_str = ' '.join(obj_val_list)
            obj_str += '\n'
            file.write(obj_str)


if is_load == 'n':
    generated_objects = generate_objects(objects_list) # if N load - generate objs
    print(generated_objects)


# GAME START
while True:

    end_flag = check_state(generated_objects) # is game over?

    if end_flag:       
        break           

    for obj in generated_objects:
        if obj['type'] == 'player':
            direction = input('Please make your move (u/d/l/r): ') # move input 4 objects
        elif obj['type'] == 'enemy':
            direction = choice('lrud')
    
        if obj['movable']: 
            move(direction, obj) # moving objects

    turns += 1
    save(generated_objects, turns) # saving every turn

# GAME END
print('The game is over!')