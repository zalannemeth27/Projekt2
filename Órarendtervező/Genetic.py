import random

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, crossover_rate, n_classes, n_days, n_slots):
        self.n_classes = n_classes
        self.n_days = n_days
        self.n_slots = n_slots
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def generate_population(self):
        # Kezdeti populáció generálása: véletlenszerű órarendek
        population = []
        for _ in range(self.population_size):
            schedule = {i: (random.randint(0, self.n_days - 1), random.randint(0, self.n_slots - 1)) for i in range(self.n_classes)}
            population.append(schedule)
        return population

    def fitness(self, schedule):
        # Fitnesz érték számítása: pl. ütközések, túlterhelés, stb.
        fitness_value = 0
        for class_id, (day, slot) in schedule.items():
            # Pl. minden órarend ütközés +1
            for other_class_id, (other_day, other_slot) in schedule.items():
                if class_id != other_class_id and day == other_day and slot == other_slot:
                    fitness_value += 1  # ütközés esetén növeljük a büntetést
        return fitness_value

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


