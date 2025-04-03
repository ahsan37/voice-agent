from dataclasses import dataclass

@dataclass
class VoiceAgent:
    id: str # Primary key, must be unique
    name: str
    system_prompt: str
    llm_model_id: str
    tts_model_id: str
    stt_model_id: str
    voice_id: str
    personality: str