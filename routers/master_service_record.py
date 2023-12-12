from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre
from typing import List
from datetime import date


router = APIRouter()
 
 
class MasterServiceRecord(BaseModel):
    name: str
    phones: List[str]
    email: str
    date: date
    description: str
   

@router.post('/{service_id}/record/create')
async def create_master_service_record(master_id: int, service_id: int, car_id:int, master_service_record: MasterServiceRecord):

    # 1. Создать запись автомобиля с маркой, моделью и годом выпуска, если такого еще нет
    # 2. Получить идентификатор (id) авто
    # 3. Создать запись на услугу к мастеру с конкретным авто

    query = f'''
            insert into sto.master_service_record (master_id, service_id, name, phones, email, car_id, date, description) 
            values ({master_id}, {service_id}, '{master_service_record.name}', '{'{"' + '", "'.join(master_service_record.phones) + '"}'}', '{master_service_record.email}', {car_id}, '{master_service_record.date}', '{master_service_record.description}')
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch('/{master_service_record_id}/update')
async def update_master_service_record(master_service_record_id: int, master_service_record: MasterServiceRecord):
    query = f'''
            update sto.master_service_recjrd
            set name = '{master_service_record.name}', phones = '{'{"' + '", "'.join(master_service_record.phones) + '"}'}', email = '{master_service_record.email}', car_id = {master_service_record.car_id}, date = '{master_service_record.date}', description = '{master_service_record.description}'
            where id = {master_service_record_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{master_service_record_id}/delete")  
async def delete_master_service_record(master_service_record_id: int):
   query = f'''
            delete from sto.master_service_record
            where id = {master_service_record_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get("/by_name/all")
async def get_all_master_service_records_by_name(master_service_record: MasterServiceRecord):
    query = f'''
            select * 
            from master_service_record
            where name = '{master_service_record.name}' and car_id = {master_service_record.car_id}
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)


@router.get("/all")
async def get_all_master_service_records(master_service_record: MasterServiceRecord):
    query = f'''
            select * 
            from master_service_record
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)