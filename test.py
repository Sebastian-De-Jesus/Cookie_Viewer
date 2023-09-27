# Replace '/path/to/firefox/profile'
#profile_folder = '/Users/Mike/AppData/Roaming/Mozilla/Firefox/Profiles/6hjvnf5j.default-release'

#print(user)
#profile_folder = '/Users/' + user + '/AppData/Roaming/Mozilla/Firefox/Profiles/6hjvnf5j.default-release'
#print(profile_folder)
#cookie_file = profile_folder + '/cookies.sqlite'




# Libray to access cookie file as database
import sqlite3

# Access computer profile name
import os
x = os.environ['USERPROFILE']
user = x[9:]

# Search for specific files and folders
import glob
pattern = '/Users/' + user + '/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite'
matching_paths = glob.glob(pattern)
profile_folder = matching_paths[0]

# Connect to the SQLite
conn = sqlite3.connect(profile_folder)
cursor = conn.cursor()

# Cookie Request
cursor.execute("SELECT name, value, host, path, expiry FROM moz_cookies")
#cursor.execute("SELECT name FROM moz_cookies")

# Find all cookies
cookies = cursor.fetchall()

# Create dataframe from cookie database
import pandas as pd
database = pd.read_csv('cookie-database.csv')
x = list(database.iloc[:, 3:4].values)
y = list(database.iloc[:, 5:6].values)

# Blank container for cookies
result = dict()

# Loop through all cookies
for cookie in cookies:
    name, value, host, path, expiry = cookie
    i = 0
    for search in x:
        if name == search:
            temp = y[i]
            result.update({name:y[i]})
        i+=1
        
    #print(f"Name: {name}")  
    #print(f"Value: {value}")
    #print(f"Domain: {host}")
    #print(f"Path: {path}")
    #print(f"Expires: {expiry}")
    
print(result)

# Close the database connection
conn.close()



 