# -*-coding:UTF8 ISO-8859-1 -*
import xml.etree.cElementTree as xml
import os
import json
import sys
import matplotlib.pyplot as plt # 2D plotting library

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

def JSON_categories_plot (JSON_file):
    '''
        Print a graph with the total images separated by types
    '''
    types = []
    number_of_types = []
    for desc in JSON_file :
        for details in desc.items() :
            if ((desc[0] == 'type') and (not(desc[0] in types))):
                desc[0] += types
            if (desc[0] == 'categories'):
                for format in desc[1]:
                    print (format)
                    # if detail_format in '.jpg'
                    # number_of_types += 1
            #categories += [{"format": cat[0], "nombre":cat[1]}]
            #number_of_types += contenu.keys('format')
            #types += contenu["types"]
    datatest = [5000, 1, 2]
    labels = ['A', 'B', 'C']
    try :
        1/0
        plt.figure(figsize=(8, 8))
        plt.plot(range(len(datatest)), datatest, color='blue')
        plt.xticks(range(len(datatest)), labels, rotation='vertical')
        plt.title('Histogram of the data classified by type')
        plt.show()
    except :
        print ("There is an error !")

def menu(*list_of_menu_buttons):
    global data_JSON
    '''
        Function that prints a menu on the terminal.
        If we pass lists of commands : it do them without printed the menu.
    '''
    list_of_menu_buttons = list_of_menu_buttons[0]
    if list_of_menu_buttons != []: # Is there a sequence of executions to do ?
        val = list_of_menu_buttons.pop(0) # read the first element removed
    else : # Menu is printed and we wait the command prompt
        print ("""\n\n Menu. Please, make a choice.
                        \t1 - create JSON files which contain info for each directory found recursively from . (overwrite existing JSON files)
                        \t2 - create JSON files which contain info for each directory found recursively from . (if it does not already exist) 
                        \t3 - get all JSON files found recursively from .
                        \t4 - plot statistics from the JSON files.
                        \t5 - print the JSON files found by the third menu.
                        \t6 - END of the program.
                    """)
        val = int(input())
    if (val == 1):
        # recursively research of directories
        recursive_search_and_JSON_file_generator(".", 1)
    elif (val == 2):
        recursive_search_and_JSON_file_generator(".", 0)
    elif (val == 3):
        data_JSON = JSON_files_join(".")
    elif (val == 4):
        JSON_categories_plot (data_JSON)
    elif (val == 5):
        print (json.dumps(data_JSON, indent=4))
    elif (val == 6):
        exit ()
    else :
        print ("Your choice must be an integer between 1 and 6 !")
    # recall the menu at the end of the task.
    menu(list_of_menu_buttons)

def main (arguments) :
    menu(arguments) # call the menu which is a switch-case of functions.

if (__name__ == "__main__"):
    '''
        It forces python to execute the main fonction automatically.
        It read the arguments of the script, try to convert them to integer.
        It executes the menu with the arguments.
    '''
    arguments = sys.argv[1:]
    for i in range(len(arguments)):
        try:
            arguments[i] = int(arguments[i])
        except ValueError:
            print("Could not convert argument to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    main(arguments)
