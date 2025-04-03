# simulate_dispatch.py
import asyncio
import random
import string
from livekit import api
from dotenv import load_dotenv

load_dotenv()

async def simulate_job():
    lkapi = api.LiveKitAPI()  
    
    # Generate a unique room name for this simulated job.
    unique_suffix = "".join(random.choices(string.digits, k=10))
    room_name = f"test-room-{unique_suffix}"
    
    # Create a dispatch job for the worker.
    dispatch = await lkapi.agent_dispatch.create_dispatch(
        api.CreateAgentDispatchRequest(
            agent_name="my-test-agent",  # This must match the agent_name you set in WorkerOptions.
            room=room_name,
            metadata='{"phone_number": "+17133055217"}' 
        )
    )
    print("Dispatch created:", dispatch)
    await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(simulate_job())
