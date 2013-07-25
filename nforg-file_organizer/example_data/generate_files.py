import sys, os, random, string


def generate_files_quantity(directory, file_types, quantity):
    """ Generate quantity * file_types emtpy files """
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
            files_generated += 1
            file.close()
            quantity -= 1


    os.chdir("..")
    return files_generated


if len(sys.argv) >= 4:
    directory = sys.argv[1]
    if not os.path.exists(directory) and directory <> ".":
        print("Choose a valid dir!")
        sys.exit(2)
    
    filetypes = sys.argv[2].split(',')
    if not filetypes:
        print("Pass a valid \"extensions\" argument\nEx: \"pdf,txt,cpp\"")
        sys.exit(4)

    quantity =  int(sys.argv[3])
    if quantity < 0:
        print("Choose a valid quantity of files.")
        sys.exit(3)

    #filetypes = "pdf jpg txt c cpp java bmp zip rar".split() #List of extensions
    generated_quantity = generate_files_quantity(directory, filetypes, quantity)
    print("Generated {} files...".format(generated_quantity))

else:
    print("Example:\ngenerate_files.py . \"pdf,cpp,txt\" 100");
