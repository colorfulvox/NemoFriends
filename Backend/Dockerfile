FROM python:3.10.5
WORKDIR /var/jenkins_home/workspace/deploy/Backend
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /var/jenkins_home/workspace/deploy/Backend/kospeech
RUN pip install -e .

COPY . .
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8000"]