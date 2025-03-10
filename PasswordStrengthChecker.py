import tkinter as tk
from tkinter import ttk, messagebox

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("600x450")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        
        # Progress bar styles
        self.style.configure("Red.Horizontal.TProgressbar", troughcolor='#f0f0f0', background='#e74c3c')
        self.style.configure("Yellow.Horizontal.TProgressbar", troughcolor='#f0f0f0', background='#f1c40f')
        self.style.configure("Green.Horizontal.TProgressbar", troughcolor='#f0f0f0', background='#2ecc71')
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Password Entry Row
        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        
        ttk.Label(entry_frame, text="Enter Password:").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(entry_frame, width=25, show="•")
        self.password_entry.pack(side=tk.LEFT, expand=True)
        self.password_entry.bind("<KeyRelease>", self.realtime_update)
        
        # Show Password Checkbutton
        self.show_password = tk.BooleanVar()
        show_pass_check = ttk.Checkbutton(
            entry_frame,
            text="Show",
            variable=self.show_password,
            command=self.toggle_password_visibility
        )
        show_pass_check.pack(side=tk.LEFT, padx=(10, 0))
        
        # Strength Meter
        analysis_frame = ttk.LabelFrame(main_frame, text="Password Analysis", padding=10)
        analysis_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        strength_frame = ttk.Frame(analysis_frame)
        strength_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        
        self.strength_label = ttk.Label(strength_frame, text="Strength: N/A")
        self.strength_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(
            strength_frame,
            orient='horizontal',
            length=200,
            mode='determinate',
            style="Red.Horizontal.TProgressbar"
        )
        self.progress.pack(side=tk.RIGHT, padx=10)
        self.progress["maximum"] = 7  # Max possible score
        
        # Criteria labels
        self.length_label = ttk.Label(analysis_frame, text="Length (≥12): ❌")
        self.length_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.upper_label = ttk.Label(analysis_frame, text="Uppercase: ❌")
        self.upper_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.lower_label = ttk.Label(analysis_frame, text="Lowercase: ❌")
        self.lower_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.digit_label = ttk.Label(analysis_frame, text="Digits: ❌")
        self.digit_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.special_label = ttk.Label(analysis_frame, text="Special Chars: ❌")
        self.special_label.grid(row=5, column=0, sticky=tk.W, pady=2)
        
        # Crack time
        self.crack_time_label = ttk.Label(analysis_frame, text="Estimated Crack Time: N/A")
        self.crack_time_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Analyze Button
        ttk.Button(main_frame, text="Analyze Password", command=self.analyze_password).grid(row=2, column=0, columnspan=2, pady=10)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='•')

    def update_criteria_label(self, label, condition):
        label.config(
            text=label.cget("text").split(":")[0] + f": {'✅' if condition else '❌'}",
            foreground="#2ECC71" if condition else "#E74C3C"
        )
        
    def realtime_update(self, event=None):
        self.analyze_password(update_only=True)
        
    def analyze_password(self, update_only=False):
        password = self.password_entry.get()
        
        if not password:
            if not update_only:
                messagebox.showwarning("Input Error", "Please enter a password!")
            return
            
        # Calculate criteria
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+" for c in password)
        
        # Update criteria labels
        self.update_criteria_label(self.length_label, length >= 12)
        self.update_criteria_label(self.upper_label, has_upper)
        self.update_criteria_label(self.lower_label, has_lower)
        self.update_criteria_label(self.digit_label, has_digit)
        self.update_criteria_label(self.special_label, has_special)
        
        # Calculate strength score
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        score = 0
        
        if length >= 12:
            score += 3
        elif length >= 8:
            score += 2
        else:
            score += 1
            
        score += char_types
        
        # Update progress bar
        self.progress["value"] = score
        if score >= 5:
            strength = "Strong"
            style = "Green.Horizontal.TProgressbar"
            color = "#2ECC71"
        elif score >= 3:
            strength = "Moderate"
            style = "Yellow.Horizontal.TProgressbar"
            color = "#F1C40F"
        else:
            strength = "Weak"
            style = "Red.Horizontal.TProgressbar"
            color = "#E74C3C"
            
        self.progress.configure(style=style)
        self.strength_label.config(
            text=f"Strength: {strength}",
            foreground=color
        )
        
        # Calculate crack time
        combinations = 94 ** length
        guesses_per_second = 1e9
        seconds = combinations / guesses_per_second
        
        time_str = (
            "Instantly" if seconds < 1 else
            f"{int(seconds)} seconds" if seconds < 60 else
            f"{int(seconds/60)} minutes" if seconds < 3600 else
            f"{int(seconds/3600)} hours" if seconds < 86400 else
            f"{int(seconds/86400)} days"
        )
        
        self.crack_time_label.config(text=f"Estimated Crack Time: {time_str}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()