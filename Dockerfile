FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install python-numpy python-scipy -y

# RUN useradd -ms /bin/bash djangouser

ADD . /app

RUN pip install pip==18 && pip install -r /app/requirements.txt

# USER djangouser

EXPOSE 8080
CMD ["python", "/app/main.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]