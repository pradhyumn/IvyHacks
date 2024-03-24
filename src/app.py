"""
Main web application service. Serves the static frontend as well as
API routes for transcription, language model generation and text-to-speech.
"""

import json
from pathlib import Path

from modal import Mount, asgi_app

from .common import stub
# from .llm_zephyr import Zephyr
from .transcriber import Whisper
from .tts import Tortoise

static_path = Path(__file__).with_name("frontend").resolve()

PUNCTUATION = [".", "?", "!", ":", ";", "*"]


@stub.function(
    mounts=[Mount.from_local_dir(static_path, remote_path="/assets")],
    container_idle_timeout=300,
    timeout=600,
)
@asgi_app()
def web():
    from fastapi import FastAPI, Request
    from fastapi.responses import Response, StreamingResponse
    from fastapi.staticfiles import StaticFiles
    from io import BytesIO
    from .pdf_processing.extract_text import ExtractText
    from fastapi.responses import JSONResponse
    import anthropic
    import os
    import dotenv
    from .LLM_prompting.interview_anthropic import analyse_and_generate
    from .LLM_prompting.interview_anthropic import kickoff

    dotenv.load_dotenv()


    web_app = FastAPI()
    transcriber = Whisper()
    text_extractor= ExtractText()
    # llm = Zephyr()
    tts = Tortoise()
    client=anthropic.Anthropic(api_key= os.getenv("CLAUDE_API_KEY"))

    @web_app.post("/transcribe")
    async def transcribe(request: Request):
        bytes = await request.body()
        result = transcriber.transcribe_segment.remote(bytes)
        return result["text"]
    
    @web_app.post("/upload_resume")
    async def upload(request: Request):
        body = await request.form()
        file = body["file"]
        bytes = await file.read()
        buffer=BytesIO(bytes)

        extracted_text= text_extractor.extract_text_from_pdf(buffer)
        try:
            message = text_extractor.send_text_to_claude_api(extracted_text, client)
            # text_extractor.resume=extracted_text
            return JSONResponse(content={"text": message.content[0].text}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
        
    @web_app.post("/upload_job_description")
    async def upload_job_description(request: Request):
        body = await request.form()
        if "file" not in body:
            extracted_text= body["jd"]
        else:
            file = body["file"]
            bytes = await file.read()
            buffer=BytesIO(bytes)

            extracted_text= text_extractor.extract_text_from_pdf(buffer)
            # text_extractor.job_description=extracted_text
        return JSONResponse(content={"text": extracted_text}, status_code=200)
    
    @web_app.post("/kick_off")
    async def kick_off_response(request: Request):
        body = await request.json()
        tts_enabled = body["tts"]
        if "noop" in body:
            # llm.generate.spawn("")
            # Warm up 3 containers for now.
            if tts_enabled:
                for _ in range(3):
                    tts.speak.spawn("")
            return

        def speak(sentence):
            if tts_enabled:
                fc = tts.speak.spawn(sentence)
                return {
                    "type": "audio",
                    "value": fc.object_id,
                }
            else:
                return {
                    "type": "sentence",
                    "value": sentence,
                }

        def gen():
            sentence = ""

            for segment in kick_off(candidate_profile=body["resume"],job_description=body["jd"],client=client):
                yield {"type": "text", "value": segment}
                sentence += segment

                for p in PUNCTUATION:
                    if p in sentence:
                        prev_sentence, new_sentence = sentence.rsplit(p, 1)
                        yield speak(prev_sentence)
                        sentence = new_sentence

            if sentence:
                yield speak(sentence)

        def gen_serialized():
            for i in gen():
                yield json.dumps(i) + "\x1e"

        return StreamingResponse(
            gen_serialized(),
            media_type="text/event-stream",
        )
    
    @web_app.post("/generate")
    async def generate_questions(request: Request):
        body=await request.json()
        tts_enabled = body["tts"]

        if "noop" in body:
            # llm.generate.spawn("")
            # Warm up 3 containers for now.
            if tts_enabled:
                for _ in range(3):
                    tts.speak.spawn("")
            return

        def speak(sentence):
            if tts_enabled:
                fc = tts.speak.spawn(sentence)
                return {
                    "type": "audio",
                    "value": fc.object_id,
                }
            else:
                return {
                    "type": "sentence",
                    "value": sentence,
                }

        def gen():
            sentence = ""

            for segment in analyse_and_generate(candidate_emotion_analysis="Candidate looks neutral", 
                                                candidate_response=body["input"],interview_history=body["history"],
                                                time_left="10 minutes",candidate_profile=body["resume"],
                                                job_description=body["jd"],client=client):
                yield {"type": "text", "value": segment}
                sentence += segment

                for p in PUNCTUATION:
                    if p in sentence:
                        prev_sentence, new_sentence = sentence.rsplit(p, 1)
                        yield speak(prev_sentence)
                        sentence = new_sentence

            if sentence:
                yield speak(sentence)

        def gen_serialized():
            for i in gen():
                yield json.dumps(i) + "\x1e"

        return StreamingResponse(
            gen_serialized(),
            media_type="text/event-stream",
        )

    @web_app.get("/audio/{call_id}")
    async def get_audio(call_id: str):
        from modal.functions import FunctionCall

        function_call = FunctionCall.from_id(call_id)
        try:
            result = function_call.get(timeout=30)
        except TimeoutError:
            return Response(status_code=202)

        if result is None:
            return Response(status_code=204)

        return StreamingResponse(result, media_type="audio/wav")

    @web_app.delete("/audio/{call_id}")
    async def cancel_audio(call_id: str):
        from modal.functions import FunctionCall

        print("Cancelling", call_id)
        function_call = FunctionCall.from_id(call_id)
        function_call.cancel()

    web_app.mount("/", StaticFiles(directory="/assets", html=True))
    return web_app
