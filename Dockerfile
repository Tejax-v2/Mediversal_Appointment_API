FROM python:3.12

WORKDIR /mediversal

COPY . /mediversal/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]