import matplotlib.pyplot as plt
import string
import random
import time

from difflib import SequenceMatcher


allchars = string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits + " "

correct_word = input("Please provide a phrase: ")
# correct_word = "Hello!"
def word_generator(size=len(correct_word), chars=allchars):
    return "".join(random.choice(chars) for _ in range(size))


class Agent(object):

    def __init__(self, guess):
        self.guess = guess


    @staticmethod
    def mate(agent1, agent2, crossover_prob=0.5):
        # if len(agent1.guess) != len(agent2.guess):
        #     print("agents have mismatched guesses; unable to mate")
        #     return

        outguess = ''
        for i in range(min(len(agent1.guess), len(agent2.guess))):

            if random.uniform(0,1) < 0.5:
                outguess += agent1.guess[i]
            else:
                outguess += agent2.guess[i]

        if len(agent1.guess) > len(agent2.guess):
            outguess += agent1.guess[len(agent2.guess):]
        else:
            outguess += agent2.guess[len(agent1.guess):]

        return Agent(outguess)


    @staticmethod
    def reproduce(agent1):
        return Agent(agent1.guess)

    def mutate(self):

        new_char = random.choice(allchars)

        guess = list(self.guess)
        guess[random.choice(range(len(self.guess)))] = new_char

        self.guess = "".join(guess) if Agent(guess).eval() > self.eval() else self.guess

    def eval(self):
        count = 0
        for i in range(len(self.guess)):
            if self.guess[i] == correct_word[i]:
                count += 1

        return count / len(self.guess)
        # return SequenceMatcher(None, self.guess, correct_word).ratio()



class Session:
    def __init__(self, agents, correct_word, iterations=1000, epochs=5,
                    mutation_prob=0.2, mating_fraction=1, repro_fraction=.5):

        self.iterations = iterations
        self.epochs = epochs
        self.agents = agents
        self.mutation_prob = mutation_prob
        self.mating_fraction = mating_fraction
        self.repro_fraction = repro_fraction


    def run(self):
        for epoch in range(self.epochs):
            # self.diversify()

            for iteration in range(self.iterations):


                # Sort by eval
                srt_agents = sorted(self.agents[:], key=lambda x: x.eval())
                print(srt_agents[0].guess)
                if srt_agents[0].eval() == 1.0:
                    return self.agents[0].guess, self.agents

                # Kill the worst of the agents
                srt_agents = srt_agents[len(srt_agents) - int(len(srt_agents)*self.repro_fraction):]

                for agent in srt_agents[:]:

                    # Try for mutation amongst all agents
                    if random.uniform(0,1) < self.mutation_prob:

                        agent.mutate()

                    # Try for mating for each of the mutated, spliced off agents
                    if random.uniform(0,1) < self.mating_fraction and len(srt_agents)<len(self.agents):

                        child = Agent.mate(agent, random.choice(srt_agents))
                        # print("CHILD: ", child.guess)
                        srt_agents.append(child)


                while len(srt_agents) < len(self.agents):
                    srt_agents.append(Agent.reproduce(random.choice(srt_agents)))

                # # Re-sort with all the new agents
                # srt_agents = sorted(srt_agents, key=lambda x: x.eval(), reversed=False)
                #

                self.agents = srt_agents


if __name__ == "__main__":
    now = time.time()
    # test_agent = Agent("helko!")
    test_agent_2 = Agent("ello?a")
    # agents = [test_agent, test_agent_2]
    agents = []
    for i in range(10000):
        agents.append(Agent(word_generator()))

    new_ses = Session(agents, correct_word)
    output,_ = new_ses.run()
    print(output, time.time()-now)

    # print(SequenceMatcher(None, "ello ", "Hello").ratio())


    #
    # test_agent = Agent("helko!")
    # test_agent_2 = Agent("H3flo?")
    # agents = [test_agent,test_agent_2]
    # srt_agents = sorted(agents[:], key=lambda x: x.eval())[::-1]
    # for ag in srt_agents:
    #     print(ag.eval(), ag.guess)
    # # print(Agent.mate(test_agent, test_agent_2).guess)
    # print(test_agent.eval())
