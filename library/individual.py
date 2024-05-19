from random import choice, sample


class Individual:
    # we always initialize
    def __init__(self, representation=None, size=None, valid_set=None, repetition=True):

        if representation is None:
            if repetition:
                # individual will be chosen from the valid_set with a specific size
                self.representation = [choice(valid_set) for i in range(size)]
            else:
                self.representation = sample(valid_set, size)

        # if we pass an argument like Individual(my_path)
        else:
            self.representation = representation

        # fitness will be assigned to the individual
        self.fitness = self.get_fitness()

    # methods for the class
    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}"
