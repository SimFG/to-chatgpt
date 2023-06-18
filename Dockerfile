FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install

ENV PATH=$PATH:/usr/local/bin

EXPOSE 8000

# Set the command to run the application
CMD ["poetry", "run", "python", "app.py", "-a", "new_bing"]
