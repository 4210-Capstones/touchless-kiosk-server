"""from classes.db_classes import User, Booking, BookingRoom, BookingType, Club, ClubRequest, Image, Role, UserRole, Tag, ImageTag, Room, ImageRequest
from database.Service import UserService
from database.config_db import create_db
from database.dependency_db import get_db
from database.config_db import engine
from sqlalchemy_data_model_visualizer import generate_data_model_diagram, add_web_font_and_interactivity"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.LoginAPI import login_router
from backend.api.UserAPI import user_router
from backend.database import config_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute before app start
    if os.getenv("RUNNING_TESTS") != "true":
        config_db.wait_for_database()
        config_db.create_db()

    yield

    # Execute after app end
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(login_router)

# just a test for db so far
"""if __name__ == '__main__':

    create_db()

    # Suppose these are your SQLAlchemy data models defined above in the usual way, or imported from another file:
    models = [User, Role, UserRole, Tag, Image, ImageTag, Room, Booking, ImageRequest, Club, ClubRequest]
    output_file_name = 'my_data_model_diagram'
    generate_data_model_diagram(models, output_file_name)
    add_web_font_and_interactivity('my_data_model_diagram.svg', 'my_interactive_data_model_diagram.svg')
    
    # BookingRoom.__table__.drop(engine)
    # Room.__table__.drop(engine)
    # ImageRequest.__table__.drop(engine)
    # ImageTag.__table__.drop(engine)
    # Tag.__table__.drop(engine)
    # Image.__table__.drop(engine)
    # ClubRequest.__table__.drop(engine)
    # Club.__table__.drop(engine)
    # Booking.__table__.drop(engine)
    # BookingType.__table__.drop(engine)
    # UserRole.__table__.drop(engine)
    # Role.__table__.drop(engine)
    # User.__table__.drop(engine)

    #user = User(user_email='bartholomew@aol.com', user_first='Bartholomew', user_last='Cornelius', user_password='password') 
    #user = User(user_email='drewbrees@gmail.com', user_first='Drew', user_last='Brees', user_password='password1')
    #user = User(user_email='toothless@yahoo.com', user_first='Toothless', user_last='Dragon', user_password='hiccup')

    # db = next(get_db())
    # user_id = UserService.create(user, db).id
    # print(f"User created with id {user_id}")

    db = next(get_db())
    # print(f"Fetching User...: \n {UserService.get(user_id, db)}")
    users = db.query(User).all()
    for user in users:
        print(f'{user.user_first} {user.user_last} belongs to the following roles')
        for role in user.user_roles:
            print(f'{role.role_name}')

    # db = next(get_db())
    # print("Deleting User...")
    # UserService.delete(user_id, db)


    # db = next(get_db())
    # if UserService.get(user_id, db) is None:
    #     print("Successfully deleted")
    # else:
    #     print("Not successful")"""