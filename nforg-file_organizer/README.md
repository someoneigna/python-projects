Nforg  -  a Python script to organize files 
===========================================


There are three basic modes:
------------------------

-n/-n+: matches the starting letter of the files, moving them
 to folders with that corresponding letter.
 

-t: matches the filetype, moving the files to a folder with that
filetype name.


-t: matches files in the specified time frame, or exact time, not 
implemented currently.  





Usage: 
------

Arguments:

		nforg.py <mode> <filetypes> <dir>


To match files of the specified filetypes and group by mode.  



Example:  
----------



####Suppose we have a folder full of files, and its a mess :O
![Start](https://raw.github.com/someoneigna/python-projects/master/nforg-file_organizer/example_data/after.jpg)  





####Wouldn't be great if we could just sort all files, of the filetypes I want, into folders without hard work?
![SortingName](https://raw.github.com/someoneigna/python-projects/master/nforg-file_organizer/example_data/after_selective_name.jpg)  






####Hmm, but, what if I want to separate my source code, from my music and also from my books! Well, you can too:
![SortingType](https://raw.github.com/someoneigna/python-projects/master/nforg-file_organizer/example_data/sort_by_filetype.jpg)  







####Well, now I have a pdf dir, and a mp3 dir, and source code untouched. But I want my mp3 by Band/Author!!!
![SortingInsideFolder](https://raw.github.com/someoneigna/python-projects/master/nforg-file_organizer/example_data/sort_by_name_inside_mp3.jpg)  






####And now I have to look for a particular c and java project, so lets sort them by type and see what we got:
![FinalResult](https://raw.github.com/someoneigna/python-projects/master/nforg-file_organizer/example_data/final_result.jpg)  










What can and cannot nforge currently do:  
----------------------------------------  



**Can**
* Order files on the current specified dir, without recurse.
* Be used on Windows - GNU/Linux - MacOS, and almost every OS supporting Python 2.7.x


**Cannot**
* Handle more than one command operation at the time. (you can a make a script for that)
* Be stop to continue before.
* Save a list of files sorted with details. (this is unneeded most of the time, you can use tree and grep, etc)  


---------------
If you know of a feature that you could really found helpful just let me now. I will be more than happy to include it.  


P.D: Currently more test cases are needed to **ENSURE** you that is safe to use it, but it shouldn't break your files.
At most a file could end in a weird folder. But neitter has happened to me. I use it regularly. Anyway, use it **IN YOUR
OWN RISK**.  



I wish this little tutorial/demostration could help you. You can play with the [script][1] used in this demo and
with [nforg][2]. Just in case take this to [clean][3] the folder after.  


[1]: https://github.com/someoneigna/python-projects/blob/master/nforg-file_organizer/example_data/generate_files.py
[2]: https://github.com/someoneigna/python-projects/blob/master/nforg-file_organizer/nforg.py
[3]: https://github.com/someoneigna/python-projects/blob/master/nforg-file_organizer/example_data/clean_dir.sh
