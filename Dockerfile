FROM python:3.12

WORKDIR /container

ENV PYTHONPATH=/container

COPY requirements.txt /container/requirements.txt

RUN pip install "fastapi[standard]"

RUN pip install --no-cache-dir --upgrade -r /container/requirements.txt

COPY . /container/.

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]