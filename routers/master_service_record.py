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
    car_id: int
    date: date
    description: str
    
    
@router.post('/{service_id}/record/create')
async def create_master_service_record(master_id: int, service_id: int, master_service_record: MasterServiceRecord):

    # 1. Создать запись автомобиля с маркой, моделью и годом выпуска, если такого еще нет
    # 2. Получить идентификатор (id) авто
    # 3. Создать запись на услугу к мастеру с конкретным авто

    query = f'''
            insert into sto.master_service_record (master_id, service_id, name, phones, email, car_id, date, description) 
            values ({master_id}, {service_id}, '{master_service_record.name}', '{'{"' + '", "'.join(master_service_record.phones) + '"}'}', '{master_service_record.name}', '{master_service_record.email}', {master_service_record.car_id}, '{master_service_record.date}', '{master_service_record.description}',)
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)