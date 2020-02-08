Fall 2019
ECE1779
Assignment 1.
Author: Zixuan Hu

## Instruction:
### 1. Set database;

MySQL code for creating a table:
run:
- mysql -u username -p password <A1.sql
        
In the config.py file, you need to set up your own database first!

### 2. Run the flask:
  I create a virtual env to run the flask:
    by using python3: 
    
     - python3 -m venv venv
     - source ./venv/bin/activate
     
    this command line works for my macOS
    for windows OS:
    
     - python3 -m venv venv
     - ./venv/bin/activate
  
  then set the env for flask:
   - EXPORT FLASK_APP=main.py
   - EXPORT FLASK_ENV=development
    flask run
  for windows user:
   - set FLASK_APP=main.py
   - set FLASK_ENV=development
   - flask run
  Hope this works.
 


## To do lists:

FOR OPTIMIZATION:
2. Image delete function;
3. Make pages looks better.

... what else?
