# -*-coding:UTF8 ISO-8859-1 -*
import os
import json
import sys
import matplotlib.pyplot as plt # 2D plotting library
import numpy as np

def info_directory (path) :
    '''
        It'll look for information in each file in the path :
            - Extensions ;
            - Quantity of extensions ;
    '''
    for root, dirs, files in os.walk(path, topdown=False):
        categories = []
        if files != '' : # Are there files in the directory ?
            list_of_categories = {}
            for name in files:
                file_extension = os.path.splitext(name)[1] # extension of the file
                # counts number of files extensions.
                if (file_extension in list_of_categories.keys()):
                    list_of_categories[file_extension] += 1
                else :
                    list_of_categories[file_extension] = 1
            # on formate le retour en json
            for cat in list_of_categories.items() :
                categories += [{"format": cat[0], "nombre":cat[1]}]
        return (categories)

def JSON_files_join (path):
    '''
        It'll look for JSON files recursively from .
        It returns a join of all JSON files.
    '''
    JSON_files_join = []
    for root, dirs, files in os.walk(path, topdown=False):
        if files != '' : # y a t-il des fichiers dans le dossier ?
            for name in files:
                file_extension = os.path.splitext(name)[1] # extension du nom
                if (file_extension.upper() == ".JSON"):
                    with open(os.path.join(root, name), 'r', encoding='utf-8') as f:
                        JSON_files_join += [json.load(f)]
    return (JSON_files_join)
    
        
def types_split (directory_name) :
    '''
        It splits the name of the directory to deduct multiple types.
        By convention, the name respects a structure.
    '''
    pre_defined_types = ['bat', 'vampire', 'wolf']
    split_name = directory_name.split("_")
    types = []
    for word in split_name :
        if word in pre_defined_types :
            types.append(word)
    return (types)
        
def decomposition_lieu (directory_name) :
    '''
        It splits the name of the directory to deduct the place.
        By convention, the name respects a structure.
    '''
    pre_defined_types = ['CVM', 'Alex']
    split_name = directory_name.split("_")
    types = []
    for word in split_name :
        if word in pre_defined_types :
            types.append(word)
    return (types)

def generator_of_general_structure_JSON_file (directory_name) :
    '''
        It creates a general structure of the JSON file.
        It usually uses :
            - the name of the directory to deduct the absolute path ;
            - the name of the directory to deduct the types of files contained ;
            - the name of the directory to deduct the place where photos were taken ;
            - the name of the directory to deduct the date when photos were taken ;
    '''
    JSON_file = {"chemin_du_dossier": os.path.join(os.getcwd(), directory_name), \
                "type" : types_split(directory_name),\
                "lieu" : decomposition_lieu(directory_name),\
                "categories" : []}
    return (JSON_file)

