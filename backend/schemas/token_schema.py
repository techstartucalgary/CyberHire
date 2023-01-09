from pydantic import BaseModel

class Token(BaseModel):
    """
    Model for returning a token
    """
    access_token: str
    token_type: str