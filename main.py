from fastapi import FastAPI
from db import postgre
from routers import sto_router, master_router, consultatin_router, portfolio_router, feedback_router, service_router, master_service_router, master_service_record_router
import uvicorn
   
app = FastAPI()

app.include_router(sto_router, prefix='/sto', tags=['sto'])
app.include_router(master_router, prefix='/sto', tags=['master'])
app.include_router(consultatin_router, prefix='/sto', tags=['consultation'])
app.include_router(portfolio_router, prefix='/sto', tags=['portfolio'])
app.include_router(feedback_router, prefix='/sto', tags=['feedback'])
app.include_router(service_router, prefix='/service', tags=['service'])
app.include_router(master_service_router, prefix='/master_service', tags=['master_service'])
app.include_router(master_service_record_router, prefix='/service', tags=['master_service_record'])

# Вызов функции при старте сервера
@app.on_event('startup')
async def startup_event():
    postgre.connect()
    postgre.init_cursor()

# Вызов функции при выключении сервера
@app.on_event('shutdown')
async def shutdown_event():
    postgre.close_cursor()
    postgre.close_connection()


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=4444)