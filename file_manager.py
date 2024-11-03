import os
import shutil
import time
import tkinter as tk
import customtkinter as ctk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
from datetime import datetime

class FileManagerApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Advanced File Organizer")
        self.app.geometry("1200x800")
        self._create_ui()

    def _create_ui(self):
        # the main container
        self.main_container = ctk.CTkFrame(self.app)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)

        custom_font = ("Yu Gothic UI", 18, 'normal')

        # tab style view
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=25)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabview._segmented_button.configure(font=custom_font)

        self.tab_organizer = self.tabview.add(" Organizer ")
        self.tab_monitor = self.tabview.add(" Monitor ")
        self.tab_analysis = self.tabview.add(" Disk Analysis ")
        self.tab_temp_cleanup = self.tabview.add(" Temp cleanup ")
        self.tab_cleanup = self.tabview.add(" File cleanup ")

        self._setup_organizer_tab()
        self._setup_monitor_tab()
        self._setup_analysis_tab()
        self._setup_cleanup_tab()
        self._setup_temp_cleanup_tab()


    def _setup_organizer_tab(self):
        # here you enter dir path
        input_frame = ctk.CTkFrame(self.tab_organizer)
        input_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Enter directory path:").pack(side="left", padx=5);
        self.dir_entry = ctk.CTkEntry(input_frame, width=400)
        self.dir_entry.pack(side="left", padx=5)

        # buttons
        btn_frame = ctk.CTkFrame(self.tab_organizer)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="Organize Files", command=self._organize_files).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Remove Duplicates", command=self._remove_duplicates).pack(side="left", padx=5)

        # the logger for organizer
        log_frame = ctk.CTkFrame(self.tab_organizer)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(log_frame, text="Organization log:").pack()
        self.org_log = ctk.CTkTextbox(log_frame, height=300)
        self.org_log.pack(fill="both", expand=True, padx=5, pady=5)


    def _setup_monitor_tab(self):
        control_frame = ctk.CTkFrame(self.tab_monitor)
        control_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(control_frame, text="Directory to monitor:").pack(side="left", padx=5)
        self.monitor_entry = ctk.CTkEntry(control_frame, width=400)
        self.monitor_entry.pack(side="left", padx=5)

        self.monitor_btn = ctk.CTkButton(control_frame, text="Start Monitoring", command=self._toggle_monitoring)
        self.monitor_btn.pack(side="left", padx=5)

        #logger for monitor
        log_frame = ctk.CTkFrame(self.tab_monitor)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.monitor_log = ctk.CTkTextbox(log_frame, height=400)
        self.monitor_log.pack(fill="both", expand=True, padx=5, pady=5)


    def _setup_analysis_tab(self):
        control_frame = ctk.CTkFrame(self.tab_analysis)
        control_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(control_frame, text="Directory to analyze:").pack(side="left", padx=5)
        self.analysis_entry = ctk.CTkEntry(control_frame, width=400)
        self.analysis_entry.pack(side="left", padx=5)

        ctk.CTkButton(control_frame, text="Analyze", command=self._analyze_drive).pack(side="left", padx=5)

        self.analysis_frame = ctk.CTkScrollableFrame(self.tab_analysis)
        self.analysis_frame.pack(fill="both", expand=True, padx=10, pady=5)


    def _setup_cleanup_tab(self):
        options_frame = ctk.CTkFrame(self.tab_cleanup)
        options_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(options_frame, text="Directory to clean:").pack(side="left", padx=5)
        self.cleanup_entry = ctk.CTkEntry(options_frame, width=400)
        self.cleanup_entry.pack(side="left", padx=5)

        # all cleanup options
        self.cleanup_options = ctk.CTkFrame(self.tab_cleanup)
        self.cleanup_options.pack(fill="x", padx=10, pady=5)

        self.empty_folders_var = tk.BooleanVar(value=True)
        self.old_files_var = tk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.cleanup_options, text="Remove empty folders", variable=self.empty_folders_var).pack(anchor="w")

        ctk.CTkCheckBox(self.cleanup_options, text="Remove files older than 30 days", variable=self.old_files_var).pack(anchor="w")

        ctk.CTkButton(self.cleanup_options, text="Start cleanup process", command=self._perform_cleanup).pack(pady=10)

        self.cleanup_results = ctk.CTkTextbox(self.tab_cleanup, height=200)
        self.cleanup_results.pack(fill="both", expand=True, padx=10, pady=5)


    def _setup_temp_cleanup_tab(self):
        options_frame = ctk.CTkFrame(self.tab_temp_cleanup)
        options_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(options_frame, text="Enter username on the pc:").pack(side="left", padx=5)
        self.temp_cleanup_entry = ctk.CTkEntry(options_frame, width=400)
        self.temp_cleanup_entry.pack(side="left", padx=5)

        # all cleanup options
        self.temp_cleanup_options = ctk.CTkFrame(self.tab_temp_cleanup)
        self.temp_cleanup_options.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.temp_cleanup_options, text="Start cleanup process", command=self._perform_temp_cleanup).pack(pady=10)

        self.temp_cleanup_results = ctk.CTkTextbox(self.tab_temp_cleanup, height=200)
        self.temp_cleanup_results.pack(fill="both", expand=True, padx=10, pady=5)


    def _organize_files(self):
        self.org_log.insert(tk.END, "Sorting...\n")
        self.app.update_idletasks()
        self.org_log.delete("1.0", tk.END)
        self.org_log.configure(state=tk.NORMAL)
    
        directory = os.path.abspath(os.path.normpath(self.dir_entry.get().strip()))
        try:
            if not os.path.isdir(directory):
                raise FileNotFoundError("Invalid directory path. Please try again.")
        
            os.chdir(directory)
            current_dir = os.getcwd()
            self.org_log.insert(tk.END, f"Current Directory: {current_dir}\n")

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

                    for dir_name, extensions in file_types.items():
                        if file_ext in extensions:
                            dest_dir = os.path.join(current_dir, dir_name)
                            break
                    else:
                        dest_dir = os.path.join(current_dir, "Others")
                    
                    dest_path = os.path.join(dest_dir, file)
                
                    if os.path.exists(dest_path):
                        base, extension = os.path.splitext(file)
                        counter = 1
                        new_file = f"{base}_{counter}{extension}"
                        dest_path = os.path.join(dest_dir, new_file)

                        while os.path.exists(dest_path):
                            counter += 1
                            new_file = f"{base}_{counter}{extension}"
                            dest_path = os.path.join(dest_dir, new_file)
                
                    shutil.move(file, dest_dir)
                    self.org_log.insert(tk.END, f"Moved '{file}' to '{dest_dir}'\n")

            self.org_log.insert(tk.END, "Sorting Completed...\n")

        except FileNotFoundError as e:
            self.org_log.insert(tk.END, f"Error: {e}\n")
        except Exception as e:
            self.org_log.insert(tk.END, f"Error: {e}\n")
        finally:
            self.org_log.configure(state=tk.DISABLED)
        self.app.update_idletasks()


    import os

    def _remove_duplicates(self):
        directory = os.path.abspath(os.path.normpath(self.dir_entry.get().strip()))

        self.org_log.insert("end", f"Removing duplicates in {directory}...\n")
        try:
            current = directory  # Directly use the directory
            print(f"Current Directory: {current}")

            file_dict = {}

            # Recursive file listing
            for root, dirs, files in os.walk(current):
                for file in files:
                    full_path = os.path.join(root, file)
                    file_size = os.path.getsize(full_path)
                    if file_size in file_dict:
                        file_dict[file_size].append(full_path)
                    else:
                        file_dict[file_size] = [full_path]

            for file_size, file_list in file_dict.items():
                if len(file_list) > 1:
                    original_file = file_list[0]
                    for duplicate_file in file_list[1:]:
                        os.remove(duplicate_file)
                        print(f"Deleted duplicate file: {duplicate_file}")
                        self.org_log.insert(tk.END, f"Deleted duplicate file: {duplicate_file}\n")

        except Exception as e:
            # Handle exceptions gracefully
            print(f"An error occurred: {e}")
            self.org_log.insert(tk.END, f"An error occurred: {e}\n")
    
    def _toggle_monitoring(self):
        if self.monitor_btn.cget("text") == "Start Monitoring":
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self):
        dir = self.monitor_entry.get()
        if not os.path.isdir(dir):
            self.monitor_log.insert("end", "Invalid directory path\n")
            return

        # Define handler for file system events
        class Handler(FileSystemEventHandler):
            def __init__(self, app):
                self.app = app

            def on_any_event(self, event):
                if event.is_directory:
                    return
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.app.monitor_log.insert("end", f"{timestamp} - {event.event_type}: {event.src_path}\n")
                self.app.monitor_log.see("end")

        # Set up observer and handler
        self.observer = Observer()
        self.observer.schedule(Handler(self), dir, recursive=False)
        self.observer.start()
        self.monitor_btn.configure(text="Stop Monitoring")
        self.monitor_log.insert("end", f"Started monitoring {dir}\n")

    def stop_monitoring(self):
        if hasattr(self, 'observer') and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        self.monitor_btn.configure(text="Start Monitoring")
        self.monitor_log.insert("end", f"Stopped monitoring {self.monitor_entry.get()}\n")

    
    def _analyze_drive(self):
        directory = os.path.abspath(os.path.normpath(self.analysis_entry.get().strip()))

        status_label = ctk.CTkLabel(self.analysis_frame, text="")
        status_label.pack(pady=5)

        if not os.path.isdir(directory):
            status_label.configure(text="Invalid directory path.", text_color="red")
            return

        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
    
        try:
            disk_usage = psutil.disk_usage(directory)

            drive_letter = os.path.splitdrive(directory)[0]
            if drive_letter:
                    drive_display = f"Drive {drive_letter[-1].upper()}"
            else:
                    drive_display = "Root Directory"

            ctk.CTkLabel(self.analysis_frame, text="Disk Space Analysis:", font=("Arial", 14)).pack(pady=(10, 5))
            ctk.CTkLabel(self.analysis_frame, text=f"Directory: {drive_display}").pack()
            ctk.CTkLabel(self.analysis_frame, text=f"Total Space: {disk_usage.total / (1024.0 ** 3):.2f} GB").pack()
            ctk.CTkLabel(self.analysis_frame, text=f"Used Space: {disk_usage.used / (1024.0 ** 3):.2f} GB ({disk_usage.percent}%)").pack()
            ctk.CTkLabel(self.analysis_frame, text=f"Free Space: {disk_usage.free / (1024.0 ** 3):.2f} GB").pack()

        except Exception as e:
            status_label.configure(text=f"Error: {e}", text_color="red")


    def _perform_temp_cleanup(self):
        username = self.temp_cleanup_entry.get()
        if not username:
            self.temp_cleanup_results.insert("end", "Please enter a valid username\n")
            return

        # Define the temp directories
        temp_dirs = [
            f"C:\\Users\\{username}\\AppData\\Local\\Temp",
            "C:\\Windows\\Temp"
        ]

        removed_count = 0
        saved_space = 0
        self.temp_cleanup_results.delete("1.0", "end")
        self.temp_cleanup_results.insert("end", "Starting cleanup...\n")

        for temp_dir in temp_dirs:
            if not os.path.isdir(temp_dir):
                self.temp_cleanup_results.insert("end", f"Invalid directory: {temp_dir}\n")
                continue
    
            # Remove ALL temp files
            for root, dirs, files in os.walk(temp_dir):  
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        removed_count += 1
                        saved_space += file_size
                        self.temp_cleanup_results.insert("end", f"Removed file: {file_path}\n")
                            
                    except Exception as e:
                        self.temp_cleanup_results.insert("end", f"Failed to remove {file_path}: {str(e)}\n")

        self.temp_cleanup_results.insert("end", 
                            f"\nCleanup completed:\n"
                            f"- Removed {removed_count} items\n"
                            f"Saved {saved_space / (1024*1024):.2f} MB of space\n"
                           )
        
    def _perform_cleanup(self):
        directory = os.path.abspath(os.path.normpath(self.cleanup_entry.get().strip()))
        removed_count = 0
        saved_space = 0
        try:
            print(f"Directory path: {directory}")
            
            if not os.path.isdir(directory):
                raise FileNotFoundError("Invalid directory path. Please try again.")
            
            self.cleanup_results.delete("1.0", "end")
            self.cleanup_results.insert("end", "Starting cleanup...\n")
            
            # First pass: Remove old files
            if self.old_files_var.get():
                for root, dirs, files in os.walk(directory, topdown=False):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if time.time() - os.path.getmtime(file_path) > 30 * 24 * 3600:
                                size = os.path.getsize(file_path)
                                os.remove(file_path)
                                removed_count += 1
                                saved_space += size
                                self.cleanup_results.insert("end", f"Removed old file: {file_path}\n")
                        except Exception as e:
                            continue
            
            # Second pass: Remove empty folders
            if self.empty_folders_var.get():
                for root, dirs, files in os.walk(directory, topdown=False):
                    try:
                        if not os.listdir(root):
                            os.rmdir(root)
                            removed_count += 1
                            self.cleanup_results.insert("end", f"Removed empty folder: {root}\n")
                            self.cleanup_results.see("end")
                            self.cleanup_results.update()
                    except Exception as e:
                        continue

        except FileNotFoundError as e:
            self.cleanup_results.insert("end", f"Error: {e}\n")
        except Exception as e:
            self.cleanup_results.insert("end", f"Error: {e}\n")
        finally:
            self.cleanup_results.insert(
                "end",
                f"\nCleanup completed:\n"
                f"- Removed {removed_count} items\n"
                f"- Saved {saved_space / (1024*1024):.2f} MB of space\n"
            )

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = FileManagerApp()
    app.run()