import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

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
                                  font=('Helvetica', 10),
                                  width=20)
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Manuális gomb
        self.manual_button = tk.Button(self.file_frame,
                                     text="Manuális...",
                                     font=('Helvetica', 10))
        self.manual_button.pack(side=tk.LEFT, padx=5)
        self.manual_button.config(command=self.manual_mode)

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
            short_name = filename.split('/')[-1]
            if len(short_name) > 20:
                short_name = short_name[:17] + "..."
            self.file_label.config(text=short_name)

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
            # Itt fut majd le az algoritmus
            print("Órarend generálása kezdődik...")
            
            # Algoritmus lefutása után megjelenítjük az eredmény ablakot
            self.show_result_window()

    def show_result_window(self):
        # Új ablak létrehozása
        self.result_window = tk.Toplevel()
        self.result_window.title("Generálás eredménye")
        self.result_window.geometry("800x600")  # Nagyobb ablak a táblázatnak
        
        # Főcím
        title_label = ttk.Label(
            self.result_window,
            text="Generált órarend",
            font=('Helvetica', 16, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(pady=10)

        # Órarend táblázat keret
        table_frame = ttk.Frame(self.result_window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Órarend táblázat
        self.schedule_table = ttk.Treeview(
            table_frame,
            columns=("Idő", "Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"),
            show="headings",
            height=12
        )

        # Oszlopok beállítása
        for col in self.schedule_table["columns"]:
            self.schedule_table.heading(col, text=col)
            self.schedule_table.column(col, width=120, anchor=tk.CENTER)

        # Időpontok hozzáadása (8:00-tól 20:00-ig)
        for hour in range(8, 20):
            self.schedule_table.insert("", tk.END, values=(
                f"{hour:02d}:00",
                "", "", "", "", ""
            ))

        # Scrollbar hozzáadása
        scrollbar = ttk.Scrollbar(
            table_frame, 
            orient=tk.VERTICAL, 
            command=self.schedule_table.yview
        )
        self.schedule_table.configure(yscrollcommand=scrollbar.set)
        
        # Táblázat és scrollbar elhelyezése
        self.schedule_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Exportálási opciók keret
        export_frame = ttk.Frame(self.result_window)
        export_frame.pack(fill=tk.X, padx=20, pady=10)

        # Nézet választó
        view_label = ttk.Label(
            export_frame,
            text="Exportálási nézet:",
            font=('Helvetica', 10)
        )
        view_label.pack(side=tk.LEFT, padx=5)

        self.view_var = tk.StringVar()
        view_options = [
            "Oktató szerint",
            "Szak és évfolyam szerint",
            "Terem szerint"
        ]
        self.view_combo = ttk.Combobox(
            export_frame,
            textvariable=self.view_var,
            values=view_options,
            state="readonly",
            width=20
        )
        self.view_combo.pack(side=tk.LEFT, padx=5)
        self.view_combo.set("Válasszon nézetet")

        # Ha kiválasztunk egy nézetet, frissítjük a második comboboxot
        self.view_combo.bind('<<ComboboxSelected>>', self.update_second_combo)

        # Második választó (dinamikusan töltődik majd)
        self.second_var = tk.StringVar()
        self.second_combo = ttk.Combobox(
            export_frame,
            textvariable=self.second_var,
            state="readonly",
            width=25
        )
        self.second_combo.pack(side=tk.LEFT, padx=5)

        # Exportálás gomb
        export_button = tk.Button(
            export_frame,
            text="Exportálás",
            font=('Helvetica', 9),
            padx=10,
            pady=5,
            command=self.export_schedule
        )
        export_button.pack(side=tk.RIGHT, padx=5)

    def update_second_combo(self, event=None):
        # A második combobox tartalmának frissítése a választott nézet alapján
        selected_view = self.view_var.get()
        
        if selected_view == "Oktató szerint":
            options = ["Dr. Kiss János", "Dr. Nagy Péter", "Dr. Szabó Mária"]  # Példa oktatók
        elif selected_view == "Szak és évfolyam szerint":
            options = ["Programtervező informatikus BSc 1. évf.", 
                      "Mérnökinformatikus BSc 2. évf.",
                      "Gazdaságinformatikus MSc 1. évf."]  # Példa szakok
        elif selected_view == "Terem szerint":
            options = ["IF-001", "IF-002", "IF-103", "IF-204"]  # Példa termek
        else:
            options = []

        self.second_combo['values'] = options
        if options:
            self.second_combo.set("Válasszon...")
        else:
            self.second_combo.set("")

    def export_schedule(self):
        try:
            # Fájl mentési ablak megnyitása
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[
                    ("Excel fájlok", "*.xlsx"),
                    ("CSV fájlok", "*.csv"),
                    ("Minden fájl", "*.*")
                ],
                title="Órarend mentése"
            )
            
            if filename:
                # Itt történik a tényleges exportálás
                # Példa adatok generálása (ezeket a generált órarend adatai helyett kellene használni)
                schedule_data = [
                    {"Idő": "08:00", "Hétfő": "Matematika", "Kedd": "Fizika", "Szerda": "", "Csütörtök": "", "Péntek": ""},
                    {"Idő": "09:00", "Hétfő": "", "Kedd": "", "Szerda": "Programozás", "Csütörtök": "", "Péntek": ""},
                    # További órák...
                ]

                # Exportálás Excel formátumban
                if filename.endswith('.xlsx'):
                    df = pd.DataFrame(schedule_data)
                    df.to_excel(filename, index=False)
                # Exportálás CSV formátumban
                elif filename.endswith('.csv'):
                    df = pd.DataFrame(schedule_data)
                    df.to_csv(filename, index=False)

                messagebox.showinfo("Siker", "Az órarend sikeresen exportálva!")
                
                # Eredmény ablak bezárása
                self.result_window.destroy()
                
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt az exportálás során: {str(e)}")

    def manual_mode(self):
        # Elrejtjük az eredeti ablakot
        self.root.withdraw()
        
        # Új ablak létrehozása
        self.manual_window = tk.Toplevel()
        self.manual_window.title("Manuális órarend készítés")
        self.manual_window.geometry("400x600")  # Nagyobb magasság a több mezőnek
        self.manual_window.resizable(False, False)

        # Címke az ablak tetején
        title_label = ttk.Label(self.manual_window,
                              text="Manuális adatbevitel",
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)

        # Adatbeviteli mezők kerete
        input_frame = ttk.Frame(self.manual_window, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)

        # Teremnév
        ttk.Label(input_frame, text="Teremnév:").pack(anchor=tk.W)
        self.room_name_entry = ttk.Entry(input_frame, width=40)
        self.room_name_entry.pack(fill=tk.X, pady=(0, 10))

        # Terem kapacitása
        ttk.Label(input_frame, text="Terem kapacitása:").pack(anchor=tk.W)
        self.room_capacity_entry = ttk.Entry(input_frame, width=40)
        self.room_capacity_entry.pack(fill=tk.X, pady=(0, 10))

        # Tárgy neve
        ttk.Label(input_frame, text="Tárgy neve:").pack(anchor=tk.W)
        self.subject_entry = ttk.Entry(input_frame, width=40)
        self.subject_entry.pack(fill=tk.X, pady=(0, 10))


        # Tárgy kezdeti időpontja
        ttk.Label(input_frame, text="Tárgy kezdeti időpontja:").pack(anchor=tk.W)
        self.start_time_entry = ttk.Entry(input_frame, width=40)
        self.start_time_entry.pack(fill=tk.X, pady=(0, 10))
        self.start_time_entry.insert(0, "pl.: 8:00")

        # Tárgy befejezési időpontja
        ttk.Label(input_frame, text="Tárgy befejezési időpontja:").pack(anchor=tk.W)
        self.end_time_entry = ttk.Entry(input_frame, width=40)
        self.end_time_entry.pack(fill=tk.X, pady=(0, 20))
        self.end_time_entry.insert(0, "pl.: 9:30")

        # Gombok kerete
        button_frame = ttk.Frame(self.manual_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        # Hozzáadás gomb (középen)
        add_button = tk.Button(button_frame,
                             text="Hozzáadás",
                             font=('Helvetica', 10),
                             command=self.add_manual_data)
        add_button.pack(side=tk.TOP, pady=10)

        # Vissza gomb (bal alsó sarok)
        back_button = tk.Button(self.manual_window,
                              text="Vissza",
                              font=('Helvetica', 10),
                              command=self.close_manual_window)
        back_button.pack(side=tk.BOTTOM, anchor=tk.SW, padx=10, pady=10)

        # Ha bezárják az ablakot X-szel
        self.manual_window.protocol("WM_DELETE_WINDOW", self.close_manual_window)

    def add_manual_data(self):
        # Adatok beolvasása
        room_name = self.room_name_entry.get()
        room_capacity = self.room_capacity_entry.get()
        subject = self.subject_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        
        # Ellenőrzés, hogy minden mező ki van-e töltve
        if not all([room_name, room_capacity, subject, start_time, end_time]):
            messagebox.showwarning("Figyelmeztetés", 
                                 "Kérem töltse ki az összes mezőt!")
            return
            
        # Kapacitás szám ellenőrzése
        try:
            capacity = int(room_capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hiba", 
                               "A terem kapacitásának pozitív számnak kell lennie!")
            return

        # Időformátum ellenőrzése
        def validate_time_format(time_str):
            if len(time_str) != 5:  # óó:pp formátum = 5 karakter
                return False
            if time_str[2] != ':':  # kettőspont a közepén
                return False
            hours, minutes = time_str.split(':')
            try:
                h, m = int(hours), int(minutes)
                return 0 <= h <= 23 and 0 <= m <= 59
            except ValueError:
                return False

        # Időpontok ellenőrzése
        if not validate_time_format(start_time) or not validate_time_format(end_time):
            messagebox.showerror("Hiba", 
                               "Az időpontokat óó:pp formátumban kell megadni! (pl.: 08:30)")
            return

        # Itt lehet majd feldolgozni az adatokat
        print(f"Új adat hozzáadva:\n"
              f"Teremnév: {room_name}\n"
              f"Kapacitás: {room_capacity}\n"
              f"Tárgy: {subject}\n"
              f"Kezdés: {start_time}\n"
              f"Befejezés: {end_time}")
        
        # Mezők törlése
        for entry in [self.room_name_entry, self.room_capacity_entry, 
                     self.subject_entry, self.start_time_entry, 
                     self.end_time_entry]:
            entry.delete(0, tk.END)
            
        # Időpont példák visszaállítása
        self.start_time_entry.insert(0, "pl.: 8:00")
        self.end_time_entry.insert(0, "pl.: 9:30")

    def close_manual_window(self):
        # Bezárjuk a manuális ablakot
        self.manual_window.destroy()
        # Újra megjelenítjük az eredeti ablakot
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
