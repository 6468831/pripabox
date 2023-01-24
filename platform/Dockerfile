FROM python:3.9-slim
EXPOSE 8000

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# COPY requirements.txt /tmp/requirements.txt
# RUN pip --no-cache-dir install --upgrade pip & pip install -r /tmp/requirements.txt


WORKDIR /src/platform

COPY . /src/platform/

