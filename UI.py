import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class OrarendTervezo:
    def __init__(self, root):
        self.root = root
        self.root.title("Órarend Tervező")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # Fő konténer
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)

        # Főcím
        title_label = ttk.Label(self.main_frame, 
                              text="Órarend Tervező", 
                              font=('Helvetica', 24, 'bold'),
                              foreground="#2c3e50")
        title_label.pack(pady=30)

        # Fájl kiválasztó rész
        self.file_frame = ttk.Frame(self.main_frame)
        self.file_frame.pack(pady=20)
        
        self.load_button = ttk.Button(self.file_frame, 
                                    text="Fájl megnyitása", 
                                    command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.file_label = ttk.Label(self.file_frame, 
                                  text="Nincs fájl kiválasztva", 
                                  font=('Helvetica', 10))
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Algoritmus választó rész
        ttk.Label(self.main_frame, 
                 text="Optimalizálási algoritmus", 
                 font=('Helvetica', 12)).pack(pady=10)

        self.algorithm_var = tk.StringVar()
        algorithms = [
            "Genetikus algoritmus",
            "Bakteriális Evolúciós Algoritmus",
            "Hangyakolónia Algoritmus",
            "Lokális keresési módszer"
        ]
        self.algorithm_combo = ttk.Combobox(self.main_frame, 
                                          textvariable=self.algorithm_var,
                                          values=algorithms,
                                          width=30,
                                          state="readonly")
        self.algorithm_combo.pack(pady=10)
        self.algorithm_combo.set("Válasszon algoritmust")

        # Generálás gomb
        self.generate_button = tk.Button(self.main_frame,
                                       text="Órarend generálása",
                                       font=('Helvetica', 10),
                                       padx=10,
                                       pady=5)
        self.generate_button.pack(pady=20)
        self.generate_button.config(command=self.generate_schedule)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Válassza ki az adatfájlt",
            filetypes=[
                ("Támogatott fájlok", "*.csv *.xlsx *.xls"),
                ("CSV fájlok", "*.csv"),
                ("Excel fájlok", "*.xlsx *.xls")
            ]
        )
        if filename:
            file_extension = filename.lower().split('.')[-1]
            if file_extension not in ['csv', 'xlsx', 'xls']:
                messagebox.showerror(
                    "Hiba", 
                    "Csak CSV vagy Excel fájlokat lehet betölteni!"
                )
                return
            self.selected_file = filename
            self.file_label.config(text=filename.split('/')[-1])

    def generate_schedule(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showwarning(
                "Figyelmeztetés",
                "Kérem először válasszon ki egy bemeneti fájlt!"
            )
            return
            
        if not self.algorithm_var.get() or self.algorithm_var.get() == "Válasszon algoritmust":
            messagebox.showwarning(
                "Figyelmeztetés", 
                "Kérem válasszon algoritmust!"
            )
            return
            
        if messagebox.askyesno(
            "Megerősítés",
            f"Szeretné elindítani az órarend generálását?\n\n"
            f"Választott fájl: {self.selected_file.split('/')[-1]}\n"
            f"Választott algoritmus: {self.algorithm_var.get()}"
        ):
            print("Órarend generálása kezdődik...")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
