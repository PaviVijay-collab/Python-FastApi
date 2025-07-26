from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

import odoorpc

app = FastAPI()

HOST_NAME = '192.168.1.7'
HOST_PORT = 8069

db_name = 'Odoo_16'


class Login(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(data: Login):
    odoo = odoorpc.ODOO(HOST_NAME, port=HOST_PORT)

    user = data.username
    password = data.password

    try:
        # Login
        odoo.login(db_name, user, password)

        # Current user
        user = odoo.env.user
        print(user.name)  # name of the user connected
        print(user.company_id.name)  # the name of its company

        return user.name

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get('/')
def hello_world():
    return 'Hello World'
