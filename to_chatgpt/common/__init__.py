import asyncio
import json
from abc import ABCMeta, abstractmethod

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, JSONResponse

from to_chatgpt.common.constant import role_map
from to_chatgpt.common.log import logger
from to_chatgpt.common.message import (
    convert_messages_to_prompt_without_role,
    to_chatgpt_response,
    to_chatgpt_response_stream,
)


class BaseAdapter(metaclass=ABCMeta):
    @abstractmethod
    async def achat(self, request: Request):
        pass

    def chat(self, request: Request):
        pass


def init_app():
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods, including OPTIONS
        allow_headers=["*"],
    )
    return app


async def achat(adapter: BaseAdapter, request: Request):
    openai_params = await request.json()
    is_stream = openai_params.get("stream", False)
    try:
        if is_stream:
            async def generate():
                async for stream_response in adapter.achat(request):
                    if stream_response == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    yield f"data: {json.dumps(stream_response)}\n\n"

            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            response = adapter.achat(request)
            openai_response = await response.__anext__()
            return JSONResponse(content=openai_response)
    except Exception as e:
        logger.exception("achat fail")
        if is_stream:
            async def generate():
                exception_data = json.dumps(to_chatgpt_response_stream(f"exception: {e}", None))
                stop_data = json.dumps(to_chatgpt_response_stream("", "stop"))
                yield f"data: {exception_data}\n\n"
                yield f"data: {stop_data}\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            return JSONResponse(content=to_chatgpt_response(f"exception: {e}"))


def chat(adapter: BaseAdapter, request: Request):
    openai_params = asyncio.run(request.json())
    is_stream = openai_params.get("stream", False)
    try:
        if is_stream:
            def generate():
                for stream_response in adapter.chat(request):
                    if stream_response == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    yield f"data: {json.dumps(stream_response)}\n\n"

            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            response = adapter.chat(request)
            openai_response = response.__next__()
            return JSONResponse(content=openai_response)
    except Exception as e:
        logger.exception("chat fail")
        if is_stream:
            async def generate():
                exception_data = json.dumps(to_chatgpt_response_stream(f"exception: {e}", None))
                stop_data = json.dumps(to_chatgpt_response_stream("", "stop"))
                yield f"data: {exception_data}\n\n"
                yield f"data: {stop_data}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            return JSONResponse(content=to_chatgpt_response(f"exception: {e}"))
