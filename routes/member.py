from fastapi import APIRouter, Depends, HTTPException, Response
from schemas  import py_models as pm
from typing import List
import app_services.services as serv
import sqlalchemy.orm as orm
from models import sql_models as sql

app = APIRouter()

@app.get('/members', response_model = List[pm.Members])
async def get_members(db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches all the existing Library Members in form of a list.
    This includes sensitive details like the Member ID, Expenditure, Debt and Warnings.
    For the Librarian!
    '''
    try:
        db_users = db.query(sql.Members).all()
        return db_users
    except Exception as e:
        return Response(content=str(e))

@app.get('/members/{id}', response_model = pm.Members)
async def get_a_member(id: int, db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches an existing Library Member.
    This includes sensitive details like the Member ID, Expenditure, Debt and Warnings.
    For the Librarian!
    '''
    
    db_user = db.query(sql.Members).filter(sql.Members.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    return db_user
    

@app.post('/members',status_code = 201, response_model = pm.Members, response_model_exclude_unset=True)
async def create_member(member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    '''
    This route creates a new Library Members.
    Only the Name and the Email ID can be added here, rest parameters are default.
    It checks whether the entered email ID exists or not and then creates a new Member.
    For the Librarian!
    '''
    db_user_exists = db.query(sql.Members).filter(sql.Members.email == member.email).first()
    if db_user_exists:
        raise HTTPException(status_code=409, detail="Email ID already exists!")
    
    new_user = sql.Members(name=member.name, email=member.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@app.put('/members/{id}', response_model = pm.Members)
async def update_member(id: int, member: pm.Members, db: orm.Session=Depends(serv.get_db)):
    '''
    This route changes details of an existing Library Members.
    Only the Name and the Email ID can be changed here.
    It checks whether the entered user ID exists or not and then changes as per Request.
    For the Librarian!
    '''
    
    db_user = db.query(sql.Members).filter(sql.Members.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    
    db_user.name = member.name
    db_user.email = member.email
    db.commit()
    db.refresh(db_user)
    return db_user
    
    
@app.delete('/members/{id}')
async def delete_member(id: int, db: orm.Session=Depends(serv.get_db)): 
    '''
    This route deletes an existing Library Members.
    It checks whether the entered user ID exists or not and then deletes as per Request.
    For the Librarian!
    ''' 
    
    db_user = db.query(sql.Members).filter(sql.Members.id == id).first()
    temp_user = db_user
    if db_user is None:
        raise HTTPException(status_code=404, detail="This user does not exist!")
    db_user.delete()
    db.commit()
    return Response(content=f"User with ID: {id} has been deleted")

@app.get('/library/warnings', response_model = List[pm.Members])
async def warning_members(db: orm.Session=Depends(serv.get_db)):
    '''
    This route fetches the members who's debt has exceeded 500 i.e warning is set to True and returns them
    For the Librarian!
    '''    
    db_users = db.query(sql.Members).filter(sql.Members.warning == True).all()
    return db_users
    
 
