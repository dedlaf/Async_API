from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from schemas.user import User, UserInDB
from services.mongo_service import MongoCRUD, get_mongo_crud

router = APIRouter()


@router.post(
    "/",
    response_model=UserInDB,
    summary="Создание нового пользователя",
    description="Добавляет нового пользователя в базу данных",
)
async def create_user(user: User, mongo_crud: MongoCRUD = Depends(get_mongo_crud)):
    user_dict = user.dict()
    user_id = await mongo_crud.insert_document(collection_name="User", data=user_dict)
    return UserInDB(id=str(user_id), **user_dict)


@router.get(
    "/{user_id}",
    response_model=UserInDB,
    summary="Получение пользователя по идентификатору",
    description="Возвращает данные пользователя по его id",
)
async def get_user(user_id: str, mongo_crud: MongoCRUD = Depends(get_mongo_crud)):
    obj_id = ObjectId(user_id)
    found_user = await mongo_crud.find(
        collection_name="User", condition={"_id": obj_id}
    )
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    found_user["id"] = str(found_user.pop("_id"))
    return found_user


@router.put(
    "/{user_id}",
    response_model=UserInDB,
    summary="Обновление данных пользователя",
    description="Обновляет данные пользователя по его id и возвращает обновлённого пользователя",
)
async def update_user(
    user_id: str, user: User, mongo_crud: MongoCRUD = Depends(get_mongo_crud)
):
    obj_id = ObjectId(user_id)
    await mongo_crud.update_document(
        collection_name="User", condition={"_id": obj_id}, new_values=user.dict()
    )
    updated_user = await mongo_crud.find(
        collection_name="User", condition={"_id": obj_id}
    )
    updated_user["id"] = str(updated_user.pop("_id"))
    return updated_user


@router.delete(
    "/users/{user_id}",
    response_model=dict,
    summary="Удаление пользователя",
    description="Удаляет пользователя по его id",
)
async def delete_user(user_id: str, mongo_crud: MongoCRUD = Depends(get_mongo_crud)):
    obj_id = ObjectId(user_id)
    result = await mongo_crud.delete_document(
        collection_name="User", condition={"_id": obj_id}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted"}


@router.get(
    "/",
    response_model=List[UserInDB],
    summary="Получение списка пользователей",
    description="Возвращает список всех пользователей в базе данных",
)
async def get_users(mongo_crud: MongoCRUD = Depends(get_mongo_crud)):
    found_users = await mongo_crud.find(
        collection_name="User", condition={}, multiple=True
    )
    for user in found_users:
        user["id"] = str(user.pop("_id"))
    return found_users
