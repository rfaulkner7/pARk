from db.schemas import Path
from db.db import get_db
from db import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .controllers import create_a_path
from .utils import convert
from PIL import Image
from .utils import convert
import numpy as np
import asyncio
import shutil
import base64
from fastapi import FastAPI, File, UploadFile

router = APIRouter()


# @router.put('', response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), user: User = Depends(fastapi_users.get_current_user)):
#     if not user.is_owner:
#         raise HTTPException(403, detail="The user is not an owner")
#     if get_store_details(db, item.store_id).owner != str(user.id):
#         raise HTTPException(403, detail="The user is not an owner of the selected store")
#     db_item = create_menu_item(db, item.store_id, item.name, item.description, item.price)
#     return db_item


@router.put('/genPath', response_model=schemas.Path)
def create_path(uInput: schemas.PathCreate, db: Session = Depends(get_db)):

    # uInput.user - returns user id from the user input provided
    # got rid of uInput.user - reads user input body item named user
    img = Image.open("newParking.png")
    size = img.size
    img2 = img.resize(((int)(size[0]/100), (int)(size[1]/100)))
    array = np.array(img2)
    db_item = create_a_path(db, convert(array))
    return db_item


@router.post('/image')
def imageGetter(image: schemas.Image):
    data = (image.img)
    imgData = base64.b64decode(data)
    filename = "newParking.png"
    with open(filename, 'wb') as f:
        f.write(imgData)
    # with open("destination.png", "wb") as buffer:
    #     shutil.copyfileobj(image.file, buffer)
    return {}
