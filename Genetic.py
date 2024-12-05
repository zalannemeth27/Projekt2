import random

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, crossover_rate, 
                 n_classes, n_days, n_slots, subject_constraints):
        self.n_classes = n_classes
        self.n_days = n_days
        self.n_slots = n_slots
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.subject_constraints = subject_constraints  # [(KurzusID, TargyID, OktatoID, Kod, Nev, Kredit), ...]

    def generate_population(self):
        # Kezdeti populáció generálása: véletlenszerű órarendek
        population = []
        for _ in range(self.population_size):
            schedule = {i: (random.randint(0, self.n_days - 1), random.randint(0, self.n_slots - 1)) for i in range(self.n_classes)}
            population.append(schedule)
        return population

    def fitness(self, schedule):
        fitness_value = 0
        
        # Ütközések ellenőrzése
        for kurzus_id1, (day1, slot1) in schedule.items():
            for kurzus_id2, (day2, slot2) in schedule.items():
                if kurzus_id1 != kurzus_id2:
                    # Időpont ütközés
                    if day1 == day2 and slot1 == slot2:
                        # Ellenőrizzük, hogy ugyanaz az oktató-e
                        oktato1 = self.get_oktato(kurzus_id1)
                        oktato2 = self.get_oktato(kurzus_id2)
                        
                        if oktato1 == oktato2:  # Oktató ütközés
                            fitness_value += 10
                        
                        fitness_value += 5  # Általános időpont ütközés
        
        return fitness_value

    def get_oktato(self, kurzus_id):
        for kurzus in self.subject_constraints:
            if kurzus[0] == kurzus_id:  # KurzusID egyezés
                return kurzus[2]  # OktatoID visszaadása
        return None

    def select_parents(self, population):
        # Szülők kiválasztása a legjobb fitnesz alapján
        population_sorted = sorted(population, key=self.fitness)
        return population_sorted[:2]  # Kiválasztjuk a két legjobb egyedet

    def crossover(self, parent1, parent2):
        # Keresztezés: egyesíti két szülő órarendjét
        child = {}
        for class_id in parent1:
            if random.random() < 0.5:
                child[class_id] = parent1[class_id]
            else:
                child[class_id] = parent2[class_id]
        return child

    def mutate(self, schedule):
        # Mutáció: véletlenszerűen módosítja egy órarend elemét
        if random.random() < self.mutation_rate:
            class_id = random.randint(0, self.n_classes - 1)
            schedule[class_id] = (random.randint(0, self.n_days - 1), random.randint(0, self.n_slots - 1))
        return schedule

    def evolve(self):
        population = self.generate_population()
        for generation in range(self.generations):
            new_population = []
            while len(new_population) < self.population_size:
                parents = self.select_parents(population)
                parent1, parent2 = parents[0], parents[1]
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population
        
        # Válasszuk ki a legjobb órarendet a végén
        best_schedule = min(population, key=self.fitness)
        return best_schedule


