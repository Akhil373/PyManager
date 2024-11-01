import os
import shutil
import tkinter as tk
import customtkinter as ctk
import psutil


def file_organize(directory_path):
    status_label.configure(text="Sorting...", text_color="orange")
    app.update_idletasks()
    log_textbox.delete("1.0", tk.END)
    log_textbox.configure(state=tk.NORMAL)
    
    try:
        if not os.path.isdir(directory_path):
            raise FileNotFoundError("Invalid directory path. Please try again.")
        
        os.chdir(directory_path)
        current_dir = os.getcwd()
        log_textbox.insert(tk.END, f"Current Directory: {current_dir}\n")

        file_types = {
            "Images": ["jpeg", "png", "jpg", "gif"],
            "Text": ["doc", "txt", "pdf", "xlsx", "docx", "xls", "rtf", "pptx"],
            "Videos": ["mp4", "mkv"],
            "Sounds": ["mp3", "wav", "m4a"],
            "Applications": ["exe", "lnk", "sh", "app"],
            "Codes": ["c", "py", "java", "cpp", "js", "html", "css", "php"],
        }

        files = os.listdir(current_dir)
        
        for file in files:
            if os.path.isfile(file):
                file_ext = file.split(".")[-1].lower() if '.' in file else ''
                dest_dir = None

                # Determine destination directory based on file extension
                for dir_name, extensions in file_types.items():
                    if file_ext in extensions:
                        dest_dir = os.path.join(current_dir, dir_name)
                        break
                else:
                    dest_dir = os.path.join(current_dir, "Others")
                
                # Create directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    log_textbox.insert(tk.END, f"Created directory: {dest_dir}\n")
                
                shutil.move(file, dest_dir)
                log_textbox.insert(tk.END, f"Moved '{file}' to '{dest_dir}'\n")

        status_label.configure(text="Sorting Completed!", text_color="green")
        log_textbox.insert(tk.END, "Sorting Completed...\n")

    except FileNotFoundError as e:
        status_label.configure(text=str(e), text_color="red")
        log_textbox.insert(tk.END, f"Error: {e}\n")
    except Exception as e:
        status_label.configure(text=f"An error occurred: {e}", text_color="red")
        log_textbox.insert(tk.END, f"Error: {e}\n")
    finally:
        log_textbox.configure(state=tk.DISABLED)
        app.update_idletasks()

def delete_duplicates(text):
    try:
        os.chdir(text)
        current = os.getcwd()
        print(f"Current Directory: {current}")

        files = os.listdir(current)
        file_dict = {}

        for file in files:
            if os.path.isfile(os.path.join(current, file)):
                file_size = os.path.getsize(os.path.join(current, file))
                if file_size in file_dict:
                    file_dict[file_size].append(file)
                else:
                    file_dict[file_size] = [file]

        for file_size, file_list in file_dict.items():
            if len(file_list) > 1:
                original_file = file_list[0]
                for duplicate_file in file_list[1:]:
                    os.remove(os.path.join(current, duplicate_file))
                    print(f"Deleted duplicate file: {duplicate_file}")
                    log_textbox.insert(tk.END, f"Deleted duplicate file: {duplicate_file}\n")

    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")
        print(e)

def delete_duplicates_and_organize():
    text = textbox.get("1.0", "end-1c").strip()
    delete_duplicates(text)
    file_organize(text)

def only_organize():
    text = textbox.get("1.0", "end-1c").strip()
    file_organize(text)

import os
import shutil
import tkinter as tk
import customtkinter as ctk
import psutil

def disk_space_analysis(directory):
    if not os.path.isdir(directory):
        status_label.configure(text="Invalid directory path.", text_color="red")
        log_textbox.insert(tk.END, "Error: Invalid directory path.\n")
        return 

    try:
        disk_usage = psutil.disk_usage(directory)

        drive_letter = os.path.splitdrive(directory)[0]

        if drive_letter:
            drive_display = f"Drive {drive_letter[-1].upper()}"
        else:
            drive_display = "Root Directory"

        disk_space_frame = ctk.CTkFrame(app, corner_radius=10)
        disk_space_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(disk_space_frame, text="Disk Space Analysis:", font=("Arial", 14)).pack(pady=(10, 5))
        ctk.CTkLabel(disk_space_frame, text=f"Directory: {drive_display}").pack()
        ctk.CTkLabel(disk_space_frame, text=f"Total Space: {disk_usage.total / (1024.0 ** 3):.2f} GB").pack()
        ctk.CTkLabel(disk_space_frame, text=f"Used Space: {disk_usage.used / (1024.0 ** 3):.2f} GB ({disk_usage.percent}%)").pack()
        ctk.CTkLabel(disk_space_frame, text=f"Free Space: {disk_usage.free / (1024.0 ** 3):.2f} GB").pack()

    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")
        log_textbox.insert(tk.END, f"Error: {e}\n")




app = ctk.CTk()
app.title("File Organizer")
app.geometry("1010x650")
app._set_appearance_mode("System")

# ----------------------------------------
# **Top Frame**
# ----------------------------------------
top_frame = ctk.CTkFrame(app, corner_radius=10)
top_frame.pack(pady=20, fill="x")


# ----------------------------------------
# **Left Top Frame (Input and Buttons)**
# ----------------------------------------
left_top_frame = ctk.CTkFrame(top_frame)
left_top_frame.pack(side="left", padx=20, pady=10)

# **Directory Input**
label = ctk.CTkLabel(left_top_frame, text="Enter your directory location:")
label.pack(padx=0, pady=10)

textbox = ctk.CTkTextbox(left_top_frame, height=50, width=375)
textbox.pack(padx=20, pady=10)

# **Action Buttons**
button_frame = ctk.CTkFrame(left_top_frame, width=370)
button_frame.pack()

delete_duplicates_button = ctk.CTkButton(
button_frame, text="Delete Duplicates & Organize Folder", corner_radius=15, command=delete_duplicates_and_organize
)
delete_duplicates_button.pack(side="left", padx=10)

organize_button = ctk.CTkButton(
button_frame, text="Organize Folder", corner_radius=15, command=only_organize
)
organize_button.pack(side="left", padx=10)

# **Status Label**
status_label = ctk.CTkLabel(left_top_frame, text="", height=30)
status_label.pack(pady=(0, 20))


# ----------------------------------------
# **Right Top Frame (Log)**
# ----------------------------------------
right_top_frame = ctk.CTkFrame(top_frame)
right_top_frame.pack(side="right", padx=20, pady=10)

# **Log Label and Textbox**
log_label = ctk.CTkLabel(right_top_frame, text="File Organization Log:")
log_label.pack()

log_textbox = ctk.CTkTextbox(right_top_frame, height=200, width=400)
log_textbox.configure(state=ctk.DISABLED)
log_textbox.pack(padx=20, pady=10)



# ----------------------------------------
# **Bottom Frame (Disk Space Analysis)**
# ----------------------------------------
bottom_frame = ctk.CTkFrame(app, corner_radius=10)
bottom_frame.pack(pady=20, fill="x")

# **Disk Space Analysis Label and Button**
disk_space_label = ctk.CTkLabel(bottom_frame, text="Disk Space Analysis:")
disk_space_label.pack(pady=(10, 5))

disk_space_button = ctk.CTkButton(
    bottom_frame, text="Analyze Disk Space", corner_radius=15, command=lambda: disk_space_analysis(textbox.get("1.0", "end-1c").strip())
)
disk_space_button.pack(pady=10)

app.mainloop()