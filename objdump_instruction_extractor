''' Extracts from objdump -d output the hexcode for each op+operands '''

import sys
import re

exe_info_line = 2  # objdump -d second line has ej: "program.exe:  file format pei-i386"
section_start_line = 5 # contains: \'Dissasembly of section .text: '''
function_dissasembly_line = 7 # First line containing the header for 
                              #    first function ej: 00401000 <_main>: 
                              #    match it with: function_code_re '''

line_code_re = r'(?P<addr>\w+):\s+'\
               '(?P<hexrep>(\w{2}\s)+)\s+'\
               '(?P<op>\w+){1}\s*'\
               '(?P<loperand>[\w$%\[\]*]+)?,'\
               '?(?P<roperand>[\w$%\[\]*]+)?'

FIRST_ARG = 1 # First commandline argument

function_code_re = '(?P<address>[0-9a-b]+)\s<(?P<label>\w+)>:'

cline_code_re = re.compile(line_code_re)
cfunction_code_re = re.compile(function_code_re)


def hex_for_each_op(string):
    for hgroup in string.split():
        yield '\\' + 'x' + hgroup
    pass

def main():
    if len(sys.argv) < 2:
        return
    
    with open(sys.argv[FIRST_ARG], 'r') as objdump_file :
        output = ''
        
        lines = objdump_file.read().split('\n')
        
        # Get the hex representation for each line of objdump
        for line in lines:
            if '' or '(bad)' in line or '...' in line:
                continue

            elif 'Dissasembly of section' in line:
                output += line + '\n\n'
                
            print('Processing:\n' + line)
            
            match_section = cfunction_code_re.search(line)
            match_code = cline_code_re.search(line)
            
            if match_section != None:
                section = match_section.groupdict()['label']
                output += '\nSection: {0}'.format(section) + '\n\n'

            elif match_code != None:
                for hexrep in hex_for_each_op(match_code.groupdict()['hexrep']):
                    output += hexrep
                output += '\n'
                
        # Store the hexcode of each instruction + operands into new file
        result_file = open(sys.argv[FIRST_ARG] + '.shellcode', 'w')
        result_file.writelines(output)

        result_file.close()

if __name__ == '__main__':
    main()
            
        
        
    
