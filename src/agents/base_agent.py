import logging
from livekit.agents.voice import Agent

class BaseSimulationAgent(Agent):
    def __init__(self, personality: str, objective: str):
        self.personality = personality
        self.objective = objective
        instructions = (
            f"You are a voice AI assistant with a {personality} personality, "
            f"whose objective is to {objective}."
        )
        super().__init__(instructions=instructions)
        logging.info(
            f"Initialized BaseSimulationAgent with personality '{personality}' and objective '{objective}'."
        )