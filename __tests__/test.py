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