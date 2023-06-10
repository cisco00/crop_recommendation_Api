FROM python:3.11.1

WORKDIR /flaskapi-app

COPY requirements.txt .
COPY data_index_file.csv .
COPY model_building.csv .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./ ./app

CMD ["python", "./app/main.py"]