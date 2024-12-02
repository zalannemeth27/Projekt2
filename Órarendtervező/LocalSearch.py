import random

class LocalSearchAlgorithm:
    def __init__(self, n_classes, n_days, n_slots):
        self.n_classes = n_classes
        self.n_days = n_days
        self.n_slots = n_slots
        self.best_schedule = None
        self.best_fitness = float('inf')

    def generate_initial_solution(self):
        # Kezdeti véletlenszerű órarend generálása
        schedule = {}
        for class_id in range(1, self.n_classes + 1):
            day = random.randint(1, self.n_days)
            slot = random.randint(1, self.n_slots)
            schedule[class_id] = (day, slot)
        return schedule

    def fitness(self, schedule):
        # Fitnesz érték (ütközések számának minimalizálása)
        fitness_value = 0
        for class_id, (day, slot) in schedule.items():
            for other_class_id, (other_day, other_slot) in schedule.items():
                if class_id != other_class_id and day == other_day and slot == other_slot:
                    fitness_value += 1
        return fitness_value

    def generate_neighbors(self, current_solution):
        # Szomszédos megoldások generálása (pl. két tantárgy cseréje)
        neighbors = []
        for _ in range(self.n_classes * 2):
            neighbor = current_solution.copy()
            class_id = random.choice(list(neighbor.keys()))
            other_class_id = random.choice(list(neighbor.keys()))
            
            # Két tantárgy cseréje
            neighbor[class_id], neighbor[other_class_id] = neighbor[other_class_id], neighbor[class_id]
            neighbors.append(neighbor)
        return neighbors

    def search(self):
        # Lokális keresés végrehajtása
        current_solution = self.generate_initial_solution()
        current_fitness = self.fitness(current_solution)

        # Kezdeti megoldás mentése
        self.best_schedule = current_solution
        self.best_fitness = current_fitness

        # Iterációk végrehajtása
        improved = True
        while improved:
            improved = False
            neighbors = self.generate_neighbors(current_solution)
            for neighbor in neighbors:
                neighbor_fitness = self.fitness(neighbor)
                if neighbor_fitness < current_fitness:
                    current_solution = neighbor
                    current_fitness = neighbor_fitness
                    if current_fitness < self.best_fitness:
                        self.best_schedule = current_solution
                        self.best_fitness = current_fitness
                    improved = True
                    break  # Ha találtunk jobb szomszédot, akkor azonnal lépünk tovább
        return self.best_schedule
