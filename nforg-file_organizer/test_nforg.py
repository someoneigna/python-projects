""" Test case for nforg.py """
import os, sys, string, shutil, random
import nforg

test_files = [] 
DEBUG_MODE = 0


def generate_files_quantity(directory, file_types, quantity):
    """ Generate quantity * file_types emtpy files """
    global test_files
    quantity = quantity * len(file_types)
    files_generated = 0
    
    if( not os.path.exists(directory) ):
        os.mkdir(directory)
 
    try:
        os.chdir(directory)
    except:
        print("Cant change dir!\n")
        return "ERROR"


    while( quantity > 0):

        name_blueprint =  random.sample(string.ascii_letters, 3)
        name = ""
        for char in name_blueprint:
            name += char

        ftype = random.choice(file_types)
        file_name = name + "." + ftype

        if os.path.isfile(file_name):
            continue
        else:
            file = open(file_name, "w")
            test_files.append(file_name)
            files_generated += 1
            file.close()
            quantity -= 1


    os.chdir("..")
    return files_generated


def generate_files(directory, file_types):
    global test_files
    valid = "$()=-_"
    files_generated = 0
    
    if( not os.path.exists(directory) ):
        os.mkdir(directory)

    try:
        os.chdir(directory)
    except:
        print("Cant change dir!\n")
        return "ERROR"

    for char in (valid + string.ascii_letters):
        for filetype in file_types:
            filename = char + "." + filetype 
            
            file = open(filename, "w")
            test_files.append(filename)
            #files_generated += 1 
            file.close()

    test_files.sort() 
    os.chdir("..")
    #return files_generated


def clean_files(directory):
    try:
        shutil.rmtree(directory)
    except shutil.Error:
        print("Invalid folder or you dont have rights....")
        

def check_files(directory):
    '''Checks recursively the folder for generated files'''
    global test_files
    try:
        os.chdir(directory)
    except:
        print("Cant changedir to %s" % directory)
        return 

    matches, ntest_files = 0, len(test_files)
   
    #For every file on current file | ^ Dir was changed before
    for dir_tree in os.walk("."):
        
        #Complete dir path
        dir_path = dir_tree[0] + "/"
        
        #For file in current dir file list | os.walk() returns a tuple: (path, subdirs, files) 
        for fentry in dir_tree[2]: 
            
            #For file that was generated generated
            for i, gen_file in enumerate(test_files):
                
                #If generated file matches the current one
                if gen_file == fentry:
                    if DEBUG_MODE:
                        fullpath = dir_path + fentry 
                        print("{current} matches -> {list_current}".format(current=fullpath, list_current=gen_file))
                    del test_files[i]
                    matches += 1

    os.chdir("..")
    if matches == ntest_files:
        return "PASSED"
    if DEBUG_MODE:
        print("Couldn find:")
        for filename in test_files:
            print("{}\t".format(filename))
    return "FAILED"


def get_str(my_list):
    return ''.join(my_list) 


def test_nforg():
    #Generate generate_nfiles * len(file_types)
    generate_nfiles = 500

    #Some filetypes to test
    file_types = ["pdf", "jpg", "bmp", "png", "xls", \
        "c", "html", "php", "cpp", "txt", "java", "cs", \
        "zip", "rar", "gif"]

    #Dir made to populate with generated files
    test_dir = "nforgTest"

    #Quantity of sorted files passed by nforg, and this program generated files
    classified_files, total_files = 0, 0
    
    #A extra check, test nforg from main()
    if DEBUG_MODE:
        print("Doing extra check...\nCalling nforg.main()\n")
        print("Generating files...\n")
        generate_files_quantity(test_dir, file_types, generate_nfiles)

        nforg.main(("nforg.py", "-n+", get_str(file_types), test_dir))
        check_extra = check_files(test_dir)
        clean_files(test_dir)

    else:
        check_extra = 1
   
    #---------------------Check A: Generate files, sort by name--------
    
    #Generate files and the test dir
    if DEBUG_MODE:
        print("\nCreating files for first test:")
   
    generate_files_quantity(test_dir, file_types, generate_nfiles)
    total_files += len(test_files)
    
    #Call nforg and sort by filename
    if DEBUG_MODE:
        print("\nOrganizing by filename.")
    classified_files += nforg.organize_by_name(file_types, test_dir)
   
    #Call nforg and sort by filename (symbols only)
    if DEBUG_MODE:
        print("\nOrganizing by filename (symbols).")
    classified_files += nforg.organize_by_symbols(file_types, test_dir)
    
    #Check that sorted files match the generated ones
    if DEBUG_MODE:
        print("\nChecking files:")
    check_a = check_files(test_dir)
    
    if DEBUG_MODE:
        print("Organize by name check A: %s.\n" % check_a)
    #---------------------END of Check A: sort by filename-------------------

    
    
    #---------------------Check B: Generate files, sort by filetype--------
    
    #Clean test_dir folder by removing it
    if DEBUG_MODE:
        print("Cleaning folder to restart.\n")
    
    clean_files(test_dir)
    if len(test_files) > 0:
        print("ERROR: file quantity not 0 after cleanup")

    
    #Generate new files and make the folder
    if DEBUG_MODE:
        print("Generating files for second test.\n")
    
    generate_files_quantity(test_dir, file_types, generate_nfiles)
    total_files += len(test_files)

    
    #Call nforg to organize files by type
    if DEBUG_MODE:
        print("Organizing by filetype.\n")
    
    classified_files += nforg.organize_by_filetype(file_types, test_dir)
    
    
    #Check that generated files match sorted ones
    if DEBUG_MODE:
        print("\nChecking files:")
    
    check_b = check_files(test_dir)
    
    if DEBUG_MODE: 
        print("Organize by filetype check B: %s.\n" % check_b)
    #---------------------END of Check B: sort by filetype-------------------


    #Clean for last time test dir
    print("Cleaning %s folder.\n" % test_dir)
    clean_files(test_dir)

    #Check flags and print results
    if check_a == check_b and check_b == "PASSED" and\
            check_extra and\
            total_files == classified_files:
        print("\nTest case SUCEEDED!!!")
        print("%d files crated and classified.\n" % classified_files)

    else:
        print('''\nTest case FAILED.\nCreated %d files but %d were sorted.\n
                ''' % (total_files, classified_files))




if __name__ == "__main__":
    random.seed()
    if len(sys.argv) > 1:
        if sys.argv[1] == "DEBUG":
            DEBUG_MODE = 1
    test_nforg()
    
    
            

