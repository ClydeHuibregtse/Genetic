import matplotlib.pyplot as plt

class Agent(object):

    def __init__(self):
        pass

    def _updateparams(self, params):
        pass

    @staticmethod
    def mate(agent1, agent2):
        pass

    @staticmethod
    def reproduce(agent1):
        pass

    def mutate(self):
        pass

    def eval(self):
        pass




class Session:
    def __init__(self, agents, iterations=100, epochs=5):
        self.iterations = iterations
        self.epochs = epochs
        self.agents = agents

    def run(self):
        for epoch in self.epochs:

            for iteration in self.iterations:
                pass




class GameBoard(object):
    def __init__(self, dims=(100,100) ):
        self.dims = dims
