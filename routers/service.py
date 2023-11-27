from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()


class Service(BaseModel):
    name: str
    description: str


@router.post("/create")
async def create_new_service(service: Service):
    query = f'''
            insert into sto.service (name, description) 
            values ('{service.name}', '{service.description}')
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch("/{service_id}/update")  
async def update_service_info(service_id: int, service: Service):
    query = f'''
            update sto.service
            set name = '{service.name}', description = '{service.description}'
            where id = {service_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{service_id}/delete")  
async def delete_service(service_id: int):
   query = f'''
            delete from sto.service
            where id = {service_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get("/all")
async def get_all_services(limit: int = 100, offset: int = 0):
    query = f'''
            select * 
            from sto.service
            limit {limit}
            offset {offset};
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)
