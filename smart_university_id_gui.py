

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import math
from typing import Optional, Tuple, List
from smart_university_id_system import (
    HashTable, Trie, LogQueue, Graph, Student
)


class SmartUniversityGUI:
    """Main GUI application class."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart University ID & Verification System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize backend systems
        self.students = HashTable()
        self.trie = Trie()
        self.logs = LogQueue()
        self.graph = Graph()
        
        # Load example data
        self._load_example_data()
        
        # Style configuration
        self._setup_styles()
        
        # Create main dashboard
        self._create_dashboard()
    
    def _setup_styles(self):
        """Configure modern styling."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Action.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        style.configure('Primary.TButton',
                       font=('Segoe UI', 9),
                       padding=8)
    
    def _load_example_data(self):
        """Load example test data for demonstration."""
        # Add 5 students
        demo_students = [
            (101, "Awais Khan", "CS", "2025"),
            (102, "Alice Johnson", "Math", "2024"),
            (103, "Ahmad Raza", "EE", "2026"),
            (104, "Karen Smith", "Physics", "2023"),
            (105, "Khalid Hussain", "CS", "2025"),
        ]
        
        for sid, name, dept, batch in demo_students:
            self.students.insert_student(sid, name, dept, batch)
            self.trie.insert(name)
        
        # Add 5 logs with different timestamps
        base_time = time.time() - 3600  # 1 hour ago
        demo_logs = [
            (101, "Library", base_time),
            (102, "Cafeteria", base_time + 600),
            (103, "Main Gate", base_time + 1200),
            (104, "Lab A", base_time + 1800),
            (105, "Auditorium", base_time + 2400),
        ]
        
        for log in demo_logs:
            self.logs.enqueue(log)
        
        # Add 4 blocks and paths
        blocks = ["Main Gate", "Library", "Cafeteria", "Lab A"]
        for b in blocks:
            self.graph.add_block(b)
        
        self.graph.add_path("Main Gate", "Library", 5.0)
        self.graph.add_path("Library", "Cafeteria", 3.0)
        self.graph.add_path("Cafeteria", "Lab A", 4.0)
        self.graph.add_path("Main Gate", "Lab A", 12.0)
    
    def _create_dashboard(self):
        """Create the main dashboard window."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Smart University ID & Verification System",
            font=('Segoe UI', 20, 'bold'),
            bg="#2c3e50",
            fg="white",
            pady=30
        )
        title_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0", padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button grid
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(expand=True)
        
        # Define buttons with icons (using Unicode symbols)
        buttons = [
            ("➕ Add Student", self._show_add_student, "#27ae60"),
            ("✓ Verify Student ID", self._show_verify_student, "#3498db"),
            ("🔍 Search by Name", self._show_search_name, "#9b59b6"),
            ("📝 Log Entry", self._show_log_entry, "#e67e22"),
            ("📋 Show Entry Logs", self._show_entry_logs, "#16a085"),
            ("🗺️ Shortest Path", self._show_shortest_path, "#c0392b"),
        ]
        
        # Create buttons in a grid
        row, col = 0, 0
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Segoe UI', 12, 'bold'),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief=tk.FLAT,
                cursor="hand2",
                width=25,
                height=3,
                padx=10,
                pady=10
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Exit button
        exit_btn = tk.Button(
            content_frame,
            text="🚪 Exit",
            command=self.root.quit,
            font=('Segoe UI', 11, 'bold'),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=20,
            pady=10
        )
        exit_btn.pack(pady=20)
    
    def _show_add_student(self):
        """Display Add Student screen."""
        # Create new window
        window = tk.Toplevel(self.root)
        window.title("Add Student")
        window.geometry("500x400")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Add New Student",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=20
        )
        header.pack()
        
        # Form frame
        form_frame = tk.Frame(window, bg="#f0f0f0", padx=40, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student ID
        tk.Label(form_frame, text="Student ID:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=10)
        id_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        id_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Department
        tk.Label(form_frame, text="Department:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=10)
        dept_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        dept_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Batch
        tk.Label(form_frame, text="Batch:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=10)
        batch_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        batch_entry.grid(row=3, column=1, pady=10, padx=10)
        
        def submit():
            try:
                student_id = int(id_entry.get().strip())
                name = name_entry.get().strip()
                department = dept_entry.get().strip()
                batch = batch_entry.get().strip()
                
                if not name or not department or not batch:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                if self.students.insert_student(student_id, name, department, batch):
                    self.trie.insert(name)
                    messagebox.showinfo("Success", f"Student {name} (ID: {student_id}) added successfully!")
                    window.destroy()
                else:
                    messagebox.showerror("Error", "Duplicate ID detected! Student ID already exists.")
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID! Please enter a valid number.")
        
        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="Submit",
            command=submit,
            font=('Segoe UI', 11, 'bold'),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=8
        )
        submit_btn.grid(row=4, column=0, columnspan=2, pady=30)
    
    def _show_verify_student(self):
        """Display Verify Student ID screen."""
        window = tk.Toplevel(self.root)
        window.title("Verify Student ID")
        window.geometry("500x300")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Verify Student ID",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=30
        )
        header.pack()
        
        # Input frame
        input_frame = tk.Frame(window, bg="#f0f0f0", padx=40)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(input_frame, text="Student ID:", font=('Segoe UI', 11), bg="#f0f0f0").pack(pady=10)
        id_entry = tk.Entry(input_frame, font=('Segoe UI', 12), width=25)
        id_entry.pack(pady=10)
        
        # Result label
        result_label = tk.Label(
            input_frame,
            text="",
            font=('Segoe UI', 11),
            bg="#f0f0f0",
            fg="#2c3e50",
            wraplength=400
        )
        result_label.pack(pady=20)
        
        def verify():
            try:
                student_id = int(id_entry.get().strip())
                student = self.students.search_student(student_id)
                
                if student:
                    result_label.config(
                        text=f"✓ Valid ID\n\nStudent: {student.name}\nDepartment: {student.department}\nBatch: {student.batch}",
                        fg="#27ae60"
                    )
                else:
                    result_label.config(
                        text="✗ Invalid or Fake ID\n\nThis Student ID does not exist in the system.",
                        fg="#e74c3c"
                    )
            except ValueError:
                result_label.config(
                    text="✗ Invalid Input\n\nPlease enter a valid Student ID number.",
                    fg="#e74c3c"
                )
        
        # Verify button
        verify_btn = tk.Button(
            input_frame,
            text="Verify",
            command=verify,
            font=('Segoe UI', 11, 'bold'),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=8
        )
        verify_btn.pack(pady=20)
    
    def _show_search_name(self):
        """Display Search by Name (Auto-complete) screen."""
        window = tk.Toplevel(self.root)
        window.title("Search Student by Name")
        window.geometry("600x500")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Search Student by Name",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=20
        )
        header.pack()
        
        # Input frame
        input_frame = tk.Frame(window, bg="#f0f0f0", padx=40)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="Enter name prefix:", font=('Segoe UI', 11), bg="#f0f0f0").pack(pady=5)
        name_entry = tk.Entry(input_frame, font=('Segoe UI', 12), width=30)
        name_entry.pack(pady=10)
        
        # Results frame
        results_frame = tk.Frame(window, bg="#f0f0f0", padx=40)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(results_frame, text="Matching Names:", font=('Segoe UI', 11, 'bold'), bg="#f0f0f0").pack(anchor="w", pady=5)
        
        results_text = scrolledtext.ScrolledText(
            results_frame,
            font=('Segoe UI', 10),
            height=15,
            width=50,
            wrap=tk.WORD,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1
        )
        results_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def search():
            prefix = name_entry.get().strip()
            if not prefix:
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "Please enter a name prefix to search.")
                return
            
            suggestions = self.trie.get_suggestions(prefix)
            results_text.delete(1.0, tk.END)
            
            if suggestions:
                results_text.insert(tk.END, f"Found {len(suggestions)} match(es):\n\n")
                for i, name in enumerate(suggestions, 1):
                    results_text.insert(tk.END, f"{i}. {name}\n")
            else:
                results_text.insert(tk.END, "No matches found.\n\nTry a different prefix.")
        
        # Search button
        search_btn = tk.Button(
            input_frame,
            text="Search",
            command=search,
            font=('Segoe UI', 11, 'bold'),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=8
        )
        search_btn.pack(pady=10)
        
        # Auto-search on typing (optional enhancement)
        def on_key_release(event):
            if name_entry.get().strip():
                search()
        
        name_entry.bind('<KeyRelease>', on_key_release)
    
    def _show_log_entry(self):
        """Display Log Entry screen."""
        window = tk.Toplevel(self.root)
        window.title("Log Entry")
        window.geometry("500x350")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Log Entry",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=20
        )
        header.pack()
        
        # Form frame
        form_frame = tk.Frame(window, bg="#f0f0f0", padx=40, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student ID
        tk.Label(form_frame, text="Student ID:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=15)
        id_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        id_entry.grid(row=0, column=1, pady=15, padx=10)
        
        # Location
        tk.Label(form_frame, text="Location:", font=('Segoe UI', 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=15)
        location_entry = tk.Entry(form_frame, font=('Segoe UI', 10), width=30)
        location_entry.grid(row=1, column=1, pady=15, padx=10)
        
        # Timestamp display
        timestamp_label = tk.Label(
            form_frame,
            text="",
            font=('Segoe UI', 9, 'italic'),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        timestamp_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        def update_timestamp():
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            timestamp_label.config(text=f"Timestamp will be: {current_time}")
        
        update_timestamp()
        
        def submit():
            try:
                student_id = int(id_entry.get().strip())
                location = location_entry.get().strip()
                
                if not location:
                    messagebox.showerror("Error", "Location is required!")
                    return
                
                # Verify student exists
                if not self.students.search_student(student_id):
                    messagebox.showerror("Error", f"Student ID {student_id} not found in system!")
                    return
                
                timestamp = time.time()
                self.logs.enqueue((student_id, location, timestamp))
                
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                messagebox.showinfo(
                    "Success",
                    f"Entry logged successfully!\n\nStudent ID: {student_id}\nLocation: {location}\nTime: {formatted_time}"
                )
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid Student ID! Please enter a valid number.")
        
        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="Log Entry",
            command=submit,
            font=('Segoe UI', 11, 'bold'),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=8
        )
        submit_btn.grid(row=3, column=0, columnspan=2, pady=30)
    
    def _show_entry_logs(self):
        """Display Show Entry Logs screen."""
        window = tk.Toplevel(self.root)
        window.title("Entry Logs")
        window.geometry("800x500")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Entry Logs",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=15
        )
        header.pack()
        
        # Table frame
        table_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for table
        columns = ("Student ID", "Location", "Timestamp")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        tree.heading("Student ID", text="Student ID")
        tree.heading("Location", text="Location")
        tree.heading("Timestamp", text="Timestamp")
        
        tree.column("Student ID", width=150, anchor="center")
        tree.column("Location", width=200, anchor="center")
        tree.column("Timestamp", width=300, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load logs
        logs = self.logs.display_logs()
        
        if not logs:
            # Insert empty message
            tree.insert("", tk.END, values=("No logs", "No entries", "No data"))
        else:
            for sid, location, ts in logs:
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
                tree.insert("", tk.END, values=(sid, location, formatted_time))
        
        # Status label
        status_label = tk.Label(
            window,
            text=f"Total Logs: {len(logs)}",
            font=('Segoe UI', 10),
            bg="#f0f0f0",
            pady=10
        )
        status_label.pack()
    
    def _show_shortest_path(self):
        """Display Shortest Path screen."""
        window = tk.Toplevel(self.root)
        window.title("Shortest Path Between Blocks")
        window.geometry("600x400")
        window.configure(bg="#f0f0f0")
        window.transient(self.root)
        window.grab_set()
        
        # Header
        header = tk.Label(
            window,
            text="Shortest Path Between Blocks",
            font=('Segoe UI', 18, 'bold'),
            bg="#f0f0f0",
            pady=20
        )
        header.pack()
        
        # Input frame
        input_frame = tk.Frame(window, bg="#f0f0f0", padx=40)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="Start Block:", font=('Segoe UI', 11), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=10)
        start_entry = tk.Entry(input_frame, font=('Segoe UI', 10), width=25)
        start_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(input_frame, text="End Block:", font=('Segoe UI', 11), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=10)
        end_entry = tk.Entry(input_frame, font=('Segoe UI', 10), width=25)
        end_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Available blocks info
        available_blocks = list(self.graph.adj.keys())
        blocks_info = tk.Label(
            input_frame,
            text=f"Available blocks: {', '.join(available_blocks)}",
            font=('Segoe UI', 9, 'italic'),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        blocks_info.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result frame
        result_frame = tk.Frame(window, bg="#f0f0f0", padx=40)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        result_text = scrolledtext.ScrolledText(
            result_frame,
            font=('Segoe UI', 11),
            height=10,
            width=50,
            wrap=tk.WORD,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1
        )
        result_text.pack(fill=tk.BOTH, expand=True)
        
        def find_path():
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            
            if not start or not end:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Please enter both start and end blocks.")
                return
            
            dist, path = self.graph.shortest_path(start, end)
            result_text.delete(1.0, tk.END)
            
            if math.isinf(dist):
                result_text.insert(tk.END, f"No path found between '{start}' and '{end}'.\n\n")
                result_text.insert(tk.END, f"Available blocks: {', '.join(available_blocks)}")
            else:
                path_str = " → ".join(path)
                result_text.insert(tk.END, f"Shortest Path Found!\n\n")
                result_text.insert(tk.END, f"Distance: {dist:.1f} units\n\n")
                result_text.insert(tk.END, f"Path:\n{path_str}")
        
        # Find Path button
        find_btn = tk.Button(
            input_frame,
            text="Find Path",
            command=find_path,
            font=('Segoe UI', 11, 'bold'),
            bg="#c0392b",
            fg="white",
            activebackground="#a93226",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=8
        )
        find_btn.grid(row=3, column=0, columnspan=2, pady=20)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = SmartUniversityGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
