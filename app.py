from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import groq, elevenlabs, silero
from dotenv import load_dotenv 
import os

# Load .env.local file for API keys
load_dotenv(dotenv_path=".env.local")

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # Define your voice assistant agent
    agent = Agent(
        instructions="""
            You are a helpful and friendly voice assistant.
            Greet the user and respond politely to their queries.
            End the conversation if the user says goodbye or exit.
        """
    )

    # Session setup with STT (Groq), LLM (Groq), and TTS (ElevenLabs)
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=groq.STT(model="whisper-large-v3-turbo", language="en"),
        llm=groq.LLM(model="llama3-8b-8192"),
        tts=elevenlabs.TTS( 
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id="ODq5zmih8GrVes37Dizd",
            model="eleven_multilingual_v2"
        )
    )

    await session.start(agent=agent, room=ctx.room)

    await session.generate_reply(
        instructions="Start by greeting the user and ask how you can help."
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
