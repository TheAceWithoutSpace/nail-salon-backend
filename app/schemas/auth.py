from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator, model_validator


class SendLoginCodeRequest(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

    @model_validator(mode='after')
    def check_either_field(self) -> 'SendLoginCodeRequest':
        if not self.phone_number and not self.email:
            raise ValueError("Either phone_number or email must be provided")
        return self


class VerifyLoginCodeRequest(BaseModel):
    phone_number: str
    code: str
