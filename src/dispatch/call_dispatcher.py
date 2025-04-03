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


async def entrypoint(ctx: agents.JobContext):
    logging.info(f"Job started. Metadata: {ctx.job.metadata}")
    await ctx.connect()

    phone_number = None
    try:
        metadata = json.loads(ctx.job.metadata)
        phone_number = metadata.get("phone_number")
    except Exception as e:
        logging.error("Error parsing job metadata", exc_info=e)


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
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o"),  
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
    )

    agent = SimulationAgent(personality="Friendly", objective="simulate a conversation")

    await session.start(
        room=ctx.room, 
        agent=agent,
    )

    await asyncio.sleep(10)
    logging.info("Simulated call finished.")


async def run_test() -> None:
    await entrypoint()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="my-test-agent" 
    ))
