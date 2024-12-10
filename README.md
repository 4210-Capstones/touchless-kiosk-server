# touchless-kiosk-server

## Run completely in Docker Step by Step

1. Git clone the touchless kiosk server in your command prompt / console.

2. Download Docker Desktop then open the terminal in docker.

3. Using the terminal go to the directory where you git cloned the touchless kiosk server.
  
4.  Run the command: `docker-compose -f docker-compose.dev.yml up` 
  

Use flag `-d` to detach

## Run database ~~in Docker~~ and API locally:

1. ~~`docker-compose -f docker-compose.dev.yml up database`~~
2. Create new python environment (f.e. with conda) with python 12.
3. pip install "fastapi[standard]"
4. pip install --upgrade -r requirements.txt
5. ~~In .env, change "database" to "localhost" in DATABASE_URL (do **not** commit this change!!!).~~
6. Launch App from project root.   
   `uvicorn backend.main:app --reload`

## Docs

Go to http://localhost:8000/docs to see the docs (both local and docker)

## Example usage with curl:
[Attention: Those commands reflect the API on Nov 26th. URLs and schemas might have changed, if it doesn't work.]
**Create user**:   
Send content as json   
`curl -X POST -H "Content-Type: application/json" -d "{\"user_email\": \"user@example.com\", \"user_passwo
rd\": \"12345678\"}" http://localhost:8000/users/`   
**Log in**:   
Send request form as form data    
`curl -X POST -d "username=user@example.com&password=12345678" http://localhost:8000/login/`   
You receive: `{"access_token":"[your_token]","token_type":"bearer"}`

**Get user** (restricted endpoint):    
Send token in header   
`curl -X GET -H "Authorization: Bearer [your_token]" http://localhost:8000/users/profile`    
You should receive: `{"email":"user@example.com"}`

## Running tests

Run locally:   
`pytest`

Run in docker:
- Open internal docker console of "app" service and do as above or
- Run one of the command on an external console:   
  `docker-compose -f docker-compose.dev.yml exec app pytest`

To disable warnings add `--disable-warnings` flag

## Development

### !!!
**DO NOT** work on the main branch, create your own, or even better: create one per issue.   
When you finish development, run the tests, and fix stuff until all of them run successfully.   
Then, merge the updated main branch into your branch, and run the tests again. If changes to main occurred in the meantime, redo the process.
Only then, merge your updated branch back into main, push it.
### !!!

For most purposes the following will be sufficient:

1. The API part only handles API related logic.
   - [If necessary: Create a new `xyzAPI.py` file in backend/api. Introduce a new router, include it to app in `main.py`]
   - Create a new endpoint in `xyzAPI.py` file. Keep the following in mind:
     - If your endpoint needs a body, e.g. more complicated data like a class, create a schema in `classes/schemas.py` and use it as input to the endpoint
     - If your endpoint needs access to the database, include it with `db: Session = Depends(get_db)` as parameter and pass it down.
     - If your endpoint needs to be restricted, e.g. only available to logged in users, include `user: User = Depends(get_current_user)` as parameter (or `get_current_admin` etc, if it is already implemented)
     - If your endpoint needs to return more complicated data like a class, create a response in `classes/responses.py` and use that
   - For the rest, call a function in the handler
2. The handler deals with high end-logic (doesn't deal with database directly)
   - [If necessary: Create a new `xyzHandler.py` file in `backend/handler`.]
   - Create a function which the endpoint will call
   - Deal with high end-logic (f.e. hash a password)
   - To interact with the database call a Service function (located in `database/Service`)
3. To interact with the database, create a new Service class
   - Each table in the database has to have its own Service class to enable interaction
   - Make it inherit from the parent Service class. It will add basic functionality, like create, get, update, delete.
   - Specify the used table with `model_class = ...`
   - [If necessary, you can overwrite create, get, etc. for your service class, but this should rarely be the case]
   - Extend your Service class with more functionality (f.e. for user: `get_by_mail`)
4. Create your own database classes in `classes/db_classes`. Those will mirror database entries as python objects.
   - Make your class inherit from the database parent class. It introduces an `id` parameter and generates a table name from the class name
   - Add `__abstract__ = False` to your class
   - Follow the introduced structure
   - To get help with relationships between classes, reach out to POD4
   - **DO NOT** change existing class attributes
   - The database is automatically created on startup
   - It might happen, that your local database won't be compatible with new changes to the database. In this case, delete all tables or delete the entire database ~~docker image~~ in `res/development.db` (it will delete all data)
5. Add tests to your endpoint. Things to keep in mind:
   - The testing session creates a new local database separate from the rest
   - Tests should not depend on each other, use pytest fixtures to input necessary data
   - Fixtures in `conftest.py` are available to all tests. Look at the fixtures already defined
   - To have access to the client, or any other fixture, include it as parameter
   - To use the database do: `with get_test_db() as db:`
   - To create a new testfile:
     - Name it `test_xyz.py`, otherwise it will not be auto-detected
     - Include as the very first two lines:   
       `import os`    
       `os.environ['RUNNING_TESTS'] = 'true'`



