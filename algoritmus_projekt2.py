import adatbazis
import random
import json
import pandas as pd
import csv

# Csatlakoz�s az adatb�zishoz

# Adatok bet�lt�se az adatb�zisb�l

    # Hallgat�k bet�lt�se

    # Kurzusok bet�lt�se

    # Oktat�k bet�lt�se

    # Szakok bet�lt�se

    # T�rgyak bet�lt�se

    # �rarend bet�lt�se

#Fitness f�ggv�ny
def fitness(orarend):
    score = 0
    conflicts = 0

    # �tk�z�sek ellen�rz�se
    schedule_map = {}
    for hour in orarend:
        key = (hour['idopont'], hour['terem_id'])
        if key in schedule_map:
            conflicts += 1
        else:
            schedule_map[key] = hour

    # B�ntet� pontok
    score -= conflicts * 10

    # Tov�bbi korl�toz�sok ide (pl tan�r el�rhet�s�g stb)

    return score

# Kezdeti popul�ci� gener�l�sa
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
                'idopont': random.choice(['H�tf�','Kedd','Szerda','Cs�t�rt�k','P�ntek']),
                'csoport': kurzus[5]
            })
        population.append(orarend)
    return population

# Kiv�laszt�s (random)
def select(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitnesses)
    current = 0
    for i, fitness_val in enumerate(fitnesses):
        current += fitness_val
        if current > pick:
            return population[i]

# Keresztez�s
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

# Mut�ci�
def mutate(orarend, mutation_rate=0.1):
    if random.random() < mutation_rate:
        index = random.randint(0, len(orarend) - 1)
        orarend[index]['idopont'] = random.choice(['H�tf�','Kedd','Szerda','Cs�t�rt�k','P�ntek'])
    return orarend

# Genetikus algoritmus futtat�sa
def genetic_algorithm(conn, generations=100, population=50, mutation_rate=0.1):
    # Adatok bet�lt�se
    hallgatok, kurzusok, oktatok, szakok, targyak, orarend = load_date(conn)

    # Kezdeti popul�ci�
    population = initial_population(population_size, kurzusok)

    for generation in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        new_population = []

        elite_count = population_size // 10
        new_population.extend(sorted(population, key=fitness, reverse=True)[:elite_count])

        # �j egyedek l�trehoz�sa
        while len(new_population) < population_size:
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        best_fitness = max(fitnesses)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

    # Legjobb megold�s
    best_schedule = max(population, key=fitness)
    return best_schedule

# F� program
if __name__ == "__main__":
    # Adatb�zis el�r�se

    best_schedule=genetic_algorithm(conn, generation=100, population_size=50, mutation_rate=0.1)
    

# Export�l�s JSON f�jlba
def export_to_json(schedule, filename="orarend.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(schedule, file, indent=4, ensure_ascii=False)
    print(f"�rarend export�lva a k�vetkez� f�jlba: {filename}")

# Export�l�s Excel f�jlba
def export_to_excel(schedule, filename="orarend.xlsx"):
    data = []
    for entry in schedule:
        data.append({
            "Kurzus ID": entry['kurzus_id'],
            "T�rgy ID": entry['targy_id'],
            "Oktat� ID": entry['oktato_id'],
            "Terem ID": entry['terem_id'],
            "Id�pont": entry['idopont'],
            "Csoport": entry['csoport']
        })

    df = pd.DataFram(data)
    df.to_excel(filename, index=False)
    print(f"�rarend export�lva a k�vetkez� f�jlba: {filename}")

# Export�l�s CSV f�jlba
def export_to_csv(schedule, filename="orarend.csv"):
    headers = ["Kurzus ID","T�rgy ID","Oktat� ID","Terem ID","Id�pont","Csoport"]

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
    print(f"�rarend export�lva a k�vetkez� f�jlba: {filename}")

export_to_csv(best_schedule)
export_to_excel(best_schedule)
export_to_json(best_schedule)