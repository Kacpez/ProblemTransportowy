import random
import numpy as np

#inicjalizacja populacji losowej
def initialize_population(population_size,cost_matrix,supply,demand):
    population = []
    N,M=cost_matrix.shape
    for _ in range(population_size):
        chromosome = np.zeros((N, M), dtype=int)
        supply_copy = supply.copy()
        demand_copy = demand.copy()

        while np.sum(supply_copy) > 0 and np.sum(demand_copy) > 0:
            i, j = random.randint(0, N - 1), random.randint(0, M - 1)
            if supply_copy[i] > 0 and demand_copy[j] > 0:
                quantity = min(supply_copy[i], demand_copy[j])
                chromosome[i, j] = random.randint(0,quantity)
                supply_copy[i] -= quantity
                demand_copy[j] -= quantity
        #chromosome=adjust_supply_demand(chromosome,supply,demand)
        population.append(chromosome)
    return population

# Obliczenie kosztu transportu dla danego rozwiązania z karami
def fitness(individual, cost_matrix, supply, demand):
    total_fitness = np.sum(individual * cost_matrix)
    supply_penalty = np.sum(np.maximum(supply - np.sum(individual, axis=1), 0))
    demand_penalty = np.sum(np.maximum(demand - np.sum(individual, axis=0), 0))
    if supply_penalty>0 or demand_penalty>0:
      total_fitness = np.iinfo(np.int32).max
    return total_fitness

# Obliczenie kosztu transportu dla danego rozwiązania
def fitness2(individual, cost_matrix, supply, demand):
    total_cost = np.sum(individual * cost_matrix)
    return total_cost

#selekcja turniej n=5
def select_parents(population,cost_matrix,supply,demand):
    tournament_size = 5
    parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = min(tournament, key=lambda x: fitness(x, cost_matrix, supply, demand))
        parents.append(winner)
    return parents

#krzyżowanie
def crossover(parent1, parent2,N):
    crossover_point = random.randint(0, N - 1)
    child1 = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.vstack((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

#mutacja
def mutate(individual,supply,demand):
    i, j = random.randint(0, len(supply) - 1), random.randint(0, len(demand) - 1)
    k, l = random.randint(0, len(supply) - 1), random.randint(0, len(demand) - 1)
    max_possible_quantity = min(supply[i], demand[j])
    if supply[i] > 0 and demand[j] > 0:  # Check that the range is not empty
        rand = random.randint(0, min(supply[i], demand[j]))
    else:
        rand=0
    individual[i, j] = rand
    roznica=max_possible_quantity-rand
    if roznica%2==0:
      individual[i,l]+=roznica/2
      individual[k,j]+=roznica/2
    else:
      individual[i,l]+=(roznica+1)/2-1
      individual[k,j]+=(roznica+1)/2
    return individual

def adjust_supply_demand(individual, supply, demand):
    N, M = individual.shape

    # Adjust supply
    for i in range(N):
        total_supply = np.sum(individual[i, :])
        if total_supply != supply[i]:
            diff = total_supply - supply[i]
            for j in reversed(np.argsort(individual[i, :])):
                if diff == 0:
                    break
                adjustment = min(abs(diff), individual[i, j])
                if diff > 0:
                    individual[i, j] -= adjustment
                    diff -= adjustment
                else:
                    individual[i, j] += adjustment
                    diff += adjustment

    # Adjust demand
    for j in range(M):
        total_demand = np.sum(individual[:, j])
        if total_demand != demand[j]:
            diff = total_demand - demand[j]
            for i in reversed(np.argsort(individual[:, j])):
                if diff == 0:
                    break
                adjustment = min(abs(diff), individual[i, j])
                if diff > 0:
                    individual[i, j] -= adjustment
                    diff -= adjustment
                else:
                    individual[i, j] += adjustment
                    diff += adjustment


    for j in range(M):
            total_supply = np.sum(individual[:, j])
            if total_supply > demand[j]:
                excess = total_supply - demand[j]
                while excess != 0:
                    for i in range(N):
                        if individual[i, j] > 0:
                            quantity_to_reduce = min(excess, individual[i, j])
                            individual[i, j] -= quantity_to_reduce
                            excess -= quantity_to_reduce


    for i in range(N):
            if np.sum(individual[i, :]) != supply[i]:
                shortage = abs(supply[i] - np.sum(individual[i, :]))
                while shortage != 0:
                    j = np.argmax(demand)
                    if shortage >= demand[j]:
                        quantity_to_add = demand[j]
                    else:
                        quantity_to_add = shortage
                    individual[i, j] += quantity_to_add
                    shortage -= quantity_to_add


    for j in range(M):
            if np.sum(individual[:, j]) != demand[j]:
                shortage = abs(demand[j] - np.sum(individual[:, j]))
                while shortage != 0:
                    i = np.argmax(supply)
                    if shortage >= supply[i]:
                        quantity_to_add = supply[i]
                    else:
                        quantity_to_add = shortage
                    individual[i, j] += quantity_to_add
                    shortage -= quantity_to_add
                    
    return individual




#algrytm genetyczny
def genetic_algorithm(population_size, generations, mutation_rate, cost_matrix, supply, demand):
    if not cost_matrix.any():
        raise ValueError("Empty matrix, ")
    if sum(supply) != sum(demand):
        raise ValueError("Demand and supply sums do not match")
    if len(supply)==0 or len(demand)==0:
        raise ValueError("Empty demand or supply list")
    N, M = cost_matrix.shape
    population = initialize_population(population_size, cost_matrix, supply, demand)
    costs_history=[]
    for generation in range(generations):
        parents = select_parents(population, cost_matrix,supply,demand)
        children = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = crossover(parent1, parent2, N)
            children.append(child1)
            children.append(child2)
        for i in range(len(children)):
            if random.random() < mutation_rate:
               children[i]= mutate(children[i], supply, demand)
            children[i] = adjust_supply_demand(children[i], supply.copy(), demand.copy())
        population = children

        best_solution = min(population, key=lambda x: fitness(x, cost_matrix, supply, demand))

        best_solution=adjust_supply_demand(best_solution, supply.copy(), demand.copy())
        best_cost = fitness2(best_solution, cost_matrix, supply, demand)
        costs_history.append(best_cost)

    return best_solution, best_cost,costs_history


if __name__ == "__main__":
    # Parametry algorytmu
    population_size = 200
    generations = 100
    mutation_rate = 0.3
    # Definicja problemu transportowego
    num_sources = 3  
    num_destinations = 4  
    supply = [70,50,80]  #[60,70,90,80]
    demand = [40,60,50,50]  #[100,120,80] 
    cost_matrix = np.array([[50,40,50,20],[40,80,70,30],[60,40,70,80]]) #[[4,8,11],[6,14,5],[11,12,6],[9,7,13]])

    # Uruchomienie algorytmu
    best_solution, best_cost,cost_history = genetic_algorithm(population_size, generations, mutation_rate,cost_matrix,supply,demand)
    print("Najlepsze rozwiązanie:")
    print(best_solution)
    print("Koszt dostawy:", best_cost)
    print(cost_history)
