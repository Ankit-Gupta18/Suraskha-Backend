# Suraskha-Backend

## create a new virtual env

python -m venv suraksha-backend-env

## activate the virtual env

source suraksha-backend-env/bin/activate

### install dependencies

pip install -r requirements.txt

## start server

uvicorn main:app --host 0.0.0.0 --port 8000



# Using docker

## build image

docker build -t suraksha-backend .

## start server

docker run -it --rm -p 8000:8000 --env-file .env suraksha-backend
