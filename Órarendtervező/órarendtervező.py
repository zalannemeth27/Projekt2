
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import pandas as pd
from Genetic import GeneticAlgorithm
from BacterialEvolution import BacterialEvolutionAlgorithm
from AntColony import AntColonyAlgorithm
from LocalSearch import LocalSearchAlgorithm
import sqlite3


class OrarendTervezo:
    def __init__(self, root):
        self.best_schedule = None
        self.schedule_dict = None
        self.oktato_nevek = None
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

    def generate_schedule(self):
        if not self.algorithm_var.get() or self.algorithm_var.get() == "Válasszon algoritmust":
            messagebox.showwarning(
                "Figyelmeztetés",
                "Kérem válasszon algoritmust!"
            )
            return

        if messagebox.askyesno(
            "Megerősítés",
            f"Szeretnéd elíndtani az órarend generálását?\n\n"
            f"Választott algoritmus: {self.algorithm_var.get()}"
        ):
            # Itt fut majd le az algoritmus
            print("Órarend generálása kezdődik...")

            # Algoritmus lefutása után megjelenítjük az eredmény ablakot
            self.show_result_window()
            self.run_algorithm()

    def run_algorithm(self):
        # Algoritmusok implementálása
        algorithm = self.algorithm_var.get()
        if algorithm == "Genetikus algoritmus":
            self.genetic_algorithm()
        elif algorithm == "Bakteriális Evolúciós Algoritmus":
            self.bacterial_evolution_algorithm()
        elif algorithm == "Hangyakolónia algoritmus":
            self.ant_colony_algorithm()
        elif algorithm == "Lokális keresési módzser":
            self.local_search_algorithm()

    def genetic_algorithm(self):
        print("Genetikus algoritmus futtatása...")

        n_classes = 20  # pl 10 tantárgy
        n_days = 5      # 5 nap
        n_slots = 6     # 6 időpont

        ga = GeneticAlgorithm(
            population_size=50,
            generations=100,
            mutation_rate=0.1,
            crossover_rate=0.7,
            n_classes=n_classes,
            n_days=n_days,
            n_slots=n_slots
        )

        best_schedule = ga.evolve()
        self.update_result_text(best_schedule)

    def bacterial_evolution_algorithm(self):
        print("Bakteriális Evolúciós algoritmus futtatása...")

        n_classes = 20  # pl 10 tantárgy
        n_days = 5      # 5 nap
        n_slots = 6     # 6 időpont

        # Bakteriális evolúciós algoritmus futtatása
        bea = BacterialEvolutionAlgorithm(
            population_size=50,
            generations=100,
            mutation_rate=0.1,
            n_classes=n_classes,
            n_days=n_days,
            n_slots=n_slots
        )

        best_schedule = bea.evolve()
        self.update_result_text(best_schedule)

    def ant_colony_algorithm(self):
        print("Hangyakolónia algoritums futtatása...")

        n_classes = 20  # pl 10 tantárgy
        n_days = 5      # 5 nap
        n_slots = 6     # 6 időpont

        # Hangyakolónia algoritums futtatása
        aco = AntColonyAlgorithm(
            population_size=50,
            generations=100,
            pheromone_decay=0.1,
            pheromone_instensity=1.0,
            n_classes=n_classes,
            n_days=n_days,
            n_slots=n_slots
        )

        best_schedule = aco.evolve()
        self.update_result_text(best_schedule)

    def local_search_algorithm(self):
        print("Lokális keresési algoritmus futtatása...")

        n_classes = 20  # pl 10 tantárgy
        n_days = 5      # 5 nap
        n_slots = 6     # 6 időpont

        # Lokális keresési algoritmus futtatása
        lsa = LocalSearchAlgorithm(
            n_classes=n_classes, n_days=n_days, n_slots=n_slots)

        best_schedule = lsa.search()
        self.update_result_text(best_schedule)

    def populate_schedule(self, schedule_data, schedule_dict):
        # Inicializálja az ütemezési táblázatot üres értékekkel
        for hour in range(8, 16):
            self.schedule_table.insert("", tk.END, values=(
                f"{hour:02d}:00",
                "", "", "", "", ""
            ))

        # Feltölti az ütemezési táblázatot a megadott adatokkal
        for class_id, (day, hour_slot) in schedule_data.items():
            if self.algorithm_var.get() == "Bakteriális Evolúciós Algoritmus":
                day -= 1
                hour_slot -= 1
                class_id -= 1
            # Kiszámitja a sorindexet az órasáv alapján
            row_index = hour_slot + 8 
            # Aktualis ertekek a sorban
            current_values = self.schedule_table.item(
                self.schedule_table.get_children()[row_index - 8])['values']
            # Frissíti az értékeket az osztályazonosítóval a megfelelő nap oszlopban
            updated_values = list(current_values)
            # day + 1 mert az elso oszlop az ora
            updated_values[day +
                           1] = f"{schedule_dict[class_id + 1][1]} - {schedule_dict[class_id + 1][0]}"
            # Frissiti a sort az utemezesei tablazatban
            self.schedule_table.item(self.schedule_table.get_children()[
                                     row_index - 8], values=tuple(updated_values))

    def update_result_text(self, best_schedule):
        # Text widget frissítítése
        if self.result_text and self.result_text.winfo_exists():
            self.result_text.delete(1.0, tk.END)  # Előző eredmény törlése
            self.result_text.insert(tk.END, "Legjobb órarend:\n")

            conn = sqlite3.connect('schedule.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT Kurzusok.KurzusID, Targyak.Nev, Kurzusok.Tipus, Oktatok.Nev FROM Kurzusok JOIN Targyak ON Kurzusok.TargyID = Targyak.TargyID JOIN Oktatok ON Kurzusok.OktatoID = Oktatok.OktatoID")
            schedule_db_data = cursor.fetchall()
            schedule_dict = {item[0]: item[1:] for item in schedule_db_data}

            cursor.close()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT OktatoID, Nev FROM Oktatok")
            oktato_nevek = cursor.fetchall()
            self.oktato_nevek = {item[0]: item[1] for item in oktato_nevek}

            self.schedule_dict = schedule_dict
            self.best_schedule = best_schedule

            self.populate_schedule(best_schedule, schedule_dict)

            days = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]
            time_slot = ["08:00", "09:00", "10:00",
                         "11:00", "12:00", "13:00", "14:00", "15:00"]

            for class_id, (day, slot) in best_schedule.items():
                if self.algorithm_var.get() == "Bakteriális Evolúciós Algoritmus":
                    day -= 1
                    slot -= 1
                    class_id -= 1
                self.result_text.insert(
                    tk.END, f"Tantárgy {schedule_dict[class_id + 1][1]} - {schedule_dict[class_id + 1][0]} - Nap: {days[day]}, Időpont: {time_slot[slot]}\n")

        else:
            print("A Text widget nem található vagy bezárták.")

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

        # Eredmények szöveges megjelenítése egy Text widget létrehozása
        result_frame = ttk.Frame(self.result_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Az eredmények számára Text widget
        self.result_text = tk.Text(result_frame, height=10, width=80)
        self.result_text.pack()

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
            options = list(self.oktato_nevek.values())
        elif selected_view == "Szak és Évfolyam szerint":
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

    def populate_schedule_export(self, schedule_data, schedule_dict, selected_name, view_var):
        if view_var == "Oktató szerint":
            # Inicializálja a kiválasztott oktato ütemezési modelljét
            selected_schedule = [{"Idő": f"{hour:02d}:00", "Hétfő": "", "Kedd": "",
                                  "Szerda": "", "Csütörtök": "", "Péntek": ""} for hour in range(8, 16)]

            # Feltolti az ütemezési modellt a megadott adatokkal
            for class_id, (day, hour_slot) in schedule_data.items():
                if self.algorithm_var.get() == "Bakteriális Evolúciós Algoritmus":
                    day -= 1
                    hour_slot -= 1
                    class_id -= 1
                # Kiszamítja a sorindexet az órasáv alapján
                row_index = hour_slot
                # Frissíti az értékeket az osztályazonosítóval a megfelelő nap oszlopban
                day_names = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]
                # Feltételezi hogy az oktato név a harmadik elem a sorban
                oktato = schedule_dict[class_id + 1][2]
                if oktato == selected_name:
                    selected_schedule[row_index][day_names[day]
                                                 ] = f"{schedule_dict[class_id + 1][1]} - {schedule_dict[class_id + 1][0]}"

            return selected_schedule
        else:
            # Inicializálja az ütemezési adatmodellt üres értékekkel
            schedule_model = [{"Idő": f"{hour:02d}:00", "Hétfő": "", "Kedd": "",
                               "Szerda": "", "Csütörtök": "", "Péntek": ""} for hour in range(8, 16)]

            # Feltölti az ütemezési modellt a megadott adatokkal
            for class_id, (day, hour_slot) in schedule_data.items():
                if self.algorithm_var.get() == "Bakteriális Evolúciós Algoritmus":
                    day -= 1
                    hour_slot -= 1
                    class_id -= 1
                # Kiszámítja a sorindexet az órasáv alapján
                row_index = hour_slot
                # Frissíti az értékeket az osztályazonosítóval a megfelelő nap oszlopban
                day_names = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]
                schedule_model[row_index][day_names[day]
                                          ] = f"{schedule_dict[class_id + 1][1]} - {schedule_dict[class_id + 1][0]}"

            return schedule_model

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

                schedule_data = self.populate_schedule_export(
                    self.best_schedule, self.schedule_dict, self.second_combo.get(), self.view_var.get())

                if filename.endswith('.xlsx'):
                    df = pd.DataFrame(schedule_data)
                    df.to_excel(filename, index=False)
                elif filename.endswith('.csv'):
                    df = pd.DataFrame(schedule_data)
                    df.to_csv(filename, index=False)

                messagebox.showinfo(
                    "Siker", "Az Órarend sikeresen exportálva!")
                self.result_window.destroy()

        except Exception as e:
            messagebox.showerror(
                "Hiba", f"Hiba történt az exportálás során: {str(e)}")

    def export_to_excel(self, filename):
        # Táblázat exportálása Excel fájlba
        data = []
        for row in self.schedule_table.get_children():
            row_data = self.schedule_table.item(row)["values"]
            data.append(row_data)

        df = pd.DataFrame(
            data, columns=["Idő", "Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"])
        df.to_excel(filename, index=False)
        messagebox.showinfo(
            "Siker", "Órarend sikeresen exportálva Excel formátumban!")

    def export_to_csv(self, filename):
        # Táblázat exportálása CSV fájlba
        data = []
        for row in self.schedule_table.get_children():
            row_data = self.schedule_table.item(row)["values"]
            data.append(row_data)

        df = pd.DataFrame(
            data, columns=["Idő", "Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"])
        df.to_csv(filename, index=False)
        messagebox.showinfo(
            "Siker", "Órarend sikeresen exportálva CSV formátumban!")


if __name__ == "__main__":
    root = tk.Tk()
    app = OrarendTervezo(root)
    root.mainloop()
