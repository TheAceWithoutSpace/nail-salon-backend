from pydantic import BaseModel


class SendLoginCodeRequest(BaseModel):
    phone_number: str


class VerifyLoginCodeRequest(BaseModel):
    phone_number: str
    code: str
