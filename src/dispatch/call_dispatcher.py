import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import asyncio
import logging
import os
import json
from livekit import agents, api
from livekit.agents.voice import AgentSession
from livekit.plugins import openai, deepgram, silero, cartesia
from src.agents.simulation_agent import SimulationAgent
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_AGENT_NAME = os.getenv("LIVEKIT_AGENT_NAME")

async def entrypoint(ctx: agents.JobContext):
    logging.info(f"Job started. Metadata: {ctx.job.metadata}")
    await ctx.connect()

    phone_number, system_prompt, llm_model_id, tts_model_id, stt_model_id, voice_id, personality = retrieve_metadata(ctx)

    if phone_number:
        SIP_TRUNK_ID = os.environ.get("LIVEKIT_SIP_TRUNK_ID")    
        try:
            await ctx.api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=ctx.room.name,
                    sip_trunk_id=SIP_TRUNK_ID,
                    sip_call_to=phone_number,
                    participant_identity=phone_number, 
                )
            )
            logging.info(f"Outbound call initiated to {phone_number}")
        except Exception as e:
            logging.error("Failed to create SIP participant for outbound call", exc_info=e)
    else:
        logging.info("No phone number provided in metadata; skipping outbound call.")

    session = AgentSession(
        stt=deepgram.STT(model=stt_model_id),
        llm=openai.LLM(model=llm_model_id),  
        tts=cartesia.TTS(model=tts_model_id, voice=voice_id),
        vad=silero.VAD.load(),
    )

    agent = SimulationAgent(personality=personality, objective=system_prompt)

    await session.start(
        room=ctx.room, 
        agent=agent,
    )

    logging.info("Simulated call finished.")


async def run_test() -> None:
    await entrypoint()

def retrieve_metadata(ctx: agents.JobContext):
    try:
        metadata_dict = json.loads(ctx.job.metadata)
    except (json.JSONDecodeError, TypeError):
        logging.error("Job metadata was not valid JSON.")
        return None
    
    phone_number = metadata_dict.get("phone_number")
    system_prompt = metadata_dict.get("system_prompt")
    llm_model_id = metadata_dict.get("llm_model_id")
    tts_model_id = metadata_dict.get("tts_model_id")
    stt_model_id = metadata_dict.get("stt_model_id")
    voice_id = metadata_dict.get("voice_id")
    personality = metadata_dict.get("personality")

    return phone_number, system_prompt, llm_model_id, tts_model_id, stt_model_id, voice_id, personality

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="test-agent",
        num_idle_processes=3
    ))
