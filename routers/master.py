from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre
from typing import List


router = APIRouter()


class Master(BaseModel):
    name: str
    phones: List[str]
    experience: int = 1
    specialisation: str
    login: str
    password: str


@router.post("/{sto_id}/master/create")  # Добавление мастера в СТО
async def create_new_sto_master(sto_id: int, master: Master):
    query = f'''
                   insert into sto.master (sto_id, name, phones, experience, specialisation, login, password) 
                   values ({sto_id}, '{master.name}', '{'{"' + '", "'.join(master.phones) + '"}'}', {master.experience}, '{master.specialisation}', '{master.login}', '{master.password}')
                   returning id;
                   '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.patch("/{sto_id}/master/{master_id}/update")  # Обновление информации о мастере СТО
async def update_master_info(sto_id: int, master_id: int, master: Master):
    query = f'''
                   update sto.master
                   set name = '{master.name}', phones = '{'{"' + '", "'.join(master.phones) + '"}'}', experience = {master.experience}, specialisation = '{master.specialisation}', login = '{master.login}', password = '{master.password}'
                   where id = {master_id} and sto_id = {sto_id}
                   returning id;
                   '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.delete("/{sto_id}/master/{master_id}/delete")  # Удаление мастера
async def delete_master(sto_id: int, master_id: int):
   query = f'''
                   delete from sto.master
                   where id = {master_id} and sto_id = {sto_id}
                   returning id;
                   '''
   result = postgre.execute_query(query)
   return JSONResponse(result)

@router.get("/{sto_id}/master/all")  # Получение списка мастеров в СТО
async def get_all_masters (sto_id: int, limit: int = 100, offset: int = 0):
    query = f'''
                   select id, name, phones, experience, specialisation 
                   from sto.master 
                   where sto_id = {sto_id} 
                   limit {limit} 
                   offset {offset};
                   '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)

@router.get("/{sto_id}/master/{master_id}/info")  # Получение информации о мастере в СТО
async def get_master_info(sto_id: int, master_id: int):
    query = f'''select * 
                   from sto.master 
                   where id = {master_id} and sto_id = {sto_id}
                   '''
    result = postgre.execute_query(query, fetch_type='one', commit=False)
    return JSONResponse(result)
