from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()


class Service(BaseModel):
    name: str
    price: int
    description: str


@router.post("/{sto_id}/master/{master_id}/service/create")
async def create_new_master_service(master_id: int, service: Service):
    query = f'''
            insert into sto.service (master_id, name, price, description) 
            values ({master_id}, '{service.name}', {service.price}, '{service.description}')
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch("/{sto_id}/master/{master_id}/service/{service_id}/update")  
async def update_master_service_info(sto_id: int, master_id: int, service_id: int, service: Service):
    query = f'''
            update sto.service
            set name = '{service.name}', price = {service.price}, desccription = '{service.description}'
            where id = {service_id} and master_id = {master_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{sto_id}/master/{master_id}/service/{service_id}/delete")  
async def delete_master_service(sto_id: int, master_id: int, service_id: int):
   query = f'''
            delete from sto.service
            where id = {service_id} and master_id = {master_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get("/{sto_id}/service/all")
async def get_all_sto_service(sto_id: int):
    query = f'''
            select * 
            from sto.service
            where master_id in (select id from sto.master where sto_id = {sto_id});
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)


@router.get("/{sto_id}/master/{master_id}/service/all")
async def get_all_master_service(sto_id: int, master_id: int):
    query = f'''
           select * 
           from sto.service
           where master_id in (select master_id from sto.master_service_rel where master_id = {master_id});
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)

@router.get("/{sto_id}/service/{service_id}/master/all")
async def get_service_all_master(sto_id: int, service_id: int):
    query = f'''
           select * 
           from sto.master
           where master_id in (select service_id from sto.master_service_rel where service_id = {service_id});
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)



