
FROM python:3.10.13-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir uv


COPY ./requirements.txt .

RUN uv pip install --system --no-cache-dir -r requirements.txt


COPY ./backend /code/

# Use 0.0.0.0 to make it accessible from
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]