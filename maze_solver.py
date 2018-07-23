import matplotlib.pyplot as plt
import string
import random
import time

class GameBoard(object):
    def __init__(self, board, start, final):
        self.board = board
        self.start = start
        self.final = final

    def __repr__(self):
        outboard = ""

        for r in range(len(self.board)):
            outboard += "\n"
            for c in range(len(self.board[0])):
                outboard += " "
                outboard += str(self.board[r][c])



        return outboard


    def find_all_pos(self, position):

        x, y = position

        out_set = set()
        for xi in range(-1, 2):
            for yi in range(-1,2):

                if xi != 0 and yi != 0:
                    continue

                if xi == 0 and yi == 0:
                    continue

                if 0 <= x + xi < len(self.board) and 0 <= y + yi < len(self.board[0]) and self.board[x+xi][y+yi] == " ":

                    out_set.add((x + xi, y + yi))


        return out_set

    @staticmethod
    def render_from_file(filename):
        out_board = list()
        start = None
        final = None
        with open(filename, "r") as f:
            lines = f.readlines()

            for line in lines:

                row = list()
                for char in list(line):

                    if char == "S":
                        start = (lines.index(line), list(line).index(char))
                    if char == "F":
                        final = (lines.index(line), list(line).index(char))



                    row.append(1) if char == "1" else row.append(" ")



                out_board.append(row)
            return GameBoard(out_board, start, final)



class Agent(object):

    def __init__(self, moves=None):
        if not moves:
            self.moves = []
        else:
            self.moves = moves

    def make_moves(self, gameboard):

        if not self.moves:
            starting_pos = gameboard.start
            # self.moves.append(starting_pos)

        else:
            starting_pos = self.moves[-1]


        next_move = random.choice(list(gameboard.find_all_pos(starting_pos)))

        while next_move not in self.moves:
            if next_move == gameboard.final:

                self.moves.append(next_move)

                break

            self.moves.append(next_move)
            next_move = random.choice(list(gameboard.find_all_pos(next_move)))

    @staticmethod
    def mate(agent1, agent2, gameboard, crossover_prob=0.5):
        new_moves = list()
        for i in range(min(len(agent1.moves), len(agent2.moves))):
            ## Poor algorithm
            if agent1.moves[i] == agent2.moves[i]:
                new_moves.append(agent1.moves[i])
            else:
                break

        child = Agent(new_moves)
        child.make_moves(gameboard)
        return child

    @staticmethod
    def reproduce(agent1):
        return Agent(agent1.moves)

    def mutate(self, gameboard):
        if not self.moves:
            return

        change_index = random.choice(range(len(self.moves)))
        new_change = random.choice(list(gameboard.find_all_pos(self.moves[change_index])))

        if new_change != self.moves[change_index]:
            self.moves[change_index] = new_change

        self.moves = self.moves[change_index:]

        self.make_moves(gameboard)


    def eval(self,gameboard):
        x, y = self.moves[-1] if self.moves else gameboard.start
        fx, fy = gameboard.final

        dis = ((fx - x)**2 + (fy - y)**2)**0.5

        return dis

    def render(self, gameboard):
        px, py = self.moves[-1] if self.moves else gameboard.start
        outboard = list(gameboard.board[:])
        outboard[px][py] = "X"

        return repr(GameBoard(outboard))


class Session:
    def __init__(self, agents, iterations=10000, epochs=5,
                    mutation_prob=0.5, mating_fraction=1, repro_fraction=.4):

        self.iterations = iterations
        self.epochs = epochs
        self.agents = agents
        self.mutation_prob = mutation_prob
        self.mating_fraction = mating_fraction
        self.repro_fraction = repro_fraction


    def run(self, gameboard):
        print(gameboard.final)
        for epoch in range(self.epochs):

            for iteration in range(self.iterations):
                if iteration %100 == 0:
                    print(iteration)
                # print(gameboard.board)
                # Sort by eval
                srt_agents = sorted(self.agents[:], key=lambda x: x.eval(gameboard))
                # print(srt_agents[0].moves[-1])
                # print(srt_agents[0].render(gameboard), srt_agents[0].eval(gameboard))
                if srt_agents[0].eval(gameboard) == 0.0:

                    return srt_agents[0].moves, srt_agents

                # Kill the worst of the agents
                srt_agents = srt_agents[len(srt_agents) - int(len(srt_agents)*self.repro_fraction):]

                for agent in srt_agents[:]:

                    # Try for mutation amongst all agents
                    if random.uniform(0,1) < self.mutation_prob:

                        agent.mutate(gameboard)

                    # Try for mating for each of the mutated, spliced off agents
                    if random.uniform(0,1) < self.mating_fraction and len(srt_agents)<len(self.agents):

                        child = Agent.mate(agent, random.choice(srt_agents), gameboard)

                        srt_agents.append(child)


                while len(srt_agents) < len(self.agents):
                    srt_agents.append(Agent.reproduce(random.choice(srt_agents)))


                self.agents = srt_agents


if __name__ == "__main__":
    # game = GameBoard(
    # [[1,1,1,1,1,1,1],
    #  [1," "," ",1,1,1,1],
    #  [" "," ",1,1,1,1,1],
    #  [1," ",1,1,1,1,1],
    #  [1," "," ",1,1,1,1],
    #  [1,1," "," "," "," "," "],
    #  [1,1,1,1,1,1,1]]
    # )

    game = GameBoard.render_from_file("test_mazes/test_1.txt")
    print(repr(game))
    # print(game.find_all_pos((2,1)))

    agents = []
    for i in range(1000):
        new_ag = Agent()
        new_ag.make_moves(game)
        agents.append(new_ag)

    ses = Session(agents)
    output,_ = ses.run(game)
    print(output)


#
