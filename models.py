from pydantic import BaseModel,field_validator,Field,EmailStr

class RegisterUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,example="John Doe", description="Full name of the user")
    email: EmailStr = Field(...,example="johndoe@example.com", description="Unique email address")
    password: str = Field(..., min_length=8, example="Securepassword@123", description="Password with a minimum of 8 characters")
    mobile: str = Field(...,example="+1234567890", description="Valid phone number with country code")

    @field_validator("mobile")
    def validate_phone(cls, value):
            if not value.startswith("+"):
                raise ValueError("Phone number must include a country code")
            return value
    @field_validator("password")
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char in "@$!%*?&" for char in value):
            raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &)")
        return value
    
class LoginUser(BaseModel):
     email:str
     password:str