import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class OrarendTervezo:
    def __init__(self, root):
        self.root = root
        self.root.title("Órarend Tervező")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Stílus beállítások
        self.setup_styles()
        
        # Fő konténer
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)

        # Főcím
        title_label = ttk.Label(self.main_frame, 
                              text="Órarend Tervező", 
                              style="Title.TLabel")
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
                                  style="Info.TLabel")
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Algoritmus választó rész
        ttk.Label(self.main_frame, 
                 text="Optimalizálási algoritmus:", 
                 style="Subtitle.TLabel").pack(pady=10)

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

        # Státusz sáv
        self.status_bar = ttk.Label(self.root, 
                                  text="Kérem válasszon ki egy bemeneti fájlt...", 
                                  style="Status.TLabel")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Tooltipek hozzáadása
        self.create_tooltips()

    def setup_styles(self):
        style = ttk.Style()
        # Főcím stílus
        style.configure("Title.TLabel",
                       font=('Helvetica', 24, 'bold'),
                       foreground="#2c3e50")
        # Alcím stílus
        style.configure("Subtitle.TLabel",
                       font=('Helvetica', 12),
                       foreground="#34495e")
        # Információs szöveg stílus
        style.configure("Info.TLabel",
                       font=('Helvetica', 10),
                       foreground="#7f8c8d")
        # Státusz sáv stílus
        style.configure("Status.TLabel",
                       font=('Helvetica', 9),
                       foreground="#666666",
                       background="#f0f0f0",
                       padding=5)

    def create_tooltips(self):
        CreateToolTip(self.load_button, 
            "CSV vagy Excel fájl kiválasztása a bemeneti adatokkal")
        CreateToolTip(self.generate_button, 
            "Az órarend generálásának indítása a kiválasztott beállításokkal")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
