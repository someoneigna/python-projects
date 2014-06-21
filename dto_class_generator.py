''' Reads each C# class file in specified dir, and extracts the public
    properties generating DTO (classes used for serialization and ORM)

    Params:
            0: (Optional)
                Parent namespace for the resultant DTO's
                    ex: 'Synchronizer'
                    result namespace: 'namespace Synchronizer.Data.DTO'
                
            1: Input dir containing C# classes
            2: Output dir for DTO classes
            
    Output: For each input class a 'class_name' + DTO file with
    the public properties.

    Example:
        If we have: Person.cs and Request.cs in Models/

        doing:
            dto_class_generator.py Models/ DTO/

        we get:
            PersonDTO.cs and RequestDTO.cs
'''

import re
import sys
import os

DEBUG = False

# Regex matching public properties
property_regex = re.compile('(?:public)\s(?!class)(?!override|abstract|static|readonly)(?P<type>[\w<>]+) (?P<name>\w+)(?![\(\w])')

# Regex matching using statements
import_regex = re.compile('(?:using) (?P<import>[\w\.]+);')

# Regex matching public and internal classes
class_name_regex = re.compile('(public|internal) (?P<modifier>abstract|static)?(\s)?(class) (?P<classname>\w+)')

def match_properties(text):
    return property_regex.search(text)

def match_class_name(text):
    return class_name_regex.search(text)

# Taken from StackOverflow, made by mg.
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def indent(string, level):
    return ' ' * level + string

def generate_dto(project_namespace, filepath, result_filepath):
    ''' Parse the input class file and extract classes
        and properties for each '''

    identation = 0 # Level of indent
    
    data = parse_file(filepath)
    imports = data[0]
    result = data[1]

    # Show classes read from file and properties found
    if DEBUG:
        print ('\nShowing results:')
        print (imports)
        print (result)
        for class_found in result:
            print ('Class:' + class_found)
            print ('Inside:')
            for property_found in result[class_found]:
                print (property_found)

    # Create result file for writing the results
    with open(result_filepath, 'w') as result_file:
        output = ''

        # Using statements
        for import_statement in imports:
            output = ''.join(output + 'using ' + import_statement + ';\n')
                    
        # Namespace start
        output = ''.join(output + '\nnamespace ' + project_namespace + '.Data.DTO\n' +\
        '{' + '\n')
        
        for class_found in result:

            # Class header
            indent_level = 4
            output = ''.join(output +
                             indent('/// <summary>\n', indent_level) +
                             indent('/// DTO generated from <see cref="' + class_found + '"/> for storage.\n', indent_level) +
                             indent('/// </summary>\n', indent_level) +
                             indent('public class ' + class_found + 'DTO' + '\n', indent_level) +
                             indent('{\n', indent_level)
                            )
            

            # Empty constructor
            indent_level += 4
            output += indent('public ' + class_found + 'DTO' + '()' + '{}\n\n', indent_level)

            # Inside properties
            for property_found in result[class_found]:
                output = ''.join(output +
                                 indent('public ' + property_found['type'] + ' ' + property_found['name'] +\
                                       ' { get; set; }\n', indent_level))

            # Write class to DTO generator (copies properties with reflection)
            output = ''.join(output + '\n' +
            indent('public ' + class_found + 'DTO' + '(' + class_found + ' other)\n', indent_level) +
            indent('{\n', indent_level) +
            indent('foreach(var property in other.GetType().GetProperties())\n', indent_level + 4) +
            indent('{\n', indent_level + 4) +
            indent('this.GetType()\n', indent_level + 8) +
            indent('.GetProperty(property.Name)\n', indent_level + 8) +
            indent('.SetValue(this, property.GetValue(other, null), null);\n', indent_level + 8) +
            indent('}\n', indent_level + 4) +
            indent('}\n', indent_level)
                              )
            # Write DTO to class generator (recovers a class instance from the DTO)
            output = ''.join(output + '\n' +
                             indent('/// <summary>\n', indent_level) +
                             indent('/// Returns a <see cref="' + class_found + '"/> from this DTO.\n', indent_level) +
                             indent('/// </summary>\n', indent_level) +
                             indent('public ' + class_found + ' Reconstruct()\n', indent_level) +
                             indent('{\n', indent_level) +
                             indent(class_found + ' result = new ' + class_found + '()\n', indent_level + 4) +
                             indent('{\n', indent_level + 4) )
            
            for property_found in result[class_found]:
                output = ''.join(output +
                                 indent(property_found['name'] + ' = ' + 'this.' + property_found['name'] + ',\n', indent_level + 8) )

            output = rreplace(output, ',', '', 1) # Remove last ','

            # Return result
            output = ''.join(output + indent('}\n', indent_level + 4) + indent('return result;\n', indent_level + 4))
            
            # Close Reconstruct() method
            output = ''.join(output  +
                             indent('}\n', indent_level))
                             
                             
                             

            # Close class
            indent_level -= 4
            output = ''.join(output + indent('}\n' +\
        
            # Close namespace
            '}', indent_level))

            if DEBUG:
                print('Result file:\n' + output)
                
            # Write the result file
            result_file.write(output)
    

