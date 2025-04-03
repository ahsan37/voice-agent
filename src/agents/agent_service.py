from models.voice_agent import VoiceAgent

# For prototyping, we use an in-memory dictionary to store agents, in production we would use a database
voice_agents = {
    "agent_001": VoiceAgent(
        id="agent_001",
        name="Test Agent",
        system_prompt="You are a helpful assistant.",
        llm_model_id="gpt-4o-mini",
        tts_model_id="sonic-english",
        stt_model_id="nova-3",
        voice_id="c2ac25f9-ecc4-4f56-9095-651354df60c0",
        personality="Friendly and helpful"
    ),
    "agent_002": VoiceAgent(
        id="agent_002",
        name="Test Agent",
        system_prompt="You are an unhelpful assistant.",
        llm_model_id="gpt-4o-mini",
        tts_model_id="sonic-english",
        stt_model_id="nova-3",
        voice_id="c2ac25f9-ecc4-4f56-9095-651354df60c0",
        personality="Unhelpful and rude"
    ),
    # Additional agents can be added here
}

def get_agent(agent_id: str) -> VoiceAgent:
    """
    Retrieve an agent from the database.
    """
    agent = voice_agents.get(agent_id)
    if not agent:
        raise ValueError(f"Agent with ID {agent_id} not found.")
    
    return agent

def add_agent(agent: VoiceAgent):
    """
    Add an agent to the database.
    """
    voice_agents[agent.id] = agent
    return agent

def delete_agent(agent_id: str):
    """
    Delete an agent from the database.
    """
    del voice_agents[agent_id]
