import requests
import tkinter as tk
from tkinter import filedialog, messagebox

def download_exe(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = response.url.split('/')[-1]
        save_path = save_folder.get()
        with open(f"{save_path}/{filename}", 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Success", f"File {filename} has been successfully uploaded")
    else:
        messagebox.showerror("Error", f"Failed to download file by link {url}")

def add_link():
    url = url_entry.get()
    if url:
        links.append(url)
        save_links()
        update_listbox()

def remove_link():
    selected_index = url_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        del links[index]
        save_links()
        update_listbox()

def save_links():
    with open("links.txt", "w") as f:
        for link in links:
            f.write(link + "\n")

def update_listbox():
    url_listbox.delete(0, tk.END)
    for link in links:
        url_listbox.insert(tk.END, link)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        save_folder.set(folder_path)

def download_all():
    for url in links:
        download_exe(url)
    messagebox.showinfo("Success", "All files uploaded successfully")    

def save_links():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            for link in links:
                f.write(link + "\n")
        messagebox.showinfo("Success", "The list of links was successfully saved")

def load_links():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        url_listbox.delete(0, tk.END)  # Clearing list of links
        with open(file_path, "r") as f:
            loaded_links = f.read().splitlines()
            links.clear()  # Clearing current link list
            links.extend(loaded_links)  # Adding downloaded links
            update_listbox()

# Creating a GUI
root = tk.Tk()
root.title("Downloading exe files")

# Loading a list of links from a file
try:
    with open("links.txt", "r") as f:
        links = f.read().splitlines()
except FileNotFoundError:
    links = []

# Creating interface
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add a link", command=add_link)
add_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

url_listbox = tk.Listbox(root, width=60, height=10)
url_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

update_listbox()

remove_button = tk.Button(root, text="Delete link", command=remove_link)
remove_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

folder_label = tk.Label(root, text="Download path:")
folder_label.grid(row=4, column=0, padx=5, pady=5)

save_folder = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=save_folder, width=50)
folder_entry.grid(row=4, column=1, padx=5, pady=5)

select_folder_button = tk.Button(root, text="Select a folder", command=select_folder)
select_folder_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

download_button = tk.Button(root, text="Download selected", command=lambda: download_exe(url_listbox.get(tk.ACTIVE)))
download_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

download_all_button = tk.Button(root, text="Download all", command=download_all)
download_all_button.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

load_button = tk.Button(root, text="Load from file", command=load_links)
load_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

save_button = tk.Button(root, text="Save list", command=save_links)
save_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

# Launch
root.mainloop()
