import random


class BacterialEvolutionAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, n_classes, n_days, n_slots):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.n_classes = n_classes
        self.n_days = n_days
        self.n_slots = n_slots

        # Inicializálás
        self.population = self.initialize_population()

    def initialize_population(self):
        # Véletlenszerű órarendek generálása
        population = []
        for _ in range(self.population_size):
            individual = self.create_individual()
            population.append(individual)
        return population

    def create_individual(self):
        # Véletlenszerű órarend létrehozása (pl. 10 tantárgy, 5 nap, 6 időpont)
        return {class_id: (random.randint(1, self.n_days), random.randint(1, self.n_slots)) for class_id in range(1, self.n_classes + 1)}

    def fitness(self, individual):
        # Az órarendek fitneszének mérése (pl. ütközések számának minimalizálása)
        fitness_value = 0
        for class_id, (day, slot) in individual.items():
            # Példa: ha két tantárgy ugyanazon a napon és időpontban van, az ütközés
            for other_class_id, (other_day, other_slot) in individual.items():
                if class_id != other_class_id and day == other_day and slot == other_slot:
                    fitness_value += 1
        return fitness_value

    def mutate(self, individual):
        # Véletlenszerű mutációk (pl. tantárgyak újra elosztása a napok között)
        if random.random() < self.mutation_rate:
            class_id = random.choice(list(individual.keys()))
            individual[class_id] = (random.randint(
                1, self.n_days), random.randint(1, self.n_slots))
        return individual

    def evolve(self):
        for generation in range(self.generations):
            # Fitnesz kiszámítása a populációra
            fitness_values = [self.fitness(individual)
                              for individual in self.population]

            # Kiválasztás: legjobb egyedek megtartása
            sorted_population = [x for _, x in sorted(
                zip(fitness_values, self.population), key=lambda item: item[0])]
            self.population = sorted_population[:self.population_size // 2]

            # Reprodukció: a legjobb egyedek párosítása
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = random.sample(self.population, 2)
                child = self.crossover(parent1, parent2)
                new_population.append(child)

            # Mutáció alkalmazása
            self.population.extend(new_population)
            self.population = [self.mutate(individual)
                               for individual in self.population]

        # A legjobb órarend visszaadása
        best_individual = min(self.population, key=self.fitness)
        return best_individual

    def crossover(self, parent1, parent2):
        # Keresztezés: két egyed kombinálása
        child = {}
        for class_id in range(1, self.n_classes + 1):
            if random.random() < 0.5:
                child[class_id] = parent1[class_id]
            else:
                child[class_id] = parent2[class_id]
        return child
