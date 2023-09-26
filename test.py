import pandas as pd
import sqlite3
import glob
import os
import csv



x = os.environ['USERPROFILE']
user = x[9:]

pattern = '/Users/' + user + '/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite'
matching_paths = glob.glob(pattern)
profile_folder = matching_paths[0]

print(f"{profile_folder}\n")


#cookie_file = profile_folder + '/cookies.sqlite'

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




# Loop through all cookies
result = dict()
for cookie in cookies:
    name, value, host, path, expiry = cookie
    #print(f"Name: {name}")
   #print(f"Value: {value}")
   #print(f"Domain: {host}")
   #print(f"Path: {path}")
   #print(f"Expires: {expiry}")
    i = 0
    for search in x:
        
        if name == search:
            result.update({name:y[i]})
        i+=1
   #writing to .txt file that will be used in order to compare against our CSV
    #with open("cookieNames.csv", "a") as file1:
     #   writer = csv.writer(file1)
        #file1.write(f"{name}\n")
      #  writer.writerow(name)

# Close the database connection



#with open("cookieNamesCsv.txt", "w") as file:
    #file.write(x)

print(result)
conn.close()

