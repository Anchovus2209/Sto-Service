from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre
from typing import List


router = APIRouter()


class Consultation(BaseModel):
    name:str
    phones: List[str]
    description: str
    complete: bool = False
   

@router.post("/{sto_id}/consultation/create")
async def create_new_sto_consultation(sto_id: int, consultation: Consultation):
    query = f'''
            insert into sto.consultation (sto_id, name, phones, description, complete)
            values ({sto_id}, '{consultation.name}', '{'{"' + '", "'.join(consultation.phones) + '"}'}', '{consultation.description}', {consultation.complete})
            returning id
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.patch("/{sto_id}/consultation/{consultation_id}/update")
async def update_sto_consultation_info(sto_id: int, consultation_id: int, consultation: Consultation):
    query = f'''
            update sto.consultation
            set name = '{consultation.name}', phones = '{'{"' + '", "'.join(consultation.phones) + '"}'}', description = {consultation.description}
            where id = {consultation_id} and sto_id = {sto_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.patch("/{sto_id}/consultation/{consultation_id}/complete")
async def complete_sto_consultation(sto_id: int, consultation_id: int):
    query = f'''
            update sto.consultation
            set complete = true
            where id = {consultation_id} and sto_id = {sto_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.delete("/{sto_id}/consultation/{consultation_id}/delete")  
async def delete_consultation(sto_id: int, consultation_id: int):
   query = f'''
            delete from sto.consultation
            where id = {consultation_id} and sto_id = {sto_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)

@router.get("/{sto_id}/consultation/all")  
async def get_all_masters (sto_id: int, limit: int = 100, offset: int = 0):
    query = f'''
            select id, name, phones, description, complete 
            from sto.consultation
            where sto_id = {sto_id} 
            limit {limit} 
            offset {offset};
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)

@router.get("/{sto_id}/consultation/{consultation_id}/info") 
async def get_master_info(sto_id: int, consultation_id: int):
    query = f'''
            select * 
            from sto.consultation
            where id = {consultation_id} and sto_id = {sto_id}
            '''
    result = postgre.execute_query(query, commit=False)
    return JSONResponse(result)
    