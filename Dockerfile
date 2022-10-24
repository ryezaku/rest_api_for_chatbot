FROM python:3.7
RUN ls
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

CMD ["python", "fast_api.py"]