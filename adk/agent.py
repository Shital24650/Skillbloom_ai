# adk/agent.py

class Agent:
    def __init__(self, config):
        self.name = self.__class__.__name__
        self.config = config

    def execute(self, message):
        raise NotImplementedError("Agents must implement the execute() method.")
