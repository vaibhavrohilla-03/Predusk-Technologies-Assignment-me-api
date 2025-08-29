
FROM python:3.10-slim AS base

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED 1

WORKDIR /code


RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

COPY ./requirements.txt .

RUN uv pip install --system -r requirements.txt

# Copy the entire backend directory into the working directory
COPY ./backend /code

# Use 0.0.0.0 to make it accessible from outside the container for render
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]