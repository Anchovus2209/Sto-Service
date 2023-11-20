from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from db import postgre


router = APIRouter()


class Portfolio(BaseModel):
   photo: str
   description: str


@router.post("/{sto_id}/master/{master_id}/portfolio/create")
async def create_new_master_portfolio(master_id: int, portfolio: Portfolio):
    query = f'''
            insert into sto.portfolio (master_id, photo, description) 
            values ({master_id}, '{portfolio.photo}', '{portfolio.description}')
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.patch("/{sto_id}/master/{master_id}/portfolio/{portfolio_id}/update")  
async def update_master_portfolio_info(sto_id: int, master_id: int, portfolio_id: int, portfolio: Portfolio):
    query = f'''
            update sto.portfolio
            set photo = '{portfolio.photo}', desccription = '{portfolio.description}'
            where id = {portfolio_id} and master_id = {master_id}
            returning id;
            '''
    result = postgre.execute_query(query)
    return JSONResponse(result)


@router.delete("/{sto_id}/master/{master_id}/portfolio/{portfolio_id}/delete")  
async def delete_master_portfolio(sto_id: int, master_id: int, portfolio_id: int):
   query = f'''
            delete from sto.portfolio
            where id = {portfolio_id} and master_id = {master_id}
            returning id;
            '''
   result = postgre.execute_query(query)
   return JSONResponse(result)


@router.get("/{sto_id}/portfolio/all")
async def get_all_sto_portfolio(sto_id: int):
    query = f'''
            select * 
            from sto.portfolio
            where master_id in (select id from sto.master where sto_id = {sto_id});
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)


@router.get("/{sto_id}/master/{master_id}/portfolio/all")
async def get_all_master_portfolio(sto_id: int, master_id: int):
    query = f'''
            select *
            from sto.portfolio
            where master_id = {master_id};
            '''
    result = postgre.execute_query(query, fetch_type='all', commit=False)
    return JSONResponse(result)
