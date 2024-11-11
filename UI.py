import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class OrarendTervezo:
    def __init__(self, root):
        self.root = root
        self.root.title("Órarend Tervező")
        
        # Fix ablakméret beállítása
        self.root.geometry("400x350")
        # Letiltjuk az átméretezést és a teljes képernyős módot
        self.root.resizable(False, False)

        # Fő konténer
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)  # pack használata a középre igazításhoz

        # Főcím
        title_label = ttk.Label(self.main_frame, 
                              text="Órarend Tervező", 
                              font=('Helvetica', 24, 'bold'))
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

        # Algoritmus választó címke
        ttk.Label(self.main_frame, 
                 text="Optimalizálási algoritmus:", 
                 font=('Helvetica', 12)).pack(pady=10)

        # Algoritmus választó legördülő lista
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
        self.generate_button = ttk.Button(self.main_frame, 
                                        text="Órarend generálása", 
                                        command=self.generate_schedule)
        self.generate_button.pack(pady=30)

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
                tk.messagebox.showerror(
                    "Hiba", 
                    "Csak CSV vagy Excel fájlokat lehet betölteni!"
                )
                return
            # Fájlnév megjelenítése (csak a fájl neve, nem a teljes útvonal)
            self.file_label.config(text=filename.split('/')[-1])
            print(f"Fájl betöltve: {filename}")

    def generate_schedule(self):
        if not self.algorithm_var.get() or self.algorithm_var.get() == "Válasszon algoritmust":
            tk.messagebox.showwarning("Figyelmeztetés", "Kérem válasszon algoritmust!")
            return
        print("Órarend generálás kezdődik...")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
