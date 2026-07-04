from pydantic import BaseModel, EmailStr, field_validator
from exception.password_exception import PasswordValidationException

class UserCreateSchema(BaseModel):
    name : str 
    email : EmailStr
    password :  str

    @field_validator('password')
    @classmethod
    def password_validator(cls, value):
        if len(value) < 8:
            raise PasswordValidationException("password should contain minimum 8 char")
        if not any(char.isupper() for char in value):
            raise PasswordValidationException("password should contain atleast 1 upper case (A-Z)")
        if not any(char.islower() for char in value):
            raise PasswordValidationException("password should contain atleast 1 lower case (a-z)")
        if not any(char.isdigit() for char in value):
            raise PasswordValidationException("password should contain atleast 1 digit  (0-9)")
        if not any(char in '!@#$%^&*()' for char in value):
            raise PasswordValidationException("password should contain atleast 1 special character  (ex: @$)")
        return value
class UserLoginSchema(BaseModel):
    email : EmailStr
    password : str

class RefreshToken(BaseModel):
    refresh_token : str