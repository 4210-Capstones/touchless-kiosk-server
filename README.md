# touchless-kiosk-server

## Running the Database in Docker and Code
### Dependencies
pip install python-dotenv

pip install sqlalchemy

pip install sqlalchemy-utils
### Building and Running the Postgres Image/Container in Docker
docker-compose -f docker-compose.dev.yml up
### Running the Code to Test
py backend/main.py (from root directory)
or cd backend and then py main.py