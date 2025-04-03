from models.voice_agent import VoiceAgent
from src.agents.agent_generator import generate_voice_agents
from typing import List, Dict, Optional
from openai import OpenAI

voice_agents: Dict[str, VoiceAgent] = {}

def initialize_agents(user_system_prompt: str, num_agents: int, client: Optional[OpenAI] = None):
    global voice_agents
    generated_agents = generate_voice_agents(user_system_prompt, num_agents, client)
    
    voice_agents.clear()
    
    for agent in generated_agents:
        voice_agents[agent.id] = agent

def get_all_agents() -> List[VoiceAgent]:
    """
    Retrieve all agents from the dictionary.
    """
    return list(voice_agents.values())

def get_agent(agent_id: str) -> VoiceAgent:
    """
    Retrieve an agent from the dictionary.
    """
    agent = voice_agents.get(agent_id)
    if not agent:
        raise ValueError(f"Agent with ID {agent_id} not found.")
    
    return agent

def add_agent(agent: VoiceAgent):
    """
    Add an agent to the dictionary.
    """
    voice_agents[agent.id] = agent
    return agent

def delete_agent(agent_id: str):
    """
    Delete an agent from the dictionary.
    """
    if agent_id in voice_agents:
        del voice_agents[agent_id]
    else:
        raise ValueError(f"Agent with ID {agent_id} not found.")
