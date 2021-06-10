from fastapi import APIRouter, Depends, HTTPException
from schemas  import py_models as pm
from typing import List
import services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()

@app.get('/members', response_model = List[pm.Members])
async def get_members(db: orm.Session=Depends(serv.get_db)):
    db_users = db.query(sql.Members).all()
    return db_users

@app.get('/members/{id}', response_model = pm.Members)
async def get_members(id: int, db: orm.Session=Depends(serv.get_db)):
    db_user = db.query(sql.Members).filter(sql.Members._id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    return db_user

@app.post('/members',status_code = 201, response_model = pm.Members)
async def create_member(member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    db_user_exists = db.query(sql.Members).filter(sql.Members.email == member.email).first()
    if db_user_exists:
        raise HTTPException(status_code=409, detail="Email ID already exists!")
    
    new_user = sql.Members(name=member.name, email=member.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put('/members/{id}', response_model = pm.Members)
async def update_members(id: int, member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    db_user = db.query(sql.Members).filter(sql.Members._id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    
    db_user.name = member.name
    db_user.email = member.email
    db.commit()
    db.refresh(db_user)
    return db_user
    
@app.delete('/members/{id}')
async def delete_members(id: int, db: orm.Session=Depends(serv.get_db)):  
    db_user = db.query(sql.Members).filter(sql.Members._id == id)
    temp_user = db_user
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    db_user.delete()
    db.commit()
    return temp_user
 
