FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /
CMD ["uvicorn", "serve:app", "--reload", "--host", "0.0.0.0", "--port", "8000"] 
# Replace 'main:app' if different in your FastAPI setup
