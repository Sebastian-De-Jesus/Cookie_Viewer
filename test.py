import pandas as pd
import sqlite3
import glob
import os
import csv

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


#This will print out your print out your cookie values aswell as thier uses to your terminal
#additionally this will also write the found values to a .txt file for use later
for key in result:
    print(f"This is the key : '{key}' and this is the value : '{result[key]}")
    with open("result.txt","a") as file:
        file.write(f"{str(key)} : {str(result[key])}\n")

conn.close()
