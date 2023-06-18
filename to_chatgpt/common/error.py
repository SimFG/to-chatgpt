from to_chatgpt.common import to_chatgpt_response_stream, to_chatgpt_response


async def safe_chat(chat, is_stream, client):
    try:
        yield await chat()
    except Exception as e:
        if is_stream:
            yield to_chatgpt_response_stream(f"exception: {e}", None)
            yield to_chatgpt_response_stream("", "stop")
            yield "[DONE]"
        else:
            yield to_chatgpt_response(f"exception: {e}")
    finally:
        if client:
            client.close()
