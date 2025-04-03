import logging
import asyncio
from src.agents.base_agent import BaseSimulationAgent

class SimulationAgent(BaseSimulationAgent):
    def __init__(self, personality: str, objective: str):
        super().__init__(personality, objective)

    async def on_enter(self) -> None:
        logging.info("SimulationAgent on_enter: starting conversation.")
        await self.session.say("Hello, this is a simulation agent. Let's start the conversation!")
        
        for turn in range(3):
            logging.info(f"SimulationAgent conversation turn {turn+1}")
            await asyncio.sleep(2)  
            await self.session.say(f"This is simulation turn {turn+1}.")
        
        logging.info("SimulationAgent conversation test complete.")