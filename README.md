# TO CHATGPT

**Make you feel free to use ALL chatgpt applications!!!**

There are many LLM online services now, but most of the desktop clients, browser plugins, and ChatGPT-enhanced Web currently use OpenAI interfaces. If this restriction can be broken, I believe it will make us **get off work earlier**, such as claude, cohere, new bing, google bard, etc.

For this, and inspired by the [claude to chatgpt](https://github.com/jtsang4/claude-to-chatgpt) project, I decided to give it a try, go go go !!!

**CATALOG**

- [Usage](#usage)
- [How to use it](#how-to-use-it)
- [Roadmap](#roadmap)
- [Awesome chatgpt applications](#awesome-chatgpt-applications)
- [Awesome open and OpenAI-Compatible llms](#awesome-open-and-openai-compatible-llms)

## Usage

Before using, you need to ensure that the current environment can access the corresponding llm services.

### adapter param

It is worth noting that there are currently **two types of adapters**, one is asynchronous and the other is synchronous.
The factor that decides which category to use is the sdk that currently accesses the online LLM service.
If an asynchronous interface is provided, asynchronous implementation will be given priority.

Specify the adapter through `-a`, which has been implemented so far.

**async adapters**:

- claude, implemented using [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python). The current account needs to apply, if successful, you can use it for **free** for personal daily use.
- cohere, implemented using [cohere-python](https://github.com/cohere-ai/cohere-python). You only need to register an account, and you can use it for **free** for individuals, but there is a rate limit, five times a minute.
- new_bing, implemented using [EdgeGPT](https://github.com/acheong08/EdgeGPT), which is reverse engineered API of Microsoft's Bing Chat AI. Because Currently new bing does not provide an official sdk, and it caused this way is **unstable**.

**sync adapters**:

- bard, implemented using [Bard](https://github.com/acheong08/Bard/), which is reverse engineered API of Google Bard. And it's also **unstable**.

If you want to use the `cohere` api in ChatGPT applications now, you only need to start the service, like:

```bash
python app.py -a cohere
```

Another point to note is that because some APIs are non-asynchronous, such as the current `bard`, you need to run the `app_sync.py` file, like:

```bash
python app_sync.py -a bard
```

### source code

```bash
git clone https://github.com/SimFG/to-chatgpt
cd to-chatgpt

pip install poetry
poetry install
python app.py -a new_bing
```

### docker

```bash
docker pull simfg/to_chatgpt:latest

docker run -d -p 8000:8000 simfg/to_chatgpt:0.1
```

Specify the adapter to run the service.

```bash
docker run -d -p 8000:8000 simfg/to_chatgpt:latest poetry run python app.py -a new_bing
```

## How to use it

If you find that the service **does not respond normally, you can check if there is any error output in the service console.** It is very likely that there is a problem accessing the llm service.

If you want to specify the port of the service, you can use the `-p` parameter.

Set the **openai base url** in the chatgpt application as the service address. Generally, this option is near the openai api key.

Different adapters have different usage methods, and the instructions are as follows.

1. claude

After starting the service, specify the api key of the claude service where OPENAI_API_KEY is required.

2. cohere

After starting the service, specify the api key of the cohere service where OPENAI_API_KEY is required.

3. new bing

Nothing, but it's unstable.

4. bard

After starting the service, specify `__Secure-1PSID` cookie where OPENAI_API_KEY is required.

The way to get the cookie:

- F12 for console
- Copy the values
  - Session: Go to Application → Cookies → \_\_Secure-1PSID. Copy the value of that cookie.

more details: [Bard](https://github.com/acheong08/Bard/)

## Roadmap

### Support more llm services

- [text-generation-inference](https://github.com/huggingface/text-generation-inference)
- [OpenLLM](https://github.com/bentoml/OpenLLM)
- open-assistant

If there are other llm services, **welcome to open a pr and write it here**!!!

### Manage your llm service and its data

Through this service, in addition to conversion, LLM requests and related data can also be managed.

**Of course, I may not have time to do all the functions below, all of which are my personal imagination.**

- Customize the service key to limit service requests
- LLM service key management
- Request limit
- Whitelist and Blacklist IP
- Record the request history
- Manager the request info page, like show/download/delete/various charts...

## Awesome chatgpt applications

### plugins

- [openai-translator](https://github.com/openai-translator/openai-translator)
- [chathub](https://github.com/chathub-dev/chathub)

### client

- [raycast chatgpt extension](https://github.com/raycast/extensions/blob/c0f80c73f39b1cd7159e53b706c452c12648f0a9/extensions/chatgpt/README.md)

If there are other awesome chatgpt applications, **welcome to open a pr and write it here**!!!

## Awesome open and OpenAI-Compatible llms

- [FastChat](https://github.com/lm-sys/FastChat)
- [vllm](https://github.com/vllm-project/vllm)

If there are other open and OpenAI-Compatible llms, **welcome to open a pr and write it here**!!!

These open-source LLM models provide OpenAI-compatible APIs for its supported models, so you can use them as a local drop-in replacement for OpenAI APIs. These servers is compatible with both openai-python library and cURL commands.

Take fastchat as an example:

```bash
# start the server
python3 -m fastchat.serve.controller
python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.3
python3 -m fastchat.serve.openai_api_server --host localhost --port 8000

# use the openai api
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vicuna-7b-v1.3",
    "messages": [{"role": "user", "content": "Hello! What is your name?"}]
  }'
```
more fastchat detais: [FastChat And OpenAI API](https://github.com/lm-sys/FastChat/blob/main/docs/openai_api.md)
