from fastapi import FastAPI
import pyodbc

app = FastAPI()

# Define the database connection
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\WALTON\Desktop\PR\complex\Property2_1.mdb;'
    r'PWD=AnsonSTMake811;'
)

connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

# Create a Pydantic model for an employee
from pydantic import BaseModel

class Employee(BaseModel):
    EmployeeName: str
    Code: str
    Job: str

# Define an API endpoint to retrieve employee data
@app.get('/employees', response_model=list[Employee])
async def get_employees():
    # Query the database to retrieve employee data
    cursor.execute('SELECT EmployeeName, Code, Job FROM Employee')
    rows = cursor.fetchall()

    # Create a list of Employee objects from the database rows
    employees = [Employee(EmployeeName=row.EmployeeName, Code=row.Code, Job=row.Job) for row in rows]

    return employees

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
