from pydantic import BaseModel, Field, validator


class InUserSchema(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    image: str = Field(None)
    tenant_id: int = Field(...)

    @validator("username")
    def username_must_contain_only_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    # @validator('password')
    # def hash_password(cls, v):
    #     return generate_password_hash(v).decode('utf8')


# class InUserUpdateSchema(InUserSchema):
#     is_deleted: bool = Field(False)


class OutUserSchema(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    image: str = Field(None)

    class Config:
        from_attributes = True


class OutUsersSchema(OutUserSchema):
    id: str = Field(...)

    class Config:
        from_attributes = True
