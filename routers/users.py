from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

# iniciar servidor local: uvicorn users:app --reload

### Basemodel para definir la estrutura de nuesto usuario ###
class User(BaseModel):
    id : int
    user : str
    rol : str
    level : int
    email : str
    
players_list = [User(id=1,user="Fernan2232",rol="Wizzard",level=23,email="fffardo@gmail"),
                User(id=2,user="Ale23xd",rol="Knight",level=15,email="aelale@gmail"),
                User(id=3,user="crackPro",rol="Zombie",level=33,email="tumadre@gmail")]

### Funcion que devuelve una lista de json 

@router.get("/userjsn")
async def userjsn():
    return [{"user":"Fernan2232","rol":"Wizzard","level":23,"email":"fffardo@gmail"},
            {"user":"Ale23xd","rol":"Knight","level":15,"email":"aelale@gmail"},
            {"user":"crackPro","rol":"Zombie","level":33,"email":"tumadre@gmail"}]

@router.get("/users")
async def users():
    return players_list

### Parametro de Path ( es descir parametros por la ruta )

@router.get("/user/{id}")
async def user( id : int ):
    if type(buscar(id)) == dict:
        raise HTTPException(status_code=404, detail="el usuario no existe")
    return buscar(id)
    
### Parametro de Query ( pasamos los parametros por peticion http, con la sintaxix "user/?id=1", si queremos agregar otro parametro seria "user/?id=1&name=nombre")

@router.get("/userquery/")
async def user( id : int ):
    return buscar(id)

### Operacion Post ( para crear datos ) ###

@router.post("/user/",response_model=User,status_code=201)  # response_model es para indicar cual va hacer la respuesta si todo va bien
async def new_user(user : User):                         # status_code es para indicar el HTTP que se va mostrar si todo va bien
    if type(buscar(user.id)) == User :
        raise HTTPException(status_code=404, detail="el usuario ya existe")  # en vez de usar return usamos raise que es para invocar
    else:
        players_list.append(user)
        return user


### Operacion Put ( para actualizar datos ) ###

@router.put("/user/",response_model=User)
async def update_user(user : User):
    
    found = False
    
    for index,saved_user in enumerate(players_list):
        if saved_user.id == user.id:
            players_list[index] = user
            found = True
    
    if not found:
        raise HTTPException(status_code=404, detail="el usuario no existe")
    
    return user

### Operacion Delete ( para borrar datos ) ###

@router.delete("/user/{id}")
async def userdelete(id : int):
    
    found = False
    
    for index,saved_user in enumerate(players_list):
        if saved_user.id == id:
            del(players_list[index])
            found = True
    
    if not found:
        raise HTTPException(status_code=404, detail="el usuario no existe")
    
    return {"message":"El usuario a sido borrado del servidor"}


def buscar(id : int):
    user = filter(lambda user: user.id == id, players_list)
    try:
        return list(user)[0]
    except :
        return {"error":"El usuario no existe"}