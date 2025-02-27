import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
from datetime import datetime
import zipfile
import shutil
import webbrowser

class IL2JoyBackup:
    def __init__(self, root):
        self.root = root
        self.root.title("IL-2 JoyBackup")  # Updated program name
        
        # Define themes
        self.dark_theme = {
            "bg_color": "#2d2d2d",  # Dark background
            "fg_color": "#ffffff",  # White text
            "btn_bg_color": "#3c3c3c",  # Dark button background
            "btn_fg_color": "#ffffff",  # White button text
            "terminal_bg": "#1e1e1e",  # Dark terminal background
            "terminal_fg": "#ffffff",  # White terminal text
            "popup_bg": "#2d2d2d",  # Dark popup background
            "popup_fg": "#ffffff",  # White popup text
        }
        self.light_theme = {
            "bg_color": "#f0f0f0",  # Light background
            "fg_color": "#000000",  # Black text
            "btn_bg_color": "#e0e0e0",  # Light button background
            "btn_fg_color": "#000000",  # Black button text
            "terminal_bg": "#ffffff",  # Light terminal background
            "terminal_fg": "#000000",  # Black terminal text
            "popup_bg": "#f0f0f0",  # Light popup background
            "popup_fg": "#000000",  # Black popup text
        }
        
        # Set default theme (dark)
        self.current_theme = self.dark_theme
        
        # Files to be managed
        self.files = {
            "current.map": {"content": "", "path": None},
            "devices.txt": {"content": "", "path": None},
            "global.actions": {"content": "", "path": None},
            "current.responses": {"content": "", "path": None},
        }
        
        # Temporary directory for backups
        self.temp_dir = os.path.join(os.getcwd(), "temp_backup")  # Create a temporary directory in the current working directory
        os.makedirs(self.temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Initialize UI
        self.setup_ui()
        
        # Apply theme after UI is set up
        self.apply_theme()
    
    def setup_ui(self):
        # Top frame for help and theme buttons
        self.top_frame = tk.Frame(self.root, bg=self.current_theme["bg_color"])
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Theme toggle button (right side)
        self.theme_btn = tk.Button(
            self.top_frame, text="Toggle Theme", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        
        # Help button (right side, next to theme button)
        self.help_btn = tk.Button(
            self.top_frame, text="?", font=("Arial", 12), 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.show_help
        )
        self.help_btn.pack(side=tk.RIGHT, padx=5)
        
        # Control panel
        self.control_frame = tk.Frame(self.root, bg=self.current_theme["bg_color"])
        self.control_frame.pack(pady=10)
        
        # Open Folder button and description
        self.open_btn = tk.Button(
            self.control_frame, text="Open Folder", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.open_folder
        )
        self.open_btn.grid(row=0, column=0, padx=5, pady=5)
        self.open_label = tk.Label(
            self.control_frame,
            text="Start here, open your input folder.\nUsually located at:\nC:\Program Files\IL-2 Sturmovik Great Battles\data\input",
            justify=tk.LEFT, bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"]
        )
        self.open_label.grid(row=1, column=0, padx=5, pady=5)
        
        # Backup Controls button and description
        self.backup_btn = tk.Button(
            self.control_frame, text="Backup Controls", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.backup_files
        )
        self.backup_btn.grid(row=0, column=1, padx=5, pady=5)
        self.backup_label = tk.Label(
            self.control_frame, 
            text="Create a backup of all control files as a zip.",
            bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"]
        )
        self.backup_label.grid(row=1, column=1, padx=5, pady=5)
        
        # Import Backup button and description
        self.import_backup_btn = tk.Button(
            self.control_frame, text="Import Backup", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.import_backup
        )
        self.import_backup_btn.grid(row=0, column=2, padx=5, pady=5)
        self.import_label = tk.Label(
            self.control_frame, 
            text="Import a backup zip file.",
            bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"]
        )
        self.import_label.grid(row=1, column=2, padx=5, pady=5)
        
        # Restore Backup button and description
        self.restore_backup_btn = tk.Button(
            self.control_frame, text="Restore Backup", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=self.restore_backup
        )
        self.restore_backup_btn.grid(row=0, column=3, padx=5, pady=5)
        self.restore_label = tk.Label(
            self.control_frame, 
            text="Restore backup files to their original location.",
            bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"]
        )
        self.restore_label.grid(row=1, column=3, padx=5, pady=5)
        
        # Terminal (text area for logs)
        self.terminal = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", 
            height=10, bg=self.current_theme["terminal_bg"], fg=self.current_theme["terminal_fg"]
        )
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def apply_theme(self):
        """Apply the current theme to all UI elements."""
        self.root.configure(bg=self.current_theme["bg_color"])
        self.top_frame.configure(bg=self.current_theme["bg_color"])
        self.control_frame.configure(bg=self.current_theme["bg_color"])
        
        # Update buttons
        self.help_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        self.theme_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        self.open_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        self.backup_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        self.import_backup_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        self.restore_backup_btn.configure(bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"])
        
        # Update labels
        self.open_label.configure(bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"])
        self.backup_label.configure(bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"])
        self.import_label.configure(bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"])
        self.restore_label.configure(bg=self.current_theme["bg_color"], fg=self.current_theme["fg_color"])
        
        # Update terminal
        self.terminal.configure(bg=self.current_theme["terminal_bg"], fg=self.current_theme["terminal_fg"])
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        if self.current_theme == self.dark_theme:
            self.current_theme = self.light_theme
        else:
            self.current_theme = self.dark_theme
        self.apply_theme()
    
    def log_message(self, message):
        """Add a message to the terminal."""
        self.terminal.config(state="normal")  # Enable editing
        self.terminal.insert(tk.END, message + "\n")  # Add the message
        self.terminal.config(state="disabled")  # Disable editing
        self.terminal.see(tk.END)  # Scroll to the end
    
    def show_help(self):
        """Show a help message with program details."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.configure(bg=self.current_theme["popup_bg"])
        
        help_text = """
        IL-2 JoyBackup
        --------------
        This program helps you manage control files for IL-2 Sturmovik Great Battles.

        Features:
        1. Open Folder: Load control files from a folder.
        2. Backup Controls: Create a backup of all control files as a zip.
        3. Import Backup: Import a backup zip file.
        4. Restore Backup: Restore backup files to their original location.

        How to Use:
        - Open Folder: Select the folder containing your control files.
        - Backup Controls: Create a backup of all control files.
        - Import Backup: Import a previously created backup.
        - Restore Backup: Restore files from the imported backup.

        Created by: LLv24_StableAce
        YouTube: https://youtube.com/@stableace6661
        """
        help_label = tk.Label(
            help_window, text=help_text, justify=tk.LEFT,
            bg=self.current_theme["popup_bg"], fg=self.current_theme["popup_fg"]
        )
        help_label.pack(padx=10, pady=10)
        
        # Button to open YouTube link
        youtube_btn = tk.Button(
            help_window, text="Check my YouTube", 
            bg=self.current_theme["btn_bg_color"], fg=self.current_theme["btn_fg_color"],
            command=lambda: webbrowser.open("https://youtube.com/@stableace6661")
        )
        youtube_btn.pack(pady=10)
    
    def open_folder(self):
        """Open a folder and load files."""
        # Suggest the default IL-2 input folder
        default_folder = "C:\\Program Files\\IL-2 Sturmovik Great Battles\\data\\input"
        folder_path = filedialog.askdirectory(
            title="Select Folder with Control Files",
            initialdir=default_folder if os.path.exists(default_folder) else os.getcwd()
        )
        if not folder_path:
            return
        
        self.log_message(f"Working directory: {folder_path}")
        self.load_files_from_folder(folder_path)
        self.log_message("Files loaded successfully!")
    
    def load_files_from_folder(self, folder_path):
        """Load files from the selected folder."""
        expected_files = ["current.map", "devices.txt", "global.actions", "current.responses"]
        loaded_files = []
        
        for file_name in expected_files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        self.files[file_name]["content"] = content
                        self.files[file_name]["path"] = file_path
                        loaded_files.append(file_name)
                except Exception as e:
                    self.log_message(f"Failed to open {file_name}: {e}")
            else:
                self.log_message(f"Warning: {file_name} not found in {folder_path}")
    
    def backup_files(self):
        """Create a backup of all control files."""
        # Check if all files are loaded
        if not all(data["path"] for data in self.files.values()):
            self.log_message("Backup Warning: Please load all files first!")
            return

        # Create a zip file with the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{timestamp}_joystick_Backup.zip"
        backup_dir = os.path.dirname(next(data["path"] for data in self.files.values()))  # Get the folder path
        zip_path = os.path.join(backup_dir, zip_filename)

        try:
            # Create a zip file and add the files
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file_name, data in self.files.items():
                    file_path = data["path"]
                    zipf.write(file_path, os.path.basename(file_path))  # Add the file to the zip
            self.log_message(f"Backup created successfully: {zip_path}")
        except Exception as e:
            self.log_message(f"Failed to create backup: {e}")
    
    def import_backup(self):
        """Import a backup zip file."""
        # Ask the user to select a zip file
        zip_path = filedialog.askopenfilename(
            title="Select Backup Zip File",
            filetypes=[("Zip Files", "*.zip"), ("All Files", "*.*")]
        )
        if not zip_path:
            return

        # Check if the selected file is a zip file
        if not zip_path.endswith(".zip"):
            self.log_message("Error: Please select a valid zip file!")
            return

        # Extract the zip file to the temporary directory
        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(self.temp_dir)
            self.log_message(f"Backup imported successfully from: {zip_path}")
        except Exception as e:
            self.log_message(f"Failed to import backup: {e}")
    
    def restore_backup(self):
        """Restore backup files to their original location."""
        # Check if the temporary directory exists
        if not os.path.exists(self.temp_dir):
            self.log_message("Restore Warning: No backup files found to restore!")
            return

        # Ask the user to select the destination folder
        dest_folder = filedialog.askdirectory(
            title="Select Destination Folder for Restore",
            initialdir=os.path.dirname(next(data["path"] for data in self.files.values())) if any(data["path"] for data in self.files.values()) else os.getcwd()
        )
        if not dest_folder:
            self.log_message("Restore canceled: No destination folder selected.")
            return

        # Check if the destination folder is valid
        if not os.path.isdir(dest_folder):
            self.log_message(f"Error: {dest_folder} is not a valid directory!")
            return

        # Move files back to their original location
        try:
            for file_name in self.files:
                source_path = os.path.join(self.temp_dir, file_name)
                if os.path.exists(source_path):
                    dest_path = os.path.join(dest_folder, file_name)
                    shutil.move(source_path, dest_path)
                    self.files[file_name]["path"] = dest_path  # Update the path
            self.log_message("Backup files restored successfully!")
        except Exception as e:
            self.log_message(f"Failed to restore backup: {e}")
        finally:
            # Delete the temporary directory
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            os.makedirs(self.temp_dir, exist_ok=True)  # Recreate the temporary directory

if __name__ == "__main__":
    root = tk.Tk()
    app = IL2JoyBackup(root)
    root.mainloop()