import json
import uuid
import logging
import random
from openai import OpenAI
from models.voice_agent import VoiceAgent
from typing import List, Optional

logger = logging.getLogger(__name__)

LLM_MODELS = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]
TTS_MODELS = ["sonic-english", "echo", "shimmer"]
STT_MODELS = ["nova-3"]

DEFAULT_LLM_MODEL = "gpt-4o-mini"
DEFAULT_TTS_MODEL = "sonic-english"
DEFAULT_STT_MODEL = "nova-3"

AVAILABLE_VOICES = [
    "c2ac25f9-ecc4-4f56-9095-651354df60c0",  
    "7ed24487-c70b-44f8-a65a-3a4d0a8e221a",  
    "9f4a6f95-72b3-4a64-8dce-4ef8bcc5ae46",  
]

def generate_agent_id() -> str:
    return f"agent_{uuid.uuid4().hex[:8]}"

def get_random_voice_id() -> str:
    return random.choice(AVAILABLE_VOICES)

def get_random_model(model_list, default_model):
    return random.choice(model_list) if model_list else default_model

def generate_voice_agents(user_system_prompt: str, num_agents: int, client: Optional[OpenAI] = None) -> List[VoiceAgent]:

    if client is None:
        client = OpenAI()
    
    logger.info(f"Generating {num_agents} voice agents based on user system prompt...")
    
    gpt_prompt = f"""
    You are tasked with creating {num_agents} distinct voice agents that will call and interact with a voice assistant.
    
    The voice assistant they will interact with has the following system prompt:
    "{user_system_prompt}"
    
    For each agent, generate:
    1. A name (short and descriptive)
    2. A distinct personality description 
    3. A specific objective or goal for the conversation based on the user's system prompt.
    
    Return ONLY a valid JSON array with no additional text, where each object has keys:
    - 'name': The agent's name
    - 'personality': The agent's personality description
    - 'objective': The conversation objective
    
    The response must be valid JSON parseable by json.loads() in Python.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates testing scenarios. Return only valid JSON with no additional text."},
                {"role": "user", "content": gpt_prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        result_text = response.choices[0].message.content.strip()
        
        try:
            json_data = json.loads(result_text)
            
            # Handle various response formats
            if isinstance(json_data, dict):
                # Look for arrays in the response
                for key in json_data:
                    if isinstance(json_data[key], list):
                        agent_data = json_data[key]
                        break
                else:
                    # If the response is a single agent
                    if all(k in json_data for k in ['name', 'personality', 'objective']):
                        agent_data = [json_data]
                    else:
                        raise ValueError("JSON response doesn't contain expected agent data")
            elif isinstance(json_data, list):
                agent_data = json_data
            else:
                raise ValueError("JSON response is neither a list nor a dictionary")
            
            voice_agents = []
            for data in agent_data[:num_agents]:  
                agent_id = generate_agent_id()
                agent = VoiceAgent(
                    id=agent_id,
                    name=data.get('name', f"Agent {agent_id}"),
                    system_prompt=data.get('objective', "Have a conversation with the user."),
                    llm_model_id=get_random_model(LLM_MODELS, DEFAULT_LLM_MODEL),
                    tts_model_id=get_random_model(TTS_MODELS, DEFAULT_TTS_MODEL),
                    stt_model_id=get_random_model(STT_MODELS, DEFAULT_STT_MODEL),
                    voice_id=get_random_voice_id(),
                    personality=data.get('personality', "Friendly and helpful")
                )
                voice_agents.append(agent)
            
            logger.info(f"Successfully generated {len(voice_agents)} voice agents")
            return voice_agents
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.debug(f"Raw response: {result_text}")
            raise
            
    except Exception as e:
        logger.error(f"Error generating voice agents: {e}")
        return _create_default_agents(num_agents, user_system_prompt)

def _create_default_agents(num_agents: int, user_system_prompt: str) -> List[VoiceAgent]:
    """Create default agents if GPT generation fails."""
    logger.info(f"Creating {num_agents} default voice agents")
    
    default_personalities = [
        "Friendly and helpful",
        "Impatient and direct", 
        "Curious and inquisitive",
        "Confused and needs clarification",
        "Technical and precise"
    ]
    
    default_objectives = [
        "Get detailed information about services",
        "Resolve a specific problem quickly",
        "Learn about the system capabilities",
        "Understand how the assistant works",
        "Test the assistant's knowledge"
    ]
    
    agents = []
    for i in range(num_agents):
        idx = i % len(default_personalities)
        agent_id = generate_agent_id()
        agent = VoiceAgent(
            id=agent_id,
            name=f"Agent {i+1}",
            system_prompt=default_objectives[idx],
            llm_model_id=get_random_model(LLM_MODELS, DEFAULT_LLM_MODEL),
            tts_model_id=get_random_model(TTS_MODELS, DEFAULT_TTS_MODEL),
            stt_model_id=get_random_model(STT_MODELS, DEFAULT_STT_MODEL),
            voice_id=get_random_voice_id(),
            personality=default_personalities[idx]
        )
        agents.append(agent)
    
    return agents
