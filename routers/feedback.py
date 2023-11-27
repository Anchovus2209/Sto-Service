from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()

class Feedback(BaseModel):
    description: str
    name: str
    photo: str
    rating: int


@router.post("/{sto_id}/master/{master_id}/feedback/create")
async def create_new_master_feedback(master_id: int, feedback: Feedback):
    query = f'''
            insert into sto.feedback (master_id, description, name, photo, rating) 
            values ({master_id}, '{feedback.description}', '{feedback.name}', '{feedback.photo}', {feedback.rating})
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch("/{sto_id}/master/{master_id}/feedback/{feedback_id}/update")  
async def update_master_feedback_info(sto_id: int, master_id: int, feedback_id: int, feedback: Feedback):
    query = f'''
            update sto.feedback
            set description = '{feedback.description}',name = '{feedback.name}', photo = '{feedback.photo}', rating = {feedback.rating}
            where id = {feedback_id} and master_id = {master_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{sto_id}/master/{master_id}/feedback/{feedback_id}/delete")  
async def delete_master_feedback(sto_id: int, master_id: int, feedback_id: int):
   query = f'''
            delete from sto.feedback
            where id = {feedback_id} and master_id = {master_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get("/{sto_id}/feedback/all")
async def get_all_sto_feedback(sto_id: int):
    query = f'''
            select * 
            from sto.feedback
            where master_id in (select id from sto.master where sto_id = {sto_id});
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)


@router.get("/{sto_id}/master/{master_id}/feedback/all")
async def get_all_master_feedback(sto_id: int, master_id: int):
    query = f'''
            select *
            from sto.feedback
            where master_id = {master_id};
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)



