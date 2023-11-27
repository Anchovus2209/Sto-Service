from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()


class MasterService(BaseModel):
    service_id: int | None = None
    master_id: int | None = None
    price: int


@router.post('/create_rel')
async def create_master_service_rel(master_service: MasterService):
    query = f'''
            insert into sto.master_service_rel (service_id, master_id, price) 
            values ({master_service.service_id}, {master_service.master_id}, {master_service.price})
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch('/{master_service_id}/change_price')
async def update_master_service_price(master_service_id: int, master_service: MasterService):
    query = f'''
            update sto.master_service_rel
            set price = {master_service.price}
            where id = {master_service_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{master_service_id}/delete")  
async def delete_master_service(master_service_id: int):
   query = f'''
            delete from sto.master_service_rel
            where id = {master_service_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)



@router.get("/by_sto_id/{sto_id}/all")
async def get_all_sto_services(sto_id: int):
    query = f'''
            select s.*, min(msr.price) as min_price, count(m.id) as master_number
            from sto.service s
            inner join sto.master_service_rel msr
            on s.id = msr.service_id 
            inner join sto.master m 
            on m.id = msr.master_id
            where m.sto_id = {sto_id}
            group by s.id, s.name, s.description
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)
