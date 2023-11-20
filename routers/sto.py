from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()


class Sto(BaseModel):
    adress: str
    description: str
    name: str


@router.post('/create', summary='Создание нового СТО')
async def create_new_sto(sto: Sto):
    query = f'''
            insert into sto.sto (adress, description, name)
            values ('{sto.adress}', '{sto.description}', '{sto.name}' )
            returning id
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.patch('/{sto_id}/update')
async def update_sto_info(sto_id: int, sto: Sto):
    query = f'''
            update sto.sto
            set adress = '{sto.adress}', description = '{sto.description}', name = '{sto.name}'
            where id = {sto_id}
            returnind id
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.delete ('/{sto_id}/delete')
async def delete_sto(sto_id: int):
    query = f'''
            delete from sto.sto
            where id = {sto_id}
            returning id
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.get('/all')  # Получение списка СТО
async def get_all_stos(limit: int = 100, offset: int = 0):
    query = f'''
            select id, adress 
            from sto.sto 
            limit {limit} 
            offset {offset} 
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)

@router.get("/{sto_id}/info")  # Получение информации об СТО
async def get_sto_info(sto_id: int):
    query = f'''
            select * 
            from sto.sto 
            where id = {sto_id}
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)
