from fastapi import APIRouter,HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


router = APIRouter(tags=["basic_oauth2"],
                   responses={404: {"message":"No encontrado"}})

# usamos dos clases distintas, una donde son los datos generales del user y otra donde guardaremos la contraseña, por seguridad
# para que quede aparte

class User(BaseModel):
    username : str
    fullname : str
    email : str
    disable : bool
    
class UserDB(User):
    password : str


# aqui guardaremos el token una vez autenticados 

oauth2 = OAuth2PasswordBearer(tokenUrl="loginn")


# nuestra base de datos de usuarios

usersDB = {
    "pepe123" :
        {   
            "username" : "pepe123",
            "fullname" : "Pepe Gonzales",
            "email" : "eedeseth@gmail.com",
            "disable" : False,
            "password": "1111"
        },
    "juan123" :
        {   
            "username" : "juan123",
            "fullname" : "Juan Gonzales",
            "email" : "gigirigi@gmail.com",
            "disable" : True,
            "password": "2222"
        }
}



# buscar usuarios
def search_user(username : str):
    if username in usersDB:
        return User(**usersDB[username])

# buscar usuarios en la db
def search_userdb(username : str):
    if username in usersDB:
        return UserDB(**usersDB[username])

# criterio de autenticacion, es decir, si ingresamos nuestro token bien y asi, esta sera la autorizacion
# va a depender de nuestra instancia de oauth2
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion no validas",
                            headers={"WWW-Authenticate":"Bearer"})
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario no activo")
    return user


# Login con post, ya que vamos a mandar datos

@router.post("/loginn")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    
    # comprobamos en nombre de usuario si esta dentro de la base de datos
    user_db = usersDB.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no valido")
    
    # comprobamos la contraseña
    user = search_userdb(form.username)
    if not user.password == form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña no valida")
    
    return {"acess_token":user.username,"token_type":"bearer"}
    


# Vamos a pedir nuestros datos

@router.get("/user/mee")
async def me(user : User = Depends(current_user)):
    return user
