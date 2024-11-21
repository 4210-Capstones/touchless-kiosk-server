from pydantic import BaseModel


class Token(BaseModel):
    """
    This is the token class. An object is returned if user logs in.
    To access restricted endpoints, user must send this token in the header in the form of:
    {"Authorization": f'Bearer {access_token}'}
    This is done automatically if using OpenAPI Docs.
    """

    access_token: str
    token_type: str