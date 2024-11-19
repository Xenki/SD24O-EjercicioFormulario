from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os   #PAra acceder a la ruta del home
import uuid #generar un nombre aleatorio unico

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    domicilio:str    


@app.post("/formularios")
async def guarda_formulario(nombre:str=Form(...),direccion:str=Form(...),vip:str=Form(None),foto:UploadFile=File(...)):
    print("Nombre: ",nombre)
    print("Dirección: ",direccion)
    home_usuario = os.path.expanduser("~") #home usuario
    nombre_archivo = uuid.uuid4() #nombre en formato hexadecimal
    extesion_foto = os.path.splitext(foto.filename)[1]
    if vip:
        ruta_imagen= f'{home_usuario}/fotos_vip/{nombre_archivo}{extesion_foto}'
    else:
        ruta_imagen= f'{home_usuario}/fotos_ejemplo/{nombre_archivo}{extesion_foto}'
    print("Guardando la foto del formulario en: ", ruta_imagen)
    with open(ruta_imagen,"wb") as imagen:
        contenido = await foto.read()
        imagen.write(contenido)
    respuesta = {
        "Nombre" : nombre,
        "Dirección: " : direccion,
        "VIP: " : vip,
        "Ruta de la foto": ruta_imagen
    }

    return respuesta

