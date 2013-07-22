nforg - A python script to organize files (Was for my PDF's)
=============================================================
Organize the files of the specified folder in the chosen mode.

There are three modes:
----------------------

-n/-n+: matches the starting letter of the files, moving them
 to folders with that corresponding letter.

-t: matches the filetype, moving the files to a folder with that
filetype name.

-t: matches files in the specified time frame, or exact time, not 
implemented currently.


Usage:
------        
Arguments: nforg.py <mode> <filetypes> <dir>

To match files of the specified filetypes and group by letter.

Example: 
--------
    nforg.py -n "pdf,png,txt" . 
In a folder with:

    The Catcher on the Rye.pdf Vacations013.png readme.txt Podcast12312.mp3
    
This would result in:

    Podcast12312.mp3
    T/The Catcher on the Rye.pdf
    V/Vacations013.png
    R/readme.txt
