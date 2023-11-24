FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install numpy matplotlib pandas pyarrow boto3

CMD ["python", "./morfo.py"]
