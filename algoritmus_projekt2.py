import adatbazis
import random
import json
import pandas as pd
import csv

# Csatlakozás az adatbázishoz

# Adatok betöltése az adatbázisból

    # Hallgatók betöltése

    # Kurzusok betöltése

    # Oktatók betöltése

    # Szakok betöltése

    # Tárgyak betöltése

    # Órarend betöltése

#Fitness függvény
def fitness(orarend):
    score = 0
    conflicts = 0

    # Ütközések ellenörzése
    schedule_map = {}
    for hour in orarend:
        key = (hour['idopont'], hour['terem_id'])
        if key in schedule_map:
            conflicts += 1
        else:
            schedule_map[key] = hour

    # Büntetõ pontok
    score -= conflicts * 10

    # További korlátozások ide (pl tanár elérhetõség stb)

    return score

# Kezdeti populáció generálása
def initial_population(size, kurzusok):
    population = []
    for _ in range(size):
        orarend = []
        for kurzus in kurzusok:
            orarend.append({
                'kurzusok_id': kurzus[0],
                'targy_id': kurzus[1],
                'oktato_id': kurzus[2],
                'terem_id': kurzus[3],
                'idopont': random.choice(['Hétfõ','Kedd','Szerda','Csütörtök','Péntek']),
                'csoport': kurzus[5]
            })
        population.append(orarend)
    return population

# Kiválasztás (random)
def select(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitnesses)
    current = 0
    for i, fitness_val in enumerate(fitnesses):
        current += fitness_val
        if current > pick:
            return population[i]

# Keresztezés
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

# Mutáció
def mutate(orarend, mutation_rate=0.1):
    if random.random() < mutation_rate:
        index = random.randint(0, len(orarend) - 1)
        orarend[index]['idopont'] = random.choice(['Hétfõ','Kedd','Szerda','Csütörtök','Péntek'])
    return orarend

# Genetikus algoritmus futtatása
def genetic_algorithm(conn, generations=100, population=50, mutation_rate=0.1):
    # Adatok betöltése
    hallgatok, kurzusok, oktatok, szakok, targyak, orarend = load_date(conn)

    # Kezdeti populáció
    population = initial_population(population_size, kurzusok)

    for generation in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        new_population = []

        elite_count = population_size // 10
        new_population.extend(sorted(population, key=fitness, reverse=True)[:elite_count])

        # Új egyedek létrehozása
        while len(new_population) < population_size:
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        best_fitness = max(fitnesses)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

    # Legjobb megoldás
    best_schedule = max(population, key=fitness)
    return best_schedule

# Fõ program
if __name__ == "__main__":
    # Adatbázis elérése

    best_schedule=genetic_algorithm(conn, generation=100, population_size=50, mutation_rate=0.1)
    

# Exportálás JSON fájlba
def export_to_json(schedule, filename="orarend.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(schedule, file, indent=4, ensure_ascii=False)
    print(f"Órarend exportálva a következõ fájlba: {filename}")

# Exportálás Excel fájlba
def export_to_excel(schedule, filename="orarend.xlsx"):
    data = []
    for entry in schedule:
        data.append({
            "Kurzus ID": entry['kurzus_id'],
            "Tárgy ID": entry['targy_id'],
            "Oktató ID": entry['oktato_id'],
            "Terem ID": entry['terem_id'],
            "Idõpont": entry['idopont'],
            "Csoport": entry['csoport']
        })

    df = pd.DataFram(data)
    df.to_excel(filename, index=False)
    print(f"Órarend exportálva a következõ fájlba: {filename}")

# Exportálás CSV fájlba
def export_to_csv(schedule, filename="orarend.csv"):
    headers = ["Kurzus ID","Tárgy ID","Oktató ID","Terem ID","Idõpont","Csoport"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for entry in schedule:
            writer.writerow([
                entry['kurzus_id'],
                entry['targy_id'],
                entry['oktato_id'],
                entry['terem_id'],
                entry['idopont'],
                entry['csoport']
            ])
    print(f"Órarend exportálva a következõ fájlba: {filename}")

export_to_csv(best_schedule)
export_to_excel(best_schedule)
export_to_json(best_schedule)