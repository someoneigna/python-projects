''' A script to change some 'c' code style and errors.
    I should refactor this :\ '''
import os,sys

types = ["void", "int", "unsigned int", "long int", "char", "unsigned char", "float", "double"]
tokens = []
white_space = []

# Rules
#----------------------
def fflush_before_scanf(i,elements):
    return ( i+1 < len(elements) and "scanf" in elements[i+1] and "fflush(stdin)" in elements[i] )

def is_fflush_stdin(element):
    return ( "fflush(stdin)" in element )

def scanf_str_has_ampersand(element):
    return( "scanf" in element  and ("%s" in element) and ("&" in element) )

def main_not_specified_type(i,elements):
    if(i>0 and "main" in elements[i]):
        for t in types:
            if( t in elements[i-1] or t + " main" in elements[i] ):
                return 0  #Main has type and its ok
        return( 1 ) #Fix main, type missing, add return 0 too
    return 0

#---------------------------


def replace(line_set):
    tokenize(line_set)
    i=0
    for i,token in enumerate(tokens):

        if(fflush_before_scanf(i,tokens)):
           del tokens[i] #fflush(stdin)
           tokens.insert( i+1, "getchar();" )
           continue
        elif(is_fflush_stdin(token)):
            del tokens[i]
            tokens.insert( i, "getchar();" )
            continue


        if(scanf_str_has_ampersand(token)):
            replace = token.replace( "&", "" )
            del tokens[i]
            tokens.insert( i, replace )
            continue

        if(main_not_specified_type(i, tokens)):
            del tokens[i]
            tokens.insert( i, token.replace("main", "int main") )

            tokens.insert( len(tokens)-1, "return 0;")
            white_space.insert( len(white_space)-2, white_space[len(white_space)-4] )
            white_space.insert( len(white_space)-1, 0)
            continue


def tokenize(line_set):
    for i,line in enumerate(line_set):

        token = line.strip()
        tokens.append(token)

        if line.startswith(" "):
            white_right = len(line.lstrip()) - len(token)
            white_left = len(line.rstrip()) - len(token)
            #print "LeftW:"+str(white_left)+" RightW:"+str(white_right)
        else:
            white_left = 0
            white_right = 0

        white_space.append(white_left)
        white_space.append(white_right)

        #print "Token:"+line.strip()

def fix_file( filename, result_filename ):

    if (filename.split("."))[1] <> "c":
        print "Seems that the file is not C/C++ source code\nOutput may be invalid...\n"
        return False

    result_filename = result + ".result"
    
    try:
        source_file = open( filename, "r" )
        
        if os.path.exists( result_filename ):
            print ( "The file {} exists".format(result) + "...")
            print ( "Saving result as:" + result_filename )
            result_file = open( result_filename, "w" )
            
        else:
            result_file = open( result, "w" )

        lines=[]
        for line in source_file:
            #print "Read Token:" + line.strip()
            lines.append(line)
        replace(lines)


        r=0
        for i, token in enumerate(tokens):
            result_file.write(" " * white_space[r] + token + (" " * white_space[r+1]) + "\n" )
            r+=2

        source_file.close()
        result_file.close()
        
        return True
        
    except IOError:
        print "Invalid or inexistant file...\nSpecify a valid source code file!...\n"


def main():
    if ( len(sys.argv)>=3 and sys.argv[2] ):
        fix_file( sys.argv[1],sys.argv[2] )
        
    else:
        print ("Try with \"garin_fixer.py source_code.c result_source_code.c\"")

if __name__ == '__main__':
    main()
