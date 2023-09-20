from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


class User(BaseModel):
    id: int
    name: str
    password: str


class RegisterUser(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str


users_list = [User(id=1, name="camilo", password="123"),
              User(id=2, name="andres", password="456"),
              User(id=3, name="polania", password="789")]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


app = FastAPI()


@app.post("/register")
async def register(user: RegisterUser):
    # Guardar el usuario en la lista de usuarios
    users_list.append(User(id=len(users_list) + 1,
                      name=user.name, password=user.password))

    return {"message": "Usuario registrado exitosamente"}


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # verificar el usuario
    user = filter(lambda user: user.name == form.username, users_list)
    try:
        user = list(user)[0]
        if user.password != form.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña es incorrecta"
            )

        # Generar un token de acceso
        token = {"access_token": user.name}

        return token

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe"
        )


@app.get("/users", dependencies=[Depends(oauth2_scheme)])
async def Users():
    # Convertir todos los usuarios a objetos UserResponse
    users_response = []
    for user in users_list:
        users_response.append(UserResponse(id=user.id, name=user.name))

    return users_response


@app.get("/users/{id}", dependencies=[Depends(oauth2_scheme)])
async def Users(id: int):
    # buscar usuarios por id
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error no se ha encontrado el usuario"}
