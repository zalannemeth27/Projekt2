import random

class AntColonyAlgorithm:
    def __init__(self, population_size, generations, pheromone_decay, pheromone_intensity, n_classes, n_days, n_slots):
        self.population_size = population_size
        self.generations = generations
        self.pheromone_decay = pheromone_decay
        self.pheromone_intensity = pheromone_intensity
        self.n_classes = n_classes       # Tantárgyak száma
        self.n_days = n_days            # Napok száma
        self.n_slots = n_slots          # Az időpontok száma

        self.pheromone = self.initialize_pheromone()
        self.best_schedule = None
        self.best_fitness = float('inf')
    
    def initialize_pheromone(self):
        # Inicializáljuk a feromon mátrixot
        return {(class_id, day, slot): 1 for class_id in range(1, self.n_classes + 1) 
                                      for day in range(1, self.n_days + 1) 
                                      for slot in range(1, self.n_slots + 1)}

    def fitness(self, schedule):
        # Az órarendek fitneszének mérése (pl. ütközések számának minimalizálása)
        fitness_value = 0
        for class_id, (day, slot) in schedule.items():
            # Példa: ha két tantárgy ugyanazon a napon és időpontban van, az ütközés
            for other_class_id, (other_day, other_slot) in schedule.items():
                if class_id != other_class_id and day == other_day and slot == other_slot:
                    fitness_value += 1
        return fitness_value

    def construct_solution(self):
        # A hangyák elhelyezik az órarendet (minden egyed megoldást készít)
        schedule = {}
        for class_id in range(1, self.n_classes + 1):
            # Véletlen nap és időpont választása a feromon értékek alapján
            best_choices = self.get_best_choices(class_id)
            day, slot = random.choice(best_choices)
            schedule[class_id] = (day, slot)
        return schedule

    def get_best_choices(self, class_id):
        # A legjobb választások meghatározása a feromon alapján
        choices = []
        for day in range(1, self.n_days + 1):
            for slot in range(1, self.n_slots + 1):
                pheromone_value = self.pheromone.get((class_id, day, slot), 1)
                choices.append((day, slot, pheromone_value))
        # A választásokat rangsoroljuk a feromon intenzitása szerint
        choices.sort(key=lambda x: x[2], reverse=True)
        return [(day, slot) for day, slot, _ in choices]

    def update_pheromone(self, solutions):
        # Frissítjük a feromon mátrixot
        for solution, fitness_value in solutions:
            # Feromon intenzitásának frissítése a legjobb megoldások alapján
            for class_id, (day, slot) in solution.items():
                if fitness_value < self.best_fitness:
                    self.pheromone[(class_id, day, slot)] += self.pheromone_intensity / (fitness_value + 1)
                # Elhalványulás
                self.pheromone[(class_id, day, slot)] *= (1 - self.pheromone_decay)

    def evolve(self):
        # Generációk ciklusa
        for generation in range(self.generations):
            solutions = []
            for _ in range(self.population_size):
                solution = self.construct_solution()
                fitness_value = self.fitness(solution)
                solutions.append((solution, fitness_value))
                if fitness_value < self.best_fitness:
                    self.best_fitness = fitness_value
                    self.best_schedule = solution

            self.update_pheromone(solutions)
        
        return self.best_schedule


