from fastapi import APIRouter,HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema,users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["user_db"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"} })

# iniciar servidor local: uvicorn users:app --reload


    
### Operacion Get ( para ver datos ) ###


@router.get("/",response_model= list[User])
async def users():
    return users_schema(db_client.users.find())



@router.get("/{id}")
async def user( id : str ):
    return buscar("_id",ObjectId(id))
    

@router.get("/q/")
async def user( id : str ):
    return buscar("_id",ObjectId(id))


### Operacion Post ( para crear datos ) ###

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)  
async def new_user(user : User):                        
    if type(buscar("email",user.email)) == User :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario ya existe")  

    
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    
    return User(**new_user)


### Operacion Put ( para actualizar datos ) ###

@router.put("/",response_model=User)
async def update_user(user : User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario no existe")
    
    return buscar("_id", ObjectId(user.id))

### Operacion Delete ( para borrar datos ) ###

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def userdelete(id : str):
    
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario no existe")
    
    return {"message":"El usuario a sido borrado del servidor"}


def buscar(field : str, key ):
    try:
        user = db_client.users.find_one({field:key})
        return User (**user_schema(user))
    except :
        return {"error":"El usuario no existe"}

