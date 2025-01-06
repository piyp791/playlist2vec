
FROM python:3.10
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/src
EXPOSE 3002
CMD ["uvicorn", "src.server:app",  "--host", "0.0.0.0", "--port", "3002"]