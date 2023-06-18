import asyncio
import json
from os import environ

from Bard import Chatbot
from pydantic import BaseModel
from starlette.requests import Request

from to_chatgpt.common import (
    BaseAdapter,
    convert_messages_to_prompt_without_role,
    to_chatgpt_response_stream,
    to_chatgpt_response,
    logger,
)


class BardAdapter(BaseModel, BaseAdapter):
    async def achat(self, request: Request):
        pass

    def chat(self, request: Request):
        openai_params = asyncio.run(request.json())
        logger.info(f"bard_params:{json.dumps(openai_params)}")

        messages = openai_params["messages"]
        prompt = convert_messages_to_prompt_without_role(messages)
        is_stream = openai_params.get("stream", False)

        headers = request.headers
        auth_header = headers.get("authorization", None)
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = environ.get("BARD_TOKEN")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            chatbot = Chatbot(token)
            res = chatbot.ask(prompt)
        except Exception as e:
            bard_token = environ.get("BARD_TOKEN")
            if bard_token:
                logger.error(f"fail to ask, token: {token}, exception: {e}")
                chatbot = Chatbot(bard_token)
                res = chatbot.ask(prompt)
        finally:
            loop.close()

        logger.info(f"bard_response:{json.dumps(res)}")
        response_text = res["content"]

        if is_stream:
            yield to_chatgpt_response_stream(response_text, None)
            yield to_chatgpt_response_stream("", "stop")
            yield "[DONE]"
        else:
            yield to_chatgpt_response(response_text)