def recursive_search_and_JSON_file_generator (path, overwrite):
    '''
        It will do a recursive search of directories & create automatically JSON files which contain
        details of the files in the directory.
        The option overwrite enables to delete and then write on existing files.
        overwrite != 0 <=> existing files will be overwritten.
    '''
    for root, dirs, files in os.walk(path):
        for name in dirs:
            data = generator_of_general_structure_JSON_file(name)
            data["categories"] = info_directory (os.path.join(root, name))
            # write on file if does not exist or overwrite option
            if (overwrite or not(os.path.exists(os.path.join(root, name,"data.json")))) :
                with open(os.path.join(root, name,"data.json"), 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

def get_number_of_images_in_categories (JSON_categories) :
    '''
        It returns the number of 'format' of images from a JSON of categories
    '''
    list_of_images_format = ['.PNG', '.JPG']
    total_of_images = 0
    for i in range(len(JSON_categories)):
        if JSON_categories[i]["format"].upper() in list_of_images_format:
            total_of_images += JSON_categories[i]["nombre"]
    return (total_of_images)

def JSON_categories_plot (JSON_file):
    '''
        Print a bar plot with classes. Each class is the place where the photos where shot.
        For each class, we plot the number of photos by type.
    '''
    info = dict()
    types = []
    places = []

    # Get all the types and places of the data
    for desc in JSON_file :
        types += desc.get('type')
        places += desc.get('lieu')

    types = list(set(types))
    places = list(set(places))

    # Initialize the dictionnary info to items which each key is a place and his value a dict {}
    for place in places:
        info[place] = dict()

    # For each place in the dictionnary info, we initialize to 0 the number of types.
    for place in places:
        info[place] = np.zeros(len(types))

    # We try to find the number of types to add to the dic info (for each place and for each type).
    for desc in JSON_file :
        types_found, places_found, number_of_images = [], [], 0
        for details in desc.items() :
            if (isinstance(details[1], list)):
                if (details[0] == 'type'):                
                    types_found = details[1]
                elif (details[0] == 'lieu'):                
                    places_found = details[1]
                elif (details[0] == 'categories'):                
                    number_of_images = get_number_of_images_in_categories(details[1])
                else:
                    pass 
        for place in places_found:
            for type in types_found:
                info[place][types.index(type)] += number_of_images

    # Compute the total of each types for each place
    tableau = []
    for index_type in range(len(types)):
        sum = 0
        for place in places:
            sum += info[place][index_type]
        tableau += [sum] # ajout d'une somme
    info["TOTAL"] = tableau
    places += ["TOTAL"]

    print (info)

    width = 0.2  # the width of the bars
    x = np.arange(len(types))  # the label locations
    fig, ax = plt.subplots()
    rects = []
    placement = - width*(len(places) - 1)/2
    for i in range(len(places)):
        rects += [ax.bar(x + placement, info[places[i]], width, label=places[i])]
        ax.bar_label(rects[(len(rects)-1)], padding=3)
        placement += width

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of images')
    ax.set_title('Number of images divised by location and sub-divised by type')
    ax.set_xticks(x)
    ax.set_xticklabels(types)
    ax.legend()
    fig.tight_layout()
    plt.show()

def print_menu () :
    '''
        It prints the menu.
    '''
    print ("""\n\n Menu. Please, make a choice (or a sequence of choices).
                    \t1 - create JSON files which contain info for each directory found recursively from . (overwrite existing JSON files)
                    \t2 - create JSON files which contain info for each directory found recursively from . (if it does not already exist) 
                    \t3 - get all JSON files found recursively from .
                    \t4 - plot statistics from the JSON files.
                    \t5 - print the JSON files found by the third menu.
                    \t6 - print the absolute path of the script.
                    \t7 - END of the program.
                """)

def menu(*list_of_menu_buttons):
    global data_JSON
    '''
        Function that prints a menu on the terminal.
        If we pass lists of commands : it do them without printed the menu.
    '''
    list_of_menu_buttons = list_of_menu_buttons[0] # enable to convert optional arguments of the function
    if list_of_menu_buttons != []: # Is there a sequence of executions to do ?
        val = list_of_menu_buttons.pop(0) # read the first element removed
    else : # Menu is printed and we wait the command prompt
        print_menu()
        list_of_menu_buttons = str(input()).split(' ') # We keep the string without spaces
        list_of_menu_buttons = list(list_of_menu_buttons) # We store them in a list
        list_of_menu_buttons = arguments_2_lists_of_integers(list_of_menu_buttons) # We convert them to a list of integers if possible
        val = list_of_menu_buttons.pop(0)
    if (val == 1):
        recursive_search_and_JSON_file_generator(".", 1)
    elif (val == 2):
        recursive_search_and_JSON_file_generator(".", 0)
    elif (val == 3):
        data_JSON += JSON_files_join(".")
    elif (val == 4):
        JSON_categories_plot (data_JSON)
    elif (val == 5):
        print (json.dumps(data_JSON, indent=4))
    elif (val == 6):
        print (os.getcwd())
    elif (val == 7):
        exit ()
    else :
        print ("Your choice must be an integer between 1 and 7 !")
    menu(list_of_menu_buttons) # recall the menu at the end of the task.

def arguments_2_lists_of_integers (arguments) :
    '''
        It tests and converts a list of arguments received by the shell to convert to a
        list of integers.
        It raises an exception and exit if an argument is not standard.
    '''
    try :    
        for i in range(len(arguments)):
            arguments[i] = int(arguments[i])
    except ValueError:
        print("Could not convert argument to an integer.")
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        exit(1)
    return (arguments)

def main (arguments) :
    global data_JSON
    data_JSON = []
    menu(arguments) # call the menu which is a switch-case of functions.

if (__name__ == "__main__"):
    '''
        It read the arguments of the script, try to convert them to integer.
        It forces python to execute the main fonction automatically.
        It executes the menu with the arguments (converted).
    '''
    arguments = arguments_2_lists_of_integers(sys.argv[1:])
    main(arguments)
