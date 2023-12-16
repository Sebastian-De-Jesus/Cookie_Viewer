import pandas as pd
import sqlite3
import glob
import os
from os.path import *
import platform
import tkinter as tk
from tkinter import messagebox

def clear_file(fileName=None):
    # Create result.txt if not exists, deletes its contents if it does.
    with open(fileName, "w") as file:
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
        #Finding the users correct USER name that will be needed in order to find that users file path for cookies
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

        #Finding the relative path to the directory for the EXE file to function.

        # Get the path to the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the relative path to the data folder
        data_folder = os.path.join(script_dir, "data")

        # Specify the relative path to the .csv file
        csv_file_path = os.path.join(data_folder, "cookie-database.csv")

        # Find all cookies
        cookies = cursor.fetchall()

        cookies_files = pd.read_csv(csv_file_path)
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

        # This will print out your cookie values as well as their uses to your terminal
        # additionally, this will also write the found values to a .txt file for use later
        for key in result:
            # Line below prints out to the terminal the cookie:function
            # print(f"This is the key : '{key}' and this is the value : '{result[key]}")

            # writes new contents to results
            with open("result.txt", "a") as file:
                file.write(f"{str(key)} : {str(result[key])}\n")

        # Attempting to remove the "[, ] characters from our file and writing back the altered lines"
        symbol_remove = ['[', ']', "'", '"']
        with open("result.txt", "r") as file:
            lines = file.readlines()

        # Next three lines allow us to remove all unwanted characters from our cookie:function txt
        for i in range(len(lines)):
            for symbol in symbol_remove:
                lines[i] = lines[i].replace(symbol, '')

        # writes the changes back to our result.txt for cleaner output.
        with open("result.txt", 'w') as file:
            file.writelines(lines)

        conn.close()

        # Display the content of result.txt in a Tkinter window
        show_result_content()

    except Exception as e:
        # Handle any exceptions or errors that may occur during execution
        show_custom_message(str(e), "Error", 40, 10)

# Function to display the content of result.txt in a Tkinter window
def show_result_content():
    content = ""
    with open("result.txt", "r") as file:
        content = file.read()

    result_window = tk.Toplevel(root)
    result_window.title("Scan Results")
    result_window.geometry("625x400")

    text_widget = tk.Text(result_window, wrap=tk.WORD, width=50, height=20)
    text_widget.pack()

    # Split the content into lines
    lines = content.split("\n")

    # Loop through each line
    for line in lines:
        # Find the index of the first ":"
        colon_index = line.find(":")

        if colon_index != -1:
            # Text before ":"
            cookie_name = line[:colon_index]
            # Text after ":"
            cookie_description = line[colon_index + 1:]

            # Insert the cookie name and description
            text_widget.insert(tk.END, cookie_name, ("cookie_name",))
            text_widget.insert(tk.END, ":")
            text_widget.insert(tk.END, cookie_description)
            text_widget.insert(tk.END, "\n")

    # Configure a tag to highlight cookie names
    text_widget.tag_configure("cookie_name", foreground="blue", font=("Arial", 12, "bold"))

    # Disable text editing
    text_widget.config(state=tk.DISABLED)

# Function to confirm program exit when the user clicks the X button
def on_closing():
    if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
        root.destroy()
# Create the main application window
root = tk.Tk()
root.title("Cookie Scanner")

#setting up our size for the window
root.geometry("625x280")

# Allowing our window to also be resized
root.resizable(True,True)

# Bind the on_closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a Text widget to explaining what a cookie is and how it can be used to a user
cookie_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
cookie_text.insert(tk.END,  "What is a COOKIE you might ask well allow us to explain!\n"
                            "A cookie is a small piece of data stored on your computer by websites you visit.\n"
                            "They are used to remember your preferences and provide a better browsing experience.\n"
                            "As well as TRACK you, identify your SPENDING habits, and better TARGET you.\n"
                            "By clicking Execute below we will see what cookies are on your system.")

#Disabling a user from editing the text
cookie_text.config(state=tk.DISABLED) 

cookie_text.grid(row=0, padx=10, pady=10)
# Create a button to execute the scan when clicked
scan_button = tk.Button(root, text="Execute Scan", command=execute_scan,width=40,bg="red",fg="white")
scan_button.grid(row=1)
# Place the radio button and button in the window

scan_button.grid(row=1)

# Start the GUI main loop
root.mainloop()
