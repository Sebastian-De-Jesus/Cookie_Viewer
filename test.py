import pandas as pd
import sqlite3
import glob
import os
<<<<<<< HEAD
import csv
=======
import json
import numpy as np
>>>>>>> 237d3526c6d08bc14b80bd74bbe4a8e2fec4d326
from os.path import *



def clear_file(fileName = None):
    #Checks if results exisits deletes its contents if it does.
    if exists("result.txt"):
        with open("result.txt", "w") as file:
            file.truncate(0)



#Finding the users correct USER name that will be needed in order to find that users file path for cookies
x = os.environ['USERPROFILE']
user = x[9:]

#Here we are using pattern recogintion in order for out file to find the correct cookie path for users
# additionally saves the value to a variable called profile_folder
pattern = '/Users/' + user + '/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite'
matching_paths = glob.glob(pattern)
profile_folder = matching_paths[0]

#prints out the users folder path for the cookies folder for firefox
print(f"{profile_folder}\n")

# Connect to the SQLite
conn = sqlite3.connect(profile_folder)
cursor = conn.cursor()

# Cookie Request
cursor.execute("SELECT name, value, host, path, expiry FROM moz_cookies")

# Find all cookies
cookies = cursor.fetchall()

cookies_files = pd.read_csv("cookie-database.csv")
<<<<<<< HEAD
x = cookies_files.iloc[:, 3:4].values
y = list(cookies_files.iloc[:, 5:6].values)

# Loop through all cookies and verifies which ones we have found within our 
# cookie database, saves the found cookies to a dictionary called result
result = dict()
for cookie in cookies:
    name, value, host, path, expiry = cookie
    i = 0
    for search in x:

        if name == search:
            result.update({name: y[i]})
        i += 1


clear_file(fileName="result.txt")

#This will print out your print out your cookie values aswell as thier uses to your terminal
#additionally this will also write the found values to a .txt file for use later
for key in result:
    #Line below prints out to the terminal the cookie:function
    #print(f"This is the key : '{key}' and this is the value : '{result[key]}") 
           
    #writes new contents to results
    with open("result.txt","a") as file:
        file.write(f"{str(key)} : {str(result[key])}\n")

#Attempting to remove the "[, ] characters from our file and writing back the altered lines"
symbol_remove = ['[',']',"'",'"']
with open("result.txt","r") as file: 
    lines = file.readlines()
 
#Next three lines allows us to remove all unwanted charaters from out cookie:function txt
for i in range(len(lines)):
    for symbol in symbol_remove:
        lines[i] = lines[i].replace(symbol, '')

#writes the changes back to our result.txt for cleaner output.
with open("result.txt", 'w') as file:
    file.writelines(lines)
    
=======
x = cookies_files.iloc[:, 3].values
y = list(cookies_files.iloc[:, 5].values)

# Loop through all cookies and verifies which ones we have found within our 
# cookie database, saves the found cookies to a dictionary called result

container = []
for cookie in cookies:
    name, value, host, path, expiry = cookie
    
    i = 0
    for search in x:
        if name == search:
            result = dict()
            result.update({'NAME': name})
            result.update({'PURPOSE': y[i]})
            container.append(result)
        i += 1


# Create json file for javascript, to create table from javascript, 1st option
json_obj = json.dumps(container, indent=4)
with open("result.json", "w") as outfile:
    outfile.write(json_obj)

# Create html table, can be used directly in extension popup, 2nd option
df = pd.DataFrame.from_dict(container)
df.to_html('result.html')











clear_file(fileName="result.txt")

#This will print out your print out your cookie values aswell as thier uses to your terminal
#additionally this will also write the found values to a .txt file for use later
for key in result:
    #Line below prints out to the terminal the cookie:function
    #print(f"This is the key : '{key}' and this is the value : '{result[key]}") 
           
    #writes new contents to results
    with open("result.txt","a") as file:
        file.write(f"{str(key)} : {str(result[key])}\n")

#Attempting to remove the "[, ] characters from our file and writing back the altered lines"
symbol_remove = ['[',']',"'",'"']
with open("result.txt","r") as file: 
    lines = file.readlines()
 
#Next three lines allows us to remove all unwanted charaters from out cookie:function txt
for i in range(len(lines)):
    for symbol in symbol_remove:
        lines[i] = lines[i].replace(symbol, '')

#writes the changes back to our result.txt for cleaner output.
with open("result.txt", 'w') as file:
    file.writelines(lines)



>>>>>>> 237d3526c6d08bc14b80bd74bbe4a8e2fec4d326
conn.close()



 