from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse

app = FastAPI()

# Demo ke liye tables create karta hai.
Base.metadata.create_all(bind=engine)


# CREATE
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(Employee).filter(
        Employee.email == data.email
    ).first()

    if existing:
        raise HTTPException(409, "Email already exists")

    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


# READ ALL
@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# READ ONE
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(404, "Employee not found")

    return employee


# UPDATE
@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(404, "Employee not found")

    changes = data.model_dump(exclude_unset=True)

    if changes.get("email") is not None:
        duplicate = db.query(Employee).filter(
            Employee.email == changes["email"],
            Employee.id != employee_id
        ).first()

        if duplicate:
            raise HTTPException(409, "Email already exists")

    for key, value in changes.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


# DELETE
@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(404, "Employee not found")

    db.delete(employee)
    db.commit()
    return None