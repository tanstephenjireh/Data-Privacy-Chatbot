# 
FROM python:3.10

# 
WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --progress-bar off

# 
COPY . /code

# #
# RUN alembic revision --autogenerate -m "scaffold tables"

# RUN alembic upgrade head


RUN chmod +x entrypoint.sh


ENTRYPOINT ["/code/entrypoint.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
