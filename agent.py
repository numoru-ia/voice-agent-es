"""Pipecat pipeline builder for a Spanish clinic receptionist."""
from __future__ import annotations

import os

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.services.openai import BaseOpenAILLMService
from pipecat.transports.network.fastapi_websocket import FastAPIWebsocketTransport
from pipecat.vad.silero import SileroVADAnalyzer
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext

from prompts import system_prompt
from tools import load_tools


async def run_agent(websocket, tenant_id: str):
    transport = FastAPIWebsocketTransport(
        websocket=websocket,
        params=FastAPIWebsocketTransport.InputParams(
            audio_sample_rate=8000,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            serializer="twilio",
        ),
    )

    stt = DeepgramSTTService(
        api_key=os.environ["DEEPGRAM_KEY"],
        language="es",
        model="nova-3",
    )

    tts = CartesiaTTSService(
        api_key=os.environ["CARTESIA_KEY"],
        voice_id=os.getenv("CARTESIA_VOICE", "mx-female-warm-v1"),
        language="es",
        speed=1.0,
    )

    llm = BaseOpenAILLMService(
        api_key=os.environ["LITELLM_MASTER_KEY"],
        base_url=os.environ.get("LITELLM_BASE_URL", "https://api.numoru.com/v1"),
        model=os.getenv("LLM_MODEL", "claude-sonnet"),
    )

    tools = load_tools(tenant_id)
    context = OpenAILLMContext(
        messages=[{"role": "system", "content": system_prompt(tenant_id)}],
        tools=tools,
    )

    pipeline = Pipeline([
        transport.input(),
        stt,
        context.user_aggregator(),
        llm,
        tts,
        transport.output(),
        context.assistant_aggregator(),
    ])

    runner = PipelineRunner()
    task = PipelineTask(pipeline)
    await runner.run(task)
