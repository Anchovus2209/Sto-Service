from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre
from datetime import date


router = APIRouter()


class Car(BaseModel):
 brand: str
 model: str
 year: int   
 
 
 router.post('/create')
async def create_new_car_record(car: Car): 
    query = f''' 
            insert into sto.car (brand, model, year)
            select '{car.brand}', '{car.model}', {car.year}
            where not exists (
            select 1
            from sto.car
            where brand = '{car.brand}', '{car.model}', {car.year})
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

@router.patch('/{car_id}/update')
async def update_car_record_info(car_id: int, car: Car):
    query = f'''
            update sto.car
            set brand = '{car.brand}', model = '{car.model}', year = {car.year}
            where id = {car_id}
            returnind id
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)

    
@router.delete("/{car_id}/delete")  
async def delete_car_record(car_id: int):
   query = f'''
            delete from sto.car
            where id = {car_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get('/all')  
async def get_all_car_records(limit: int = 100, offset: int = 0):
    query = f'''
            select *
            from sto.car 
            limit {limit} 
            offset {offset} 
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)


@router.get("/{car_id}/info")  
async def get_car_record_info(car_id: int):
    query = f'''
            select * 
            from sto.car
            where id = {car_id}
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)