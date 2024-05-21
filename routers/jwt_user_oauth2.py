from fastapi import APIRouter,HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from pydantic import BaseModel

router = APIRouter(tags=["jwt"],
                   responses={404:{"message":"No encontrado"}})

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 1
SECRET_KEY = "322faf3f0103dea31cb4951bf5c776bc57dd5a7d1101f6f6c8c3801db5de0af1"


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

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypto = CryptContext(schemes=["bcrypt"])

# nuestra base de datos de usuarios

usersDB = {
    "pepe123" :
        {   
            "username" : "pepe123",
            "fullname" : "Pepe Gonzales",
            "email" : "eedeseth@gmail.com",
            "disable" : False,
            "password": "$2a$12$UuNPRuhUjx2s5.cb.G24mOujzt2usZs41YvR/cnewyCWwRGX5jevC"
        },
    "juan123" :
        {   
            "username" : "juan123",
            "fullname" : "Juan Gonzales",
            "email" : "gigirigi@gmail.com",
            "disable" : True,
            "password": "$2a$12$qMwkE17o5o5Kg5Fm5oXbYuvfvz1Tt4fQ4rFACMz2aZ6wPfcZi4ysu"
        }
}

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("name")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user




def search_user(username : str):
    if username in usersDB:
        return User(**usersDB[username])

# buscar usuarios en la db
def search_userdb(username : str):
    if username in usersDB:
        return UserDB(**usersDB[username])
    
    

@router.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    
    # comprobamos en nombre de usuario si esta dentro de la base de datos
    user_db = usersDB.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no valido")
    
    # comprobamos la contraseña
    user = search_userdb(form.username)
    
    if not crypto.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña no valida")
    
    access_token = {"name":form.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)  }
    
    return {"acess_token":jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM),"token_type":"bearer"}

@router.get("/user/me")
async def me(user : User = Depends(current_user)):
    return user