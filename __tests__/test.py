import customtkinter as ctk
import os
import time
from datetime import datetime

class CleanupTab:
    def setup_cleanup_tab(self):
        # Main frame for the cleanup tab
        self.tab_cleanup.grid_columnconfigure(0, weight=1)
        
        # Directory selection frame
        options_frame = ctk.CTkFrame(self.tab_cleanup)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(options_frame, text="Directory to clean:").pack(side="left", padx=5)
        self.cleanup_entry = ctk.CTkEntry(options_frame, width=400)
        self.cleanup_entry.pack(side="left", padx=5)
        
        # Browse button
        browse_btn = ctk.CTkButton(options_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side="left", padx=5)
        
        # Cleanup options frame
        self.cleanup_options = ctk.CTkFrame(self.tab_cleanup)
        self.cleanup_options.pack(fill="x", padx=10, pady=5)
        
        # Cleanup options with variables
        self.empty_folders_var = ctk.BooleanVar(value=True)
        self.old_files_var = ctk.BooleanVar(value=True)
        self.days_threshold = ctk.IntVar(value=30)
        
        # Checkboxes and options
        ctk.CTkCheckBox(self.cleanup_options, 
                       text="Remove empty folders", 
                       variable=self.empty_folders_var).pack(anchor="w", pady=2)
        
        age_frame = ctk.CTkFrame(self.cleanup_options)
        age_frame.pack(anchor="w", fill="x", pady=2)
        
        ctk.CTkCheckBox(age_frame, 
                       text="Remove files older than", 
                       variable=self.old_files_var).pack(side="left", padx=5)
        
        ctk.CTkEntry(age_frame, 
                    width=50, 
                    textvariable=self.days_threshold).pack(side="left", padx=5)
        
        ctk.CTkLabel(age_frame, text="days").pack(side="left", padx=5)
        
        # Start button
        start_btn = ctk.CTkButton(self.cleanup_options, 
                                 text="Start cleanup process", 
                                 command=self.perform_cleanup)
        start_btn.pack(pady=10)
        
        # Results textbox
        self.cleanup_results = ctk.CTkTextbox(self.tab_cleanup, height=200)
        self.cleanup_results.pack(fill="both", expand=True, padx=10, pady=5)

    def browse_directory(self):
        directory = ctk.filedialog.askdirectory()
        if directory:
            self.cleanup_entry.delete(0, 'end')
            self.cleanup_entry.insert(0, directory)

    def perform_cleanup(self):
        directory = self.cleanup_entry.get()
        
        # Validate directory
        if not directory or not os.path.isdir(directory):
            self.cleanup_results.delete("1.0", "end")
            self.cleanup_results.insert("end", "Error: Please select a valid directory\n")
            return
        
        # Initialize counters
        removed_count = 0
        saved_space = 0
        
        # Clear previous results
        self.cleanup_results.delete("1.0", "end")
        self.cleanup_results.insert("end", f"Starting cleanup of {directory}...\n")
        self.cleanup_results.update()
        
        try:
            # Calculate threshold date
            days_old = self.days_threshold.get()
            threshold_time = time.time() - (days_old * 24 * 3600)
            
            # Walk through directory
            for root, dirs, files in os.walk(directory, topdown=False):
                # Remove old files
                if self.old_files_var.get():
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_mtime = os.path.getmtime(file_path)
                            
                            if file_mtime < threshold_time:
                                size = os.path.getsize(file_path)
                                os.remove(file_path)
                                removed_count += 1
                                saved_space += size
                                
                                # Format the date for display
                                date_str = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
                                self.cleanup_results.insert("end", 
                                    f"Removed file: {file_path} (Last modified: {date_str})\n")
                                self.cleanup_results.see("end")
                                self.cleanup_results.update()
                        
                        except Exception as e:
                            self.cleanup_results.insert("end", f"Error processing {file}: {str(e)}\n")
                            self.cleanup_results.update()
                            continue
                
                # Remove empty folders
                if self.empty_folders_var.get():
                    try:
                        if not os.listdir(root):
                            os.rmdir(root)
                            removed_count += 1
                            self.cleanup_results.insert("end", f"Removed empty folder: {root}\n")
                            self.cleanup_results.see("end")
                            self.cleanup_results.update()
                    
                    except Exception as e:
                        self.cleanup_results.insert("end", f"Error processing folder {root}: {str(e)}\n")
                        self.cleanup_results.update()
                        continue
            
            # Show summary
            mb_saved = saved_space / (1024 * 1024)
            self.cleanup_results.insert("end", f"\nCleanup completed:\n")
            self.cleanup_results.insert("end", f"- Removed {removed_count} items\n")
            self.cleanup_results.insert("end", f"- Saved {mb_saved:.2f} MB of space\n")
            self.cleanup_results.see("end")
        
        except Exception as e:
            self.cleanup_results.insert("end", f"\nError during cleanup: {str(e)}\n")
        
        self.cleanup_results.update()