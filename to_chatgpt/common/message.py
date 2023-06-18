import time

from to_chatgpt.common import role_map


def convert_messages_to_prompt_without_role(messages):
    prompt = ""
    for message in messages:
        content = message["content"]
        prompt += f"\n{content}"
    return prompt


def convert_messages_to_prompt_with_role(messages):
    prompt = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        transformed_role = role_map[role]
        prompt += f"\n{transformed_role.capitalize()}: {content}"
    return prompt


def to_chatgpt_response(response_str):
    openai_response = {
        "id": f"chatcmpl-{str(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-3.5-turbo-0301",
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response_str,
                },
                "index": 0,
                "finish_reason": "stop"
            }
        ],
    }

    return openai_response


def to_chatgpt_response_stream(response_str, finish_reason):
    openai_response = {
        "id": f"chatcmpl-{str(time.time())}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "gpt-3.5-turbo-0301",
        "choices": [
            {
                "delta": {
                    "content": response_str,
                },
                "index": 0,
                "finish_reason": finish_reason,
            }
        ],
    }

    return openai_response
