import tkinter as tk
from tkinter import messagebox
import os

# ------ CONSTANTS ------ #

APPWIDTH = 630
APPHEIGHT = 600

# ------ VARS ------ #

# Initialize path to the current working directory for better cross-platform compatibility
# or keep "C:/" if specifically targeting Windows.
path = os.getcwd()

# ------ FUNCTIONS ------ #

def execute_command():
    global path
    request = cmdentry.get().strip() # .strip() to remove leading/trailing whitespace
    cmdentry.delete(0, tk.END)

    if request.startswith("out "):
        output = request[4:]
        messagebox.showinfo("Output", output)
    elif request.startswith("help"): # Use elif for exclusive command handling
        output = "Current commands:\n{out <text>} print whatever comes after it.\n{folderlist <folder-you-are-looking-at>} list all folders/files that are in the folder provided\n{gointodir <directory_path>} change the current directory displayed.\n{makefolder <foldername>} make a folder with the name provided.\n{credits} show credits info.\n{help} view this page."
        messagebox.showinfo("K Terminal Help", output)
    elif request.startswith("credits"):
        output = "Made by Ben Lewthwaite in 2025. © Ben Lewthwaite"
        messagebox.showinfo("Credits", output)
    elif request.startswith("folderlist "):
        target_path = request[11:]
        try:
            items = os.listdir(target_path)
            # Format the list of items into a more readable string
            output = "\n".join(items)
            messagebox.showinfo(f"Contents of {target_path}", output)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Directory not found: {target_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    elif request.startswith("gointodir "):
        new_path = request[10:]
        if os.path.isdir(new_path): # Check if the provided path is a valid directory
            path = new_path
            cmd.config(text=f"$ {path}") # Update the text of the existing cmd label
            messagebox.showinfo("Info", f"Changed path to: {path}")
        else:
            messagebox.showerror("Error", f"Invalid directory: {new_path}")
    elif request.startswith("makefolder "):
        new_path = f"{path}./" + request[11:]
        try:
            os.mkdir(new_path)
            messagebox.showinfo("Make Folder", f"Folder '{new_path}' created.")
        except FileExistsError:
            messagebox.showerror("Make Folder Error", f"Folder '{new_path}' already exists.")
        except FileNotFoundError:
            messagebox.showerror("Make Folder Error", f"Parent directory for '{new_path}' not found.")
    elif request.startswith("deletefolder "):
        path_to_delete = f"{path}./" + request[13:]
        try:
            os.rmdir(path_to_delete)
            messagebox.showinfo("Delete Folder", f"Folder '{path_to_delete}' deleted.")
        except FileNotFoundError:
            messagebox.showerror("Delete Folder Error", f"Parent directory for '{path_to_delete}' not found.")
    else:
        messagebox.showwarning("Unknown Command", f"'{request}' is not a recognized command. Type 'help' for a list of commands.")


# ------ APP INITIALIZATION ------ #

app = tk.Tk()
app.iconbitmap("logo.ico")
app.title("K Terminal")
app.configure(background="black")
app.geometry(f"{APPWIDTH}x{APPHEIGHT}")
app.resizable(False, False)

# ------ DRAWING ------ #

cmd = tk.Label(app, text=f"$ {path}", fg="green", bg="black")
cmd.place(x=1, y=1) # Removed pack()

cmdentry = tk.Entry(app, width=APPWIDTH - 40, bg="black", fg="green")
cmdentry.place(x=1, y=30) # Adjusted x to 1 for left alignment, and y slightly lower for spacing

cmdbutton = tk.Button(app, text="EXECUTE", command=execute_command)
cmdbutton.place(x=APPWIDTH // 2 - 40, y=APPHEIGHT - 26) # Centered the button horizontally

app.mainloop()