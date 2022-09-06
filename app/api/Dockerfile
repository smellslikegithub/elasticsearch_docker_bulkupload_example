FROM python:3.10-buster

# Setup working directory
WORKDIR /app/api

# Install dependencies before copying stuff in order to cache steps
COPY ./requirements.txt /app/api

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . /app/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]