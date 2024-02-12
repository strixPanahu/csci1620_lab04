# **LAB 04**


## **Submission Instructions**

- [x] 0.) Submit 1 python file using naming convention below; Replace JaneDoe with your first and last name
	* e.g. JaneDoe4.py  



## **Question**

- [x] 1.) Download input.txt and store it in the same location as the script file.


- [ ] 2.) Write a program that will go through the lines in input.txt:

	- [ ] a.) If a line begins with From, use regex to find the lines
		- [ ] i.) Extract the email address, day, date, month, year, and time; 
			* There should be a space after the word “From ” to avoid logic errors
			
		- [ ] ii.) Send the details to a csv file named output.csv with the help of csv methods. 
			* This output.csv file should be stored in the same location as the script file.
			
		- [ ] iii.) The contents ofyour output.csv file should be identical to sample.csv
			* include the header row
			
	- [ ] b.) If a line begins with From: (use regular expressions to find the lines)
		- [ ] i.) Extract the email address, include Colon as part of the word 
			* e.g. lines that begin with From without a colon at the end
			
		- [ ] ii.) Keep track of how many ... email is sent from a ... address with ... a dictionary.
		
		- [ ] iii.) Send your dictionary results to an output file called output.txt. 
			* This output.txt file should be stored in the same location as the script file.
			
		- [ ] iv.) The contents of your output.txt file should be identical to sample.txt
			* Include the last row showing total email count
	
	
## Please note:
			
- [x] 3.) Write your program as a script (i.e., include the if _name_ ==‘_main_’: block).
	
- [x] 4.) Use the input and output file names provided in the instructions.
	
- [x] 5.) Output files should be opened in write mode not append mode.

- [x] 6.) Don’t forget to close any files you open.

- [x] 7.) Canvas shows the csv file as separated by tabs, but you should use the default ',’ delimiter.

- [x] 8.) Use newline='’ to prevent blank rows from being inserted into your csv file 
	
	- [x] a.) Refer to the explanation of slide 17 ofthe lecture notes. It might appear to have no effect on 		
		your PC, but you should always write your scripts to accommodate issues it might encounter 
		on other OS systems.
			
	- [ ] b.) I used 40 spaces for the email fields (e.g., file.write(f'{“Email”:40s} —Count \n’)) to achieve 
		uniform formatting. This is preferable to using tab spaces as tab spaces might not be consistent 
		across different systems (Refer to your week 2 string notes for details on this).