def parse_file(filepath):
    ''' Returns classes and properties found in a class file '''
    ''' Input: string path to the file to parse '''
    ''' Output: tuple(list of imports strings, dict (class, properties[])) '''

    classes = dict()
    imports = list()
    current_class = None
    inside_class = False

    text = open(filepath, 'r').read()

    if DEBUG:
        print('Input:\n' + text)
    property_match = None
    class_match = None
    
    for line in text.split('\n'):
        if (len(line) < 1):
            continue

        if DEBUG: # Show line
            print ('Line:\n' + line)

        import_match = import_regex.search(line)

        if (import_match != None):
            imports.append(import_match.groupdict()['import'])
            continue
        
        class_match = match_class_name(line)
        if (class_match != None):
            inside_class = True
            current_class = class_match.groupdict()['classname']
            classes[current_class] = list()
            
            if DEBUG:
                print (classes)
                print ('Got: ')
                print (class_match.groupdict())
                print ('\n')
            continue
        
        if (line == '{' or line == '}'):
            if DEBUG:
                print('Skipped bracket line\n')
            if (line == '{'):
                inside_class = True
                
                
            if (line == '}'):
                inside_class = False  #Exiting class
            continue
        
        if (inside_class):
            property_match = match_properties(line)
            if (property_match != None):
                if DEBUG:
                    print ('Got: ')
                    print (property_match.groupdict())
                    print ('\n')

                # Append property found to current class
                try:
                    classes[current_class].append(property_match.groupdict())
                except KeyError as k:
                    print ('Got key error:{0}'.format(k) + ' when\n' + line)
                
    if DEBUG:
        print ('\n')
        
    return (imports, classes)


if __name__ == '__main__':

    namespace_index = None

    # Params: Namespace Input_dir Output_dir
    if (len(sys.argv) > 3):
        namespace_index = 1
        input_index = 2
        output_index = 3

    # Params: Input_dir Output_dir
    elif (len(sys.argv) > 2):
        input_index = 1
        output_index = 2
        
    if namespace_index != None:
        # Parent namespace for DTO
        project_namespace = sys.argv[namespace_index]
    else:
        project_namespace = 'MyProject'

    if input_index != None:
        
        # Read all class files in input_dir
        input_dir = sys.argv[input_index]


        # And make DTO result class on output
        output_dir = sys.argv[output_index]

        if os.path.isfile(input_dir):
            input_filepath = input_dir
            output_filepath = output_dir

            generate_dto(project_namespace, input_filepath, output_filepath)

        else:
            # For each class file found in input_dir
            # read generate a DTO for each one
            for class_filepath in os.listdir(input_dir):

                # File has to be C# code
                if class_filepath.endswith('.cs'):
                    input_filepath = input_dir + '\\' + class_filepath
                    output_filepath = output_dir + '\\' + class_filepath.split('.')[0] + 'DTO' + '.cs'
                    
                    generate_dto(project_namespace, input_filepath, output_filepath)
    
