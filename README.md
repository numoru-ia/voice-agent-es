# voice-agent-es

Spanish-language AI receptionist (Pipecat + Deepgram + Cartesia + Qdrant + Langfuse).
Twilio Media Streams → websocket → Pipecat pipeline → LLM via LiteLLM.

Companion to: [Construir un recepcionista IA en español](https://numoru.com/contribuciones/recepcionista-ia-vapi-pipecat-espanol).

## Cost per call

~0.11 USD (2.5 min average). TTFS 900-1200 ms.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --host 0.0.0.0 --port 8765
```

Twilio TwiML:

```xml
<Response>
  <Connect>
    <Stream url="wss://voz.numoru.com/ws/clinica-123" />
  </Connect>
</Response>
```
