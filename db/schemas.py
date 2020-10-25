from pydantic import BaseModel
# from fastapi_users import models as user_models
# when updating the schema, you have to wipe the database. When creating a
# new table you can just update normally.
from datetime import datetime
from typing import List, Optional


# Paths models here
class PathBase(BaseModel):
    pass
# expect nothing from user


class Path(PathBase):
    path: str
    user: int
# we provide path and user back

    class Config:
        orm_mode = True


class PathCreate(PathBase):
    class Config:
        orm_mode = True


class Image(BaseModel):
    img: str


class ImageCreate(Image):
    pass
