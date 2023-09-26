import sqlite3

# Replace '/path/to/firefox/profile'
#profile_folder = '/Users/rocke/AppData/Roaming/Mozilla/Firefox/Profiles/rs9enx0g.default-release'
#specific user profile
import os
x = os.environ['USERPROFILE']
user = x[9:]
print(user)

profile_folder = '/Users/' + user + '/AppData/Roaming/Mozilla/Firefox/Profiles/6hjvnf5j.default-release'
print(profile_folder)

cookie_file = profile_folder + '/cookies.sqlite'

# Connect to the SQLite
conn = sqlite3.connect(cookie_file)
cursor = conn.cursor()

# Cookie Request
cursor.execute("SELECT name, value, host, path, expiry FROM moz_cookies")

# Find all cookies
cookies = cursor.fetchall()

# Loop through all cookies
for cookie in cookies:
    name, value, host, path, expiry = cookie
    print(f"Name: {name}")
    print(f"Value: {value}")
    print(f"Domain: {host}")
    print(f"Path: {path}")
    print(f"Expires: {expiry}")

# Close the database connection
conn.close()
