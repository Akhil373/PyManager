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

        # tab style view
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_organizer = self.tabview.add("File Organizer")
        self.tab_monitor = self.tabview.add("File monitor")
        self.tab_analysis = self.tabview.add("Disk Space Analysis")
        self.tab_cleanup = self.tabview.add("File cleanup")

        self._setup_organizer_tab()
        self._setup_monitor_tab()
        self._setup_analysis_tab()
        self._setup_cleanup_tab()

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

        self.temp_files_var = tk.BooleanVar(value=True)
        self.empty_folders_var = tk.BooleanVar(value=True)
        self.old_files_var = tk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.cleanup_options, text="Remove temporary files", variable=self.temp_files_var).pack(anchor="w")

        ctk.CTkCheckBox(self.cleanup_options, text="Remove empty folders", variable=self.empty_folders_var).pack(anchor="w")

        ctk.CTkCheckBox(self.cleanup_options, text="Remove files older than 30 days", variable=self.old_files_var).pack(anchor="w")

        ctk.CTkButton(self.cleanup_options, text="Start cleanup process", command=self._perform_cleanup).pack(pady=10)

        self.cleanup_results = ctk.CTkTextbox(self.tab_cleanup, height=200)
        self.cleanup_results.pack(fill="both", expand=True, padx=10, pady=5)

    def _organize_files(self):
        self.org_log.insert(tk.END, "Sorting...\n")
        self.app.update_idletasks()
        self.org_log.delete("1.0", tk.END)
        self.org_log.configure(state=tk.NORMAL)
    
        directory = self.dir_entry.get()
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
                
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                        self.org_log.insert(tk.END, f"Created directory: {dest_dir}\n")
                
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


    def _remove_duplicates(self):
        directory = self.dir_entry.get()

        self.org_log.insert("end", f"Removing duplicates in {directory}...\n")
        try:
            os.chdir(directory)
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
                        self.org_log.insert(tk.END, f"Deleted duplicate file: {duplicate_file}\n")

        except Exception as e:
            self.org_log.insert(text=f"Error: {e}")
            print(e)
    
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
        directory = self.analysis_entry.get()

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


    def _perform_cleanup(self):
        username = self.cleanup_entry.get()  # Assume there's an entry widget for the username
        if not username:
            self.cleanup_results.insert("end", "Please enter a valid username\n")
            return

        # Define the temp directories
        temp_dirs = [
            f"C:\\Users\\{username}\\AppData\\Local\\Temp",
            "C:\\Windows\\Temp"
        ]

        removed_count = 0
        saved_space = 0
        self.cleanup_results.delete("1.0", "end")
        self.cleanup_results.insert("end", "Starting cleanup...\n")

        for temp_dir in temp_dirs:
            if not os.path.isdir(temp_dir):
                self.cleanup_results.insert("end", f"Invalid directory: {temp_dir}\n")
                continue
    
            # Remove ALL temp files
            if self.temp_files_var.get():
                for root, dirs, files in os.walk(temp_dir):  
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            removed_count += 1
                            saved_space += file_size
                            self.cleanup_results.insert("end", f"Removed file: {file_path}\n")
                            
                        except Exception as e:
                            self.cleanup_results.insert("end", f"Failed to remove {file_path}: {str(e)}\n")


            # to remove older files
            if self.old_files_var.get():
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if time.time() - os.path.getmtime(file_path) > 30*24*3600:
                            size = os.path.getsize(file_path)
                            os.remove(file_path)
                            removed_count += 1
                            saved_space += size
                            self.cleanup_results.insert("end", f"Removed old file: {file_path}\n")
                    except:
                        continue
                    
            # to remove empty folders
            if self.empty_folders_var.get():
                if not os.listdir(root):
                    try:
                        os.rmdir(root)
                        removed_count += 1
                        self.cleanup_results.insert("end", f"Removed empty folder: {root}\n")
                    except:
                        continue

        self.cleanup_results.insert("end", 
                            f"\nCleanup completed:\n"
                            f"- Removed {removed_count} items\n"
                            f"Saved {saved_space / (1024*1024):.2f} MB of space\n"
                           )

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = FileManagerApp()
    app.run()