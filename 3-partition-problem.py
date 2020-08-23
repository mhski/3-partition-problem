from itertools import combinations
from time import time
import json
import random


def generate_problem(size):
    random_array = [random.randint(1, 100) for n in range(size)]
    second_array = random_array[:]
    third_array = random_array[:]

    random.shuffle(second_array)
    random.shuffle(third_array)
    total_array = random_array + second_array + third_array

    return ThreePartitionProblem({"main_set": total_array})


def generate_problem_to_file(size, path_to_file):
    problem = generate_problem(size)
    problem.export_to_file(path_to_file)


class ThreePartitionProblem:
    def __init__(self, data):
        self.tries = 0
        self.data = data
        self.main_set = self.data["main_set"]

    def __str__(self):
        return "ThreePartitionProblem (main_set={})".format(self.main_set)

    @classmethod
    def import_from_file(cls, path_to_file):
        with open(path_to_file) as file:
            return cls(json.load(file))

    def export_to_file(self, path_to_file):
        with open(path_to_file, "w") as file:
            file.write(json.dumps(self.data))

    def generate_random_solution(self):
        temp_main_set = self.main_set[:]
        random.shuffle(temp_main_set)
        a = temp_main_set[1::3]
        b = temp_main_set[1::3]
        c = temp_main_set[2::3]

        return Solution({"set": self.main_set, "subsets": [a, b, c]})

    def bruteforce_find_subset_of_sum(self, set, number_to_be_found):
        size = len(set)
        for n in range(1, size + 1):
            for c in combinations(set, n):
                self.tries += 1
                print(c)
                if sum(c) == number_to_be_found:
                    return c
        return None

    def solve_with_bruteforce(self):
        self.tries = 0
        self.time = time()

        subsets = []
        temp_main_set = self.main_set[:]
        sum_of_main_set = sum(temp_main_set)

        for n in range(3):
            subset = self.bruteforce_find_subset_of_sum(temp_main_set, sum_of_main_set / 3)
            self.tries += 1
            for element in subset:
                if element in temp_main_set:
                    temp_main_set.remove(element)

            subsets.append(subset)

        self.time = time() - self.time
        return Solution({"set": self.main_set, "subsets": subsets})

    def find_close_neighbour(self, solution):
        subsets = solution.subsets.copy()
        subsets.sort(key=sum)

        for index in range(3):
            subsets[index].sort()

        subsets[0].append(subsets[2].pop(0))

        return Solution({"set": solution.set, "subsets": subsets})

    def solve_with_climbing(self, limit=10000):
        self.tries = 0
        self.time = time()

        best_solution = self.generate_random_solution()
        print(best_solution)

        for _ in range(limit):
            print("Best solution so far: {}".format(best_solution))
            neighbour = self.find_close_neighbour(best_solution)
            self.tries +=1
            if abs(sum(neighbour.subsets[0]) + sum(neighbour.subsets[1]) + sum(neighbour.subsets[2])) < abs(
                    sum(best_solution.subsets[0]) + sum(best_solution.subsets[1]) + sum(best_solution.subsets[2])):
                best_solution = neighbour

            if sum(neighbour.subsets[0]) == sum(neighbour.subsets[1]) == sum(neighbour.subsets[2]):
                self.time = time() - self.time
                return best_solution

    def solve_with_greedy(self):
        self.tries = 0
        self.time = time()
        a = []
        b = []
        c = []

        sum_a = 0
        sum_b = 0
        sum_c = 0

        for n in sorted(self.main_set, reverse=False):
            self.tries += 1
            if sum_a <= sum_b and sum_a <= sum_c:
                a.append(n)
                sum_a = sum_a + n
            elif sum_b <= sum_a and sum_b <= sum_c:
                b.append(n)
                sum_b = sum_b + n
            else:
                c.append(n)
                sum_c = sum_c + n

        self.time = time() - self.time
        return [Solution({"set": self.main_set, "subsets": [a, b, c]})]

class Solution:
    def __init__(self, data):
        self.data = data
        self.subsets = data["subsets"]
        self.set = data["set"]

    def export_to_file(self, path_to_file):
        with open(path_to_file, "w") as file:
            goal = self.goal()
            self.data["goal"] = goal

            file.write(json.dumps(self.data))

    def goal(self):
        if not all([isinstance(n, int) for n in self.set]):
            raise ValueError("The algorithm is designed to solve natural numbers")

        if len(self.set) % 3 != 0:
            raise ValueError("The set is not divisible by 3")

        if len(self.subsets) != 3:
            raise ValueError("The algoritm was not able to divide set into 3 subsets")

        first_result = abs(sum(self.subsets[0]) - sum(self.subsets[1]))
        second_result = abs(sum(self.subsets[1]) - sum(self.subsets[2]))
        third_result = abs(sum(self.subsets[0]) - sum(self.subsets[2]))

        return sum([first_result, second_result, third_result])

    def __str__(self):
        return str((self.subsets, self.goal()))

    def __repr__(self):
        return str(self)


def zapisz_rozwiazanie(solution):
    try:
        save_to_file = int(input("Czy chcesz zapisac do pliku rozwiazanie? (1-tak, inne-nie)\n"))
    except:
        return

    if save_to_file == 1:
        path = input("Podaj sciezke zapisu rozwiazania: ")
        solution.export_to_file(path)


def rozwiaz_dla_algorytmu(problem):
    choice = int(input("1: bruteforce\n2: wspinaczkowo\n3: greedy\n"))
    if choice == 1:
        return problem.solve_with_bruteforce()
    if choice == 2:
        return problem.solve_with_climbing()
    if choice == 3:
        return problem.solve_with_greedy()


if __name__ == "__main__":
    print("Wybierz opcje: ")
    print("1) 3 partition problem dla 3N-elementowego wygenerowanego zbioru")
    print("2) 3 partition problem dla zbioru z pliku")
    choice = int(input())

    if choice == 1:
        n = int(input("Podaj n:\n"))

        problem = generate_problem(n)

        print(problem)
        print("Rozwiazanie:\n")

        solution = rozwiaz_dla_algorytmu(problem)
        print(solution)
        print("Czas trwania: {}".format(problem.time))
        print("Ilość prób: {}".format(problem.tries))
        zapisz_rozwiazanie(solution)

    elif choice == 2:
        path = input("Podaj sciezke z problemem\n")
        problem = ThreePartitionProblem.import_from_file(path)

        print(problem)
        print("Rozwiazanie:\n")

        solution = rozwiaz_dla_algorytmu(problem)
        print(solution)
        print("Czas trwania: {}".format(problem.time))
        print("Ilość prób: {}".format(problem.tries))
        zapisz_rozwiazanie(solution)
