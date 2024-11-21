# touchless-kiosk-server

## Run completely in Docker

Run the command:

`docker-compose -f docker-compose.dev.yml up`

## Run database in Docker and API locally:

1. `docker-compose -f docker-compose.dev.yml up database`
2. Create new python environment (f.e. with conda) with python 12.
3. pip install "fastapi[standard]"
4. pip install --upgrade -r /container/requirements.txt
5. In .env, change "database" to "localhost" in DATABASE_URL.
6. Launch App with working directory set to backend.    
   In PyCharm, adjust it in run configuration and mark backend directory as source root.   
   [TODO: Find way to do it on command line, normal command (wont work): `uvicorn backend.main:app --reload`]