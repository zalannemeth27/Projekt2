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
        self.result_window.geometry("400x250")  # Kicsit nagyobb ablak
        self.result_window.resizable(False, False)
        
        # Középre igazított üzenet
        message_frame = ttk.Frame(self.result_window)
        message_frame.pack(expand=True)
        
        # Sikeres üzenet hangsúlyosan
        success_message = ttk.Label(
            message_frame,
            text="Az algoritmus sikeresen lefutott!",
            font=('Helvetica', 16, 'bold'),
            foreground='#2c3e50'  # Sötétebb szín
        )
        success_message.pack(pady=30)
        
        # Exportálás gomb - kisebb méret és jobb alsó sarok
        export_button = tk.Button(
            self.result_window,  # Changed from message_frame to result_window
            text="Exportálás",
            font=('Helvetica', 9),  # Kisebb betűméret
            padx=10,              # Kisebb padding
            pady=5,
            command=self.export_schedule
        )
        export_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

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
                # Itt történik majd a tényleges exportálás
                print(f"Exportálás ide: {filename}")
                messagebox.showinfo("Siker", 
                                  "Az órarend sikeresen exportálva!")
                
                # Eredmény ablak bezárása
                self.result_window.destroy()
                
        except Exception as e:
            messagebox.showerror("Hiba", 
                               f"Hiba történt az exportálás során: {str(e)}")

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
