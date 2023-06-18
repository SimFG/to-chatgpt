import json
from typing import Optional

from EdgeGPT.EdgeGPT import Chatbot
from EdgeGPT.conversation_style import ConversationStyle
from fastapi import Request
from pydantic import BaseModel

from to_chatgpt.common import (
    convert_messages_to_prompt_without_role,
    to_chatgpt_response,
    to_chatgpt_response_stream,
    logger,
    BaseAdapter,
)


class NewBingAdapter(BaseModel, BaseAdapter):
    bot: Optional[Chatbot] = None
    style: str = "creative"
    prompt: str = ""
    is_stream: bool = False

    class Config:
        arbitrary_types_allowed = True

    def openai_to_bing_params(self, openai_params):
        messages = openai_params["messages"]
        self.prompt = convert_messages_to_prompt_without_role(messages)

        if openai_params.get("temperature"):
            temp = int(openai_params.get("temperature"))
            if temp > 1.5:
                self.style = "precise"
            elif temp > 0.8:
                self.style = "balanced"
            else:
                self.style = "creative"

        if openai_params.get("stream"):
            self.is_stream = True
        else:
            self.is_stream = False

    async def achat(self, request: Request):
        openai_params = await request.json()
        self.openai_to_bing_params(openai_params)
        if not self.bot:
            self.bot = await Chatbot.create()
        logger.info(f"new_bing_param:{json.dumps(openai_params)}")
        if not self.is_stream:
            res = await self.bot.ask(
                prompt=self.prompt,
                conversation_style=getattr(ConversationStyle, self.style),
            )
            logger.info(f"new_bing_response:{json.dumps(res)}")
            res = res["item"]["messages"][-1]["text"]
            await self.bot.reset()
            yield to_chatgpt_response(res)
        else:
            last_response = ""
            async for final, response in self.bot.ask_stream(
                prompt=self.prompt,
                conversation_style=getattr(ConversationStyle, self.style),
                raw=True,
            ):
                if final:
                    logger.info(f"new_bing_stream_response:{json.dumps(response)}")
                    await self.bot.reset()
                    if last_response == "":
                        res = response["item"]["messages"][-1]["text"]
                        yield to_chatgpt_response_stream(res, None)
                    yield to_chatgpt_response_stream("", "stop")
                    yield "[DONE]"
                else:
                    arguments = response.get("arguments", [{}])
                    if len(arguments) == 0:
                        arguments = [{}]
                    messages = arguments[0].get("messages", [])
                    if len(messages) == 0:
                        messages = [{}]
                    response = messages[0].get("text", "")
                    if len(last_response) < len(response):
                        yield to_chatgpt_response_stream(
                            response[len(last_response) :], None
                        )
                        last_response = response
                    else:
                        yield to_chatgpt_response_stream("", None)
