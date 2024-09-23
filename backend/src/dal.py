from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from pydantic import BaseModel

from uuid import uuid4

class ListSummary(BaseModel):
    id: str
    name: str
    item_count: int

    @staticmethod
    def from_db(data: dict) -> 'ListSummary':
        return ListSummary(
            id=str(data['_id']),
            name=data['name'],
            item_count=data['item_count']
        )
    
class ToDoListItem(BaseModel):
    id: str
    label: str
    checked: bool

    @staticmethod
    def from_db(data: dict) -> 'ToDoListItem':
        return ToDoListItem(
            id=str(data['_id']),
            label=data['label'],
            checked=data['checked']
        )

class ToDoList(BaseModel):
    id: str
    name: str
    items: list[ToDoListItem]

    @staticmethod
    def from_db(data: dict) -> 'ToDoList':
        return ToDoList(
            id=str(data["_id"]),
            name=data["name"],
            items=[ToDoListItem.from_db(item) for item in data['items']]
        )
    

class ToDoListDal:
    def __init__(self, todo_collection: AsyncIOMotorCollection):
        self._todo_collection = todo_collection

    async def list_todo_lists(self, session = None):
        async for doc in self._todo_collection.find(
            {},
            projection={
                "name": 1,
                'item_count': {"$size": "$items"},
                },
            sort={"name": 1},
            session=session
        ):
            yield ListSummary.from_db(doc)

    async def create_todo_list(self, name: str, session = None) -> str:
        result = await self._todo_collection.insert_one(
            {"name": name, "items": []},
            session=session
        )
        return str(result.inserted_id)
    
    async def get_todo_list(self, list_id: str | ObjectId, session = None) -> ToDoList:
        doc = await self._todo_collection.find_one(
            {"_id": ObjectId(list_id)},
            session=session
        )
        return ToDoList.from_db(doc)
    
    async def delete_todo_list(self, list_id: str | ObjectId, session = None) -> None:
        response = await self._todo_collection.delete_one(
            {"_id": ObjectId(list_id)},
            session=session
        )
        return response.deleted_count == 1
    
    async def create_item(
            self,
            id: str | ObjectId,
            label: str,
            session = None
    ) -> ToDoList | None:
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$push": {
                "items": {
                    "_id": uuid4().hex,
                    "label": label,
                    "checked": False
                    }
                }
            },
            return_document=ReturnDocument.AFTER,
            session=session
        )
        if result:
            return ToDoList.from_db(result)
        
    async def set_checked_state(
            self,
            list_id: str | ObjectId,
            item_id: str,
            checked: bool,
            session = None
    ) -> ToDoList | None:
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(list_id), "items._id": item_id},
            {"$set": {
                "items.$.checked": checked
                }
            },
            return_document=ReturnDocument.AFTER,
            session=session
        )
        if result:
            return ToDoList.from_db(result)


    async def delete_item(
            self,
            list_id: str | ObjectId,
            item_id: str,
            session = None
    ) -> ToDoList | None:
        result = await self._todo_collection.find_one_and_update(
            {"_id": ObjectId(list_id)},
            {"$pull": {
                "items": {
                    "_id": item_id
                    }
                }
            },
            return_document=ReturnDocument.AFTER,
            session=session
        )
        if result:
            return ToDoList.from_db(result)