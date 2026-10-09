import tkinter as tk
from tkinter import ttk
import numpy as np
import ast

class NightlyMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix App - Nightly Edition")
        self.root.geometry("920x720")
        
        # Nightly Theme Colors
        self.bg_color = "#1E1E1E"          
        self.frame_bg = "#2D2D30"          
        self.text_fg = "#D4D4D4"           
        self.placeholder_fg = "#777777"    # Grayed out color for examples
        self.entry_bg = "#3C3C3C"          
        self.accent_blue = "#0E639C"       
        self.accent_hover = "#1177BB"      
        self.console_bg = "#0C0C0C"        
        self.console_fg = "#4AF626"        

        self.root.configure(bg=self.bg_color)
        
        # Set up custom theme for the Dark Scrollbar
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Nightly.Vertical.TScrollbar",
                             background=self.entry_bg,
                             troughcolor=self.bg_color,
                             bordercolor=self.bg_color,
                             arrowcolor=self.text_fg)
        self.style.map("Nightly.Vertical.TScrollbar",
                       background=[('active', self.frame_bg)])
        
        # Variables
        self.memory_matrix = None          
        self.current_result = None
        
        self.setup_ui()
        self.log("System Initialized. Welcome to Matrix App.")
        self.log("Format Example: [[1,2],[3,4]]\n")

    def create_clearable_entry(self, parent, placeholder_text):
        """Creates a modern input box with placeholder text and an X to clear."""
        wrapper = tk.Frame(parent, bg=self.entry_bg, highlightbackground="#555555", highlightthickness=1)
        
        # The actual entry widget initialized with placeholder settings
        entry = tk.Entry(wrapper, bg=self.entry_bg, fg=self.placeholder_fg, insertbackground=self.text_fg, 
                         font=("Consolas", 11), relief=tk.FLAT, bd=0)
        entry.insert(0, placeholder_text)
        entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=3)
        
        # Attach placeholder metadata to the widget for easy validation
        entry.placeholder = placeholder_text
        
        # Events to handle placeholder appearing/disappearing
        def on_focus_in(event):
            if entry.get() == entry.placeholder and entry.cget('fg') == self.placeholder_fg:
                entry.delete(0, tk.END)
                entry.config(fg=self.text_fg)
                
        def on_focus_out(event=None):
            if not entry.get().strip():
                entry.insert(0, entry.placeholder)
                entry.config(fg=self.placeholder_fg)
                
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        # The 'X' clear button
        clear_btn = tk.Label(wrapper, text="✕", bg=self.entry_bg, fg="#888888", font=("Arial", 10), cursor="hand2")
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Hover events for the 'X'
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(fg="#FF5555")) 
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(fg="#888888"))
        
        # Click event to clear the entry and reset placeholder
        def clear_action(event):
            entry.delete(0, tk.END)
            self.root.focus() # Remove focus to trigger the FocusOut event visually
            on_focus_out()
            
        clear_btn.bind("<Button-1>", clear_action)
        
        return wrapper, entry

    def setup_ui(self):
        # --- Top Input Frame (Grid Layout) ---
        input_frame = tk.Frame(self.root, bg=self.frame_bg, padx=15, pady=15)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, minsize=40) 
        input_frame.grid_columnconfigure(3, weight=1)

        # Inputs using the new clearable entry function with examples
        tk.Label(input_frame, text="Matrix A:", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e", pady=4)
        wrap_a, self.entry_a = self.create_clearable_entry(input_frame, "e.g., [[1, 2], [3, 4]]")
        wrap_a.grid(row=0, column=1, sticky="ew", padx=10, pady=4)
        
        tk.Label(input_frame, text="Matrix B:", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="e", pady=4)
        wrap_b, self.entry_b = self.create_clearable_entry(input_frame, "e.g., [[5, 6], [7, 8]]")
        wrap_b.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        
        tk.Label(input_frame, text="Scalar / Size:", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="e", pady=4)
        wrap_scalar, self.entry_scalar = self.create_clearable_entry(input_frame, "e.g., 3 (for scalar math or 3x3 generation)")
        wrap_scalar.grid(row=2, column=1, sticky="w", padx=10, pady=4)

        # Memory Controls
        mem_frame = tk.Frame(input_frame, bg=self.frame_bg)
        mem_frame.grid(row=0, column=3, rowspan=3, sticky="nsew")
        
        self.lbl_memory = tk.Label(mem_frame, text="[ Memory: Empty ]", bg=self.frame_bg, fg="#FFCC00", font=("Consolas", 10, "bold"))
        self.lbl_memory.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        self.create_btn(mem_frame, "Save Output to Mem", self.save_to_memory).grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)
        self.create_btn(mem_frame, "Mem -> A", lambda: self.load_memory(self.entry_a)).grid(row=2, column=0, sticky="ew", padx=(0, 2), pady=2)
        self.create_btn(mem_frame, "Mem -> B", lambda: self.load_memory(self.entry_b)).grid(row=2, column=1, sticky="ew", padx=(2, 0), pady=2)
        mem_frame.grid_columnconfigure((0,1), weight=1)

        # --- Operations Frame (Compact 2x2 Grid) ---
        op_frame = tk.Frame(self.root, bg=self.bg_color)
        op_frame.pack(fill=tk.X, padx=10, pady=5)
        op_frame.grid_columnconfigure((0, 1), weight=1)

        # 1. Basic Scalar Ops
        f1 = tk.LabelFrame(op_frame, text=" Basic Scalar (A & Scalar) ", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 9))
        f1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.create_btn(f1, "A + Scalar", lambda: self.scalar_op('+')).grid(row=0, column=0, sticky="ew", padx=3, pady=5)
        self.create_btn(f1, "A - Scalar", lambda: self.scalar_op('-')).grid(row=0, column=1, sticky="ew", padx=3, pady=5)
        self.create_btn(f1, "A * Scalar", lambda: self.scalar_op('*')).grid(row=0, column=2, sticky="ew", padx=3, pady=5)
        f1.grid_columnconfigure((0,1,2), weight=1)

        # 2. Basic Matrix Ops
        f2 = tk.LabelFrame(op_frame, text=" Basic Matrix (A & B) ", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 9))
        f2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.create_btn(f2, "A + B", lambda: self.matrix_op('+')).grid(row=0, column=0, sticky="ew", padx=3, pady=5)
        self.create_btn(f2, "A - B", lambda: self.matrix_op('-')).grid(row=0, column=1, sticky="ew", padx=3, pady=5)
        self.create_btn(f2, "A @ B", lambda: self.matrix_op('@')).grid(row=0, column=2, sticky="ew", padx=3, pady=5)
        f2.grid_columnconfigure((0,1,2), weight=1)

        # 3. Advanced Ops
        f3 = tk.LabelFrame(op_frame, text=" Advanced Operations (Matrix A) ", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 9))
        f3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.create_btn(f3, "Det & Singularity", self.do_det_singularity).grid(row=0, column=0, sticky="ew", padx=3, pady=3)
        self.create_btn(f3, "Rank", self.do_rank).grid(row=0, column=1, sticky="ew", padx=3, pady=3)
        self.create_btn(f3, "Transpose", self.do_transpose).grid(row=1, column=0, sticky="ew", padx=3, pady=3)
        self.create_btn(f3, "Inverse", self.do_inverse).grid(row=1, column=1, sticky="ew", padx=3, pady=3)
        self.create_btn(f3, "Adjoint & Cofactor", self.do_adj_cofactor).grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        f3.grid_columnconfigure((0,1), weight=1)

        # 4. Symmetry Ops 
        f4 = tk.LabelFrame(op_frame, text=" Symmetry Operations ", bg=self.frame_bg, fg=self.text_fg, font=("Segoe UI", 9))
        f4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.create_btn(f4, "Check / Make Symmetric (A)", self.do_symmetry).grid(row=0, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        tk.Label(f4, text="Requires 'Scalar' for Matrix Size (e.g. 3 = 3x3)", bg=self.frame_bg, fg="#999999", font=("Segoe UI", 8, "italic")).grid(row=1, column=0, columnspan=2, pady=(5,0))
        self.create_btn(f4, "Gen Symmetric", self.do_gen_sym).grid(row=2, column=0, sticky="ew", padx=3, pady=3)
        self.create_btn(f4, "Gen Skew-Sym", self.do_gen_skew).grid(row=2, column=1, sticky="ew", padx=3, pady=3)
        f4.grid_columnconfigure((0,1), weight=1)

        # --- Console Output ---
        console_container = tk.Frame(self.root, bg=self.bg_color)
        console_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        top_console = tk.Frame(console_container, bg=self.bg_color)
        top_console.pack(fill=tk.X)
        tk.Label(top_console, text="Output Console:", bg=self.bg_color, fg=self.text_fg, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        
        # New Transparent X for Clearing the Console
        clear_console_btn = tk.Label(top_console, text="✕", bg=self.bg_color, fg="#888888", font=("Arial", 12, "bold"), cursor="hand2")
        clear_console_btn.pack(side=tk.RIGHT, padx=5)
        clear_console_btn.bind("<Enter>", lambda e: clear_console_btn.config(fg="#FF5555")) 
        clear_console_btn.bind("<Leave>", lambda e: clear_console_btn.config(fg="#888888"))
        clear_console_btn.bind("<Button-1>", lambda e: self.clear_console())

        self.console = tk.Text(console_container, bg=self.console_bg, fg=self.console_fg, font=("Consolas", 11), 
                               state="disabled", relief=tk.FLAT, padx=10, pady=10, highlightthickness=1, highlightbackground=self.frame_bg)
        
        scrollbar = ttk.Scrollbar(console_container, orient="vertical", command=self.console.yview, style="Nightly.Vertical.TScrollbar")
        self.console.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_btn(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg=self.accent_blue, fg="white", 
                         activebackground=self.accent_hover, activeforeground="white", 
                         relief=tk.FLAT, bd=0, font=("Segoe UI", 9, "bold"), pady=4)

    # --- Helpers & IO ---
    def log(self, msg):
        self.console.config(state="normal")
        self.console.insert(tk.END, f"{msg}\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def clear_console(self):
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")
        
    def get_matrix(self, entry_widget):
        inp = entry_widget.get().strip()
        # Ensure we don't try to parse the placeholder text
        if not inp or inp == getattr(entry_widget, 'placeholder', ''): 
            return None
        try:
            arr = ast.literal_eval(inp)
            return np.array(arr)
        except:
            self.log("ERROR: Invalid Matrix Format. Use [[1,2],[3,4]]")
            return None

    def get_scalar(self):
        inp = self.entry_scalar.get().strip()
        if not inp or inp == getattr(self.entry_scalar, 'placeholder', ''): 
            return None
        try:
            return float(inp)
        except:
            self.log("ERROR: Invalid Scalar/Size Format.")
            return None

    # --- Memory Features ---
    def save_to_memory(self):
        if self.current_result is not None:
            self.memory_matrix = self.current_result
            shape = self.memory_matrix.shape
            self.lbl_memory.config(text=f"[ Mem: {shape} Matrix ]", fg="#4AF626")
            self.log(f"--- Saved {shape} Matrix to Memory ---")
        else:
            self.log("ERROR: No valid result to save.")

    def load_memory(self, entry_widget):
        if self.memory_matrix is not None:
            entry_widget.delete(0, tk.END)
            entry_widget.config(fg=self.text_fg) # Turn text color back to normal
            entry_widget.insert(0, str(self.memory_matrix.tolist()))
            self.log("Memory loaded into input field.")
        else:
            self.log("ERROR: Memory is empty.")

    def print_extras(self, matrix):
        self.log("\nExtras:")
        try:
            if matrix.shape[0] == matrix.shape[1]:
                if np.linalg.det(matrix) == 0:
                    self.log("> Matrix is Singular")
                else:
                    self.log("> Matrix is not Singular")
        except: pass
        
        if np.array_equal(matrix, matrix.T):
            self.log("> Matrix is Symmetric")
        elif np.array_equal(matrix, -matrix.T):
            self.log("> Matrix is Skew-Symmetric")
        else:
            self.log("> Matrix is not Symmetric")

    # --- Operations Logic ---
    def scalar_op(self, op):
        A = self.get_matrix(self.entry_a)
        S = self.get_scalar()
        if A is None or S is None: return
        self.log(f"--- Scalar {op} ---")
        identity = np.eye(len(A))
        if op == '+': self.current_result = A + (S * identity)
        elif op == '-': self.current_result = A - (abs(S) * identity)
        elif op == '*': self.current_result = A * S
        self.log(f"Result:\n{self.current_result}\n" + "-" * 45)

    def matrix_op(self, op):
        A = self.get_matrix(self.entry_a)
        B = self.get_matrix(self.entry_b)
        if A is None or B is None: return
        self.log(f"--- Matrix {op} ---")
        try:
            if op == '+':
                if A.shape == B.shape: self.current_result = A + B
                else: raise ValueError("Shapes do not match.")
            elif op == '-':
                if A.shape == B.shape: self.current_result = A - B
                else: raise ValueError("Shapes do not match.")
            elif op == '@':
                if A.shape[1] == B.shape[0]: self.current_result = A @ B
                else: raise ValueError("Invalid shapes for multiplication.")
            self.log(f"Result:\n{self.current_result}")
        except Exception as e:
            self.log(f"ERROR: {e}")
        self.log("-" * 45)

    def do_det_singularity(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Determinant & Singularity ---")
        try:
            det = np.linalg.det(A)
            self.log(f"Determinant: {round(det, 4)}")
            self.log("Matrix is Singular" if det == 0 else "Matrix is not Singular")
        except:
            self.log("Must be a square matrix.")
        self.log("-" * 45)

    def do_transpose(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Transpose ---")
        self.current_result = A.T
        self.log(f"Result:\n{self.current_result}")
        self.print_extras(self.current_result)
        self.log("-" * 45)

    def do_inverse(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Inverse ---")
        try:
            if np.linalg.det(A) != 0:
                self.current_result = np.linalg.inv(A)
                self.log(f"Result:\n{self.current_result}")
                self.print_extras(self.current_result)
            else:
                self.log("Matrix is singular, not invertible.")
        except:
            self.log("Must be a square matrix.")
        self.log("-" * 45)

    def do_adj_cofactor(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Adjoint & Cofactor ---")
        try:
            inv = np.linalg.inv(A)
            det = np.linalg.det(A)
            adjoint = det * inv
            cofactor = np.transpose(inv) * det
            self.log(f"Adjoint:\n{adjoint}\n")
            self.log(f"Cofactor:\n{cofactor}")
            self.current_result = adjoint
        except:
            self.log("Matrix is singular or not square.")
        self.log("-" * 45)

    def do_rank(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Rank ---")
        self.log(f"Rank of the Matrix is: {np.linalg.matrix_rank(A)}")
        self.log("-" * 45)

    def do_symmetry(self):
        A = self.get_matrix(self.entry_a)
        if A is None: return
        self.log("--- Check/Make Symmetric ---")
        if np.array_equal(A, A.T):
            self.log("Matrix is already Symmetric.")
            self.current_result = A
        else:
            self.log("Matrix was not symmetric. Converting (A * A.T)...")
            self.current_result = A @ A.T
            self.log(f"Result:\n{self.current_result}")
        self.print_extras(self.current_result)
        self.log("-" * 45)

    def do_gen_sym(self):
        s = self.get_scalar()
        if s is None: return
        size = int(abs(s))
        matrix = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(i, size):
                val = np.random.randint(1, 100)
                matrix[i, j] = val
                matrix[j, i] = val
        self.log("--- Generated Symmetric Matrix ---")
        self.current_result = matrix
        self.log(f"{self.current_result}\n" + "-" * 45)

    def do_gen_skew(self):
        s = self.get_scalar()
        if s is None: return
        size = int(abs(s))
        matrix = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(i+1, size):
                val = np.random.randint(1, 100)
                matrix[i, j] = val
                matrix[j, i] = -val
        self.log("--- Generated Skew-Symmetric Matrix ---")
        self.current_result = matrix
        self.log(f"{self.current_result}\n" + "-" * 45)

if __name__ == "__main__":
    root = tk.Tk()
    app = NightlyMatrixApp(root)
    root.mainloop()