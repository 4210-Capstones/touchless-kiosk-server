from classes.db_classes import User, Roles, UserRoles
from database.Service import UserService
from database.config_db import create_db
from database.dependency_db import get_db
from database.config_db import engine

# just a test for db so far
if __name__ == '__main__':

    create_db()

    # UserRoles.__table__.drop(engine)
    # Roles.__table__.drop(engine)
    # User.__table__.drop(engine)

    user = User(email='<EMAIL>', password='<PASSWORD>')

    db = next(get_db())
    user_id = UserService.create(user, db).user_id
    print(f"User created with id {user_id}")

    db = next(get_db())
    print(f"Fetching User...: \n {UserService.get(user_id, db)}")

    db = next(get_db())
    print("Deleting User...")
    UserService.delete(user_id, db)


    db = next(get_db())
    if UserService.get(user_id, db) is None:
        print("Successfully deleted")
    else:
        print("Not successful")