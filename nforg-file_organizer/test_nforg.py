""" Test case  0 for nforg.py """
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
            #files_generated += 1
            file.close()
            quantity -= 1


    os.chdir("..")
    #return files_generated




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
    shutil.rmtree(directory)



def check_files(directory):
    global test_files
    try:
        os.chdir(directory)
    except:
        print("Cant changedir to %s" % directory)
        return 

    matches, ntest_files = 0, len(test_files)
    
    for dir_tree in os.walk("."):
        dir_path = dir_tree[0] + "/"
        for fentry in dir_tree[2]: 
            for i, filename in enumerate(test_files):
                
                if filename == fentry:
                    if DEBUG_MODE:
                        fullpath = dir_path + filename
                        print("%s matches -> %s" %(filename, fullpath))
                    del test_files[i]
                    matches += 1

    os.chdir("..")
    if matches == ntest_files:
        return "PASSED"
    if DEBUG_MODE:
        print("Couldn find:")
        for filename in test_files:
            print("%s\t" % filename)
    return "FAILED"



def get_str(my_list):
    
    mystr = "\""
    for index, element in enumerate(my_list):
        if index < len(my_list)-1:
            mystr += element + ","
        else:
            mystr += element
    mystr += "\""
    return mystr 



def test_nforg():
    generate_nfiles = 100

    file_types = ["pdf", "jpg", "bmp", "png", "xls", \
        "c", "html", "php", "cpp", "txt", "java", "cs", \
        "zip", "rar", "gif"]
    test_dir = "nforgTest"

    classified_files, total_files = 0, 0

    if DEBUG_MODE:
        print("Doing extra check...\nCalling nforg.main()\n")
        print("Generating files...\n")
        generate_files(test_dir, file_types)
        generate_files_quantity(test_dir, file_types, generate_nfiles)

        nforg.main(("nforg.py", "-n+", get_str(file_types), test_dir))
        check_extra = check_files(test_dir)
        clean_files(test_dir)

    else:
        check_extra = 1
    
    if DEBUG_MODE:
        print("\nCreating files for first test:")
    generate_files(test_dir, file_types)
    generate_files_quantity(test_dir, file_types, generate_nfiles)
    total_files += len(test_files)
    
    if DEBUG_MODE:
        print("\nOrganizing by filename.")
    classified_files += nforg.organize_by_name(file_types + ["xml", "txt", "zip", "rar"], "-n", test_dir)
    
    if DEBUG_MODE:
        print("\nOrganizing by filename (symbols).")
    classified_files += nforg.organize_by_symbols(file_types + ["xml", "txt", "zip", "rar"], test_dir)
   
    if DEBUG_MODE:
        print("\nChecking files:")
    check_a = check_files(test_dir)
    
    if DEBUG_MODE:
        print("Organize by name check A: %s.\n" % check_a)

    if DEBUG_MODE:
        print("Cleaning folder to restart.\n")
    clean_files(test_dir)
    if len(test_files) > 0:
        print("ERROR: file quantity not 0 after cleanup")

    if DEBUG_MODE:
        print("Generating files for second test.\n")
    generate_files(test_dir, file_types)
    generate_files_quantity(test_dir, file_types, generate_nfiles)
    total_files += len(test_files)

    if DEBUG_MODE:
        print("Organizing by filetype.\n")
    classified_files += nforg.organize_by_filetype(file_types + ["xml", "txt", "zip", "rar"] , test_dir)
    
    if DEBUG_MODE:
        print("\nChecking files:")
    check_b = check_files(test_dir)
    
    if DEBUG_MODE: 
        print("Organize by filetype check B: %s.\n" % check_b)
    print("Cleaning %s folder.\n" % test_dir)
    clean_files(test_dir)

    if check_a == check_b and check_b == "PASSED" and\
            check_extra and\
            total_files == classified_files:
        print("\nTest case SUCEEDED!!!")
        print("%d files crated and classified.\n" % classified_files)
    else:
        print("""\nTest case FAILED.\nCreated %d files but %d were sorted.\n
                """ % (total_files, classified_files))




if __name__ == "__main__":
    random.seed()
    if len(sys.argv) > 1:
        if sys.argv[1] == "DEBUG":
            DEBUG_MODE = 1
    test_nforg()
    
    
            

