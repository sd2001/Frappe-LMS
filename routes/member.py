from fastapi import APIRouter, Depends, HTTPException, Response
from schemas  import py_models as pm
from typing import List
import services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()

@app.get('/members', response_model = List[pm.Members])
async def get_members(db: orm.Session=Depends(serv.get_db)):
    try:
        db_users = db.query(sql.Members).all()
        return db_users
    except Exception as e:
        return Response(content=str(e))

@app.get('/members/{id}', response_model = pm.Members)
async def get_a_member(id: int, db: orm.Session=Depends(serv.get_db)):
    try:
        db_user = db.query(sql.Members).filter(sql.Members.id == id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="This user does not exist!")
        return db_user
    except Exception as e:
        return Response(content=str(e))

@app.post('/members',status_code = 201, response_model = pm.Members, response_model_exclude_unset=True)
async def create_member(member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    try:
        db_user_exists = db.query(sql.Members).filter(sql.Members.email == member.email).first()
        if db_user_exists:
            raise HTTPException(status_code=409, detail="Email ID already exists!")
        
        new_user = sql.Members(name=member.name, email=member.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        return Response(content=str(e))

@app.put('/members/{id}', response_model = pm.Members)
async def update_member(id: int, member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    try:
        db_user = db.query(sql.Members).filter(sql.Members.id == id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="This user does not exist!")
        
        db_user.name = member.name
        db_user.email = member.email
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        return Response(content=str(e))
    
@app.delete('/members/{id}')
async def delete_member(id: int, db: orm.Session=Depends(serv.get_db)):  
    try:
        db_user = db.query(sql.Members).filter(sql.Members.id == id)
        temp_user = db_user
        if db_user is None:
            raise HTTPException(status_code=404, detail="This user does not exist!")
        db_user.delete()
        db.commit()
        return temp_user
    except Exception as e:
        return Response(content=str(e))

@app.get('/library/warnings', response_model = List[pm.Members])
async def warning_members(db: orm.Session=Depends(serv.get_db)):
    try:
        db_users = db.query(sql.Members).filter(sql.Members.warning == True).all()
        return db_users
    except Exception as e:
        return Response(content=str(e))
 
