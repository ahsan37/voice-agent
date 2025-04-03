# simulate_dispatch.py
import asyncio
import random
import string
import os
import logging
import json

from livekit import api
from dotenv import load_dotenv
from src.agents.agent_service import get_agent
from models.voice_agent import VoiceAgent

load_dotenv()

logger = logging.getLogger(__name__)

async def simulate_job(agents: list[VoiceAgent]):
    lkapi = api.LiveKitAPI()

    CUSTOMER_PHONE_NUMBER = os.getenv("CUSTOMER_PHONE_NUMBER")
    LIVEKIT_AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME")

    for i, agent in enumerate(agents, start=1):

        # We'll create a unique room name for each dispatch
        room_name = f"outbound-call-room-{i}"
        # We'll pass in JSON metadata with phone_number and initial_message
        metadata = {
            "phone_number": CUSTOMER_PHONE_NUMBER,
            "system_prompt": agent.system_prompt,
            "llm_model_id": agent.llm_model_id,
            "tts_model_id": agent.tts_model_id,
            "stt_model_id": agent.stt_model_id,
            "voice_id": agent.voice_id,
            "personality": agent.personality
        }

        logger.info(f"Dispatching agent {agent.name} with ID {agent.id} to room {room_name}")
        dispatch_request = api.CreateAgentDispatchRequest(
            agent_name=LIVEKIT_AGENT_NAME,  # Must match our agent's WorkerOptions.agent_name
            room=room_name,
            metadata=json.dumps(metadata)
        )

        # This calls out to your LiveKit server, instructing it to dispatch our $LIVEKIT_AGENT_NAME agent
        dispatch = await lkapi.agent_dispatch.create_dispatch(dispatch_request)
        logger.info(f"Created dispatch: {dispatch}")
   
    await lkapi.aclose()

if __name__ == "__main__":
    # TODO: Generate custom agents with LLM here and add them to this list
    agents = [get_agent("agent_001"), get_agent("agent_002")]
    asyncio.run(simulate_job(agents))
