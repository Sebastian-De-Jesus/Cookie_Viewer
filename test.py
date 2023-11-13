import pandas as pd
import sqlite3
import glob
import os
import csv
from os.path import *
import platform
import tkinter as tk
from tkinter import messagebox


def clear_file(fileName = None):
    #Checks if results exisits deletes its contents if it does.
    if exists("result.txt"):
        with open("result.txt", "w") as file:
            file.truncate(0)



# Get the system's platform
def current_system():
    '''Using this will provide you with the information about what system you are on '''
    current_platform = platform.system()

    if current_platform == "Windows":
        print("Running on a Windows machine.")
    elif current_platform == "Darwin":
        print("Running on a Mac machine.")
    else:
        print("Running on a different operating system.")
        
# Function to display a custom message box with a larger size
def show_custom_message(message, title, width, height):
    custom_dialog = tk.Toplevel(root)
    custom_dialog.title(title)

    text_widget = tk.Text(custom_dialog, wrap=tk.WORD, width=width, height=height)
    text_widget.insert(tk.END, message)
    text_widget.pack()


def execute_scan():
    try:
        #Finding the users correct USER name that willpi be needed in order to find that users file path for cookies
        current_system()
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
            
        conn.close()
        show_custom_message("Scan completed successfully.", "Scan Completed", 70, 10)
    except Exception as e:
        # Handle any exceptions or errors that may occur during execution
        show_custom_message(str(e), "Error", 40, 10)

# Function to confirm program exit when the user clicks the X button
def on_closing():
    if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
        root.destroy()
# Create the main application window
root = tk.Tk()
root.title("Cookie Scanner")

# Bind the on_closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a variable to hold the radio button selection
scan_option = tk.IntVar()
scan_option.set(0)  # Initialize to 0 (no selection)

# Create the "Scan" radio button
scan_radio = tk.Radiobutton(root, text="Scan", variable=scan_option, value=1)

# Create a button to execute the scan when clicked
scan_button = tk.Button(root, text="Execute Scan", command=execute_scan)

# Place the radio button and button in the window
scan_radio.pack()
scan_button.pack()

# Start the GUI main loop
root.mainloop()