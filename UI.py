from tkinter import ttk, filedialog, messagebox
import tkinter as tk

class OrarendTervezo:
    def __init__(self, root):
        self.root = root
        self.root.title("Órarend Tervező")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # Fő konténer
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)

        # Főcím kiemelve
        title_label = ttk.Label(self.main_frame, 
                              text="Órarend Tervező", 
                              font=('Helvetica', 24, 'bold'),
                              foreground="#2c3e50")  # sötétkék szín
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
                 text="Optimalizálási algoritmus:", 
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

        # Külön keret a generálás gombnak
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        # Generálás gomb - egyszerű verzió
        self.generate_button = tk.Button(self.main_frame,
                                       text="Órarend generálása",
                                       font=('Helvetica', 10),
                                       padx=10,
                                       pady=5)
        self.generate_button.pack(pady=20)
        self.generate_button.config(command=self.generate_schedule)

        # Tooltipek hozzáadása
        self.create_tooltips()

        # Státusz sáv
        self.status_bar = ttk.Label(self.root, 
                                  text="Kérem válasszon ki egy bemeneti fájlt...", 
                                  style="Status.TLabel")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Frame a futtatás gombnak (jobb alsó sarok)
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Futtatás gomb
        self.run_button = ttk.Button(self.button_frame,
                                   text="Futtatás",
                                   command=self.show_results)
        self.run_button.pack(side=tk.RIGHT)

    def create_tooltips(self):
        CreateToolTip(self.load_button, 
            "CSV vagy Excel fájl kiválasztása a bemeneti adatokkal")

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
            self.status_bar.config(
                text=f"Fájl sikeresen betöltve: {filename.split('/')[-1]}")
        else:
            self.status_bar.config(text="A fájl kiválasztása megszakítva")

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
            self.status_bar.config(text="Órarend generálása folyamatban...")
            # Itt folytatódik majd a generálás

    def show_results(self):
        # Ellenőrzések a futtatás előtt
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

        # Új ablak megnyitása az eredményekhez
        ResultWindow(self.root, self.selected_file, self.algorithm_var.get())

class CreateToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tooltip_window = None

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tooltip_window, 
                         text=self.text, 
                         background="#ffffe0", 
                         relief="solid", 
                         padding=2)
        label.pack()

    def leave(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ResultWindow:
    def __init__(self, parent, file_path, algorithm):
        # Új ablak létrehozása
        self.window = tk.Toplevel(parent)
        self.window.title("Órarend eredmények")
        self.window.geometry("600x400")
        
        # Címke az eredmények felett
        title_label = ttk.Label(self.window,
                              text="Generált órarend",
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Információs panel
        info_frame = ttk.Frame(self.window)
        info_frame.pack(fill=tk.X, padx=20)
        
        ttk.Label(info_frame,
                 text=f"Bemeneti fájl: {file_path.split('/')[-1]}").pack(anchor=tk.W)
        ttk.Label(info_frame,
                 text=f"Használt algoritmus: {algorithm}").pack(anchor=tk.W)
        
        # Itt lesz majd az eredmények megjelenítése
        result_frame = ttk.Frame(self.window)
        result_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Példa szöveg (ezt majd később lecseréljük a valódi eredményekkel)
        ttk.Label(result_frame,
                 text="Az eredmények generálása folyamatban...").pack(expand=True)
        
        # Bezárás gomb
        close_button = ttk.Button(self.window,
                                text="Bezárás",
                                command=self.window.destroy)
        close_button.pack(pady=10)
        
        # Az új ablak modális (nem lehet az eredeti ablakot használni, amíg ez nyitva van)
        self.window.transient(parent)
        self.window.grab_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
