# touchless-kiosk-server

## Run completely in Docker

Run the command:

`docker-compose -f docker-compose.dev.yml up`

## Run database in Docker and API locally:

1. `docker-compose -f docker-compose.dev.yml up database`
2. Create new python environment (f.e. with conda) with python 12.
3. pip install "fastapi[standard]"
4. pip install --upgrade -r requirements.txt
5. In .env, change "database" to "localhost" in DATABASE_URL.
6. Launch App with working directory set to backend.    
   In PyCharm, adjust it in run configuration and mark backend directory as source root.   
   [TODO: Find way to do it on command line, normal command (wont work): `uvicorn backend.main:app --reload`]

## Example usage with curl:

**Create user**:   
Send content as json   
`curl -X POST -H "Content-Type: application/json" -d "{\"email\": \"user@example.com\", \"password\": \"12345678\"}" http://localhost:8000/users/`

**Log in**:   
Send request form as form data    
`curl -X POST -d "username=user@example.com&password=12345678" http://localhost:8000/login/`   
You receive: `{"access_token":"[your_token]","token_type":"bearer"}`

**Get user** (restricted endpoint):    
Send token in header   
`curl -X GET -H "Authorization: Bearer [your_token]" http://localhost:8000/users/profil
e`    
You should receive: `{"email":"user@example.com"}`