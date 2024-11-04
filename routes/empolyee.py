from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi import Query
from typing import Optional
from service.auth import Auth

from database import get_db
from database.models import Employee
from database.shema import EmployeeCreate, EmployeeUpdate, DefaultResponseModel
from fastapi.responses import ORJSONResponse

router = APIRouter()


@router.post("/", response_model=EmployeeCreate)
def create_employee(employee: EmployeeCreate,
                    db: Session = Depends(get_db),
                    current_user = Depends(Auth.get_current_user)
):
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        return ORJSONResponse(
            content=DefaultResponseModel(
                message=f"email: {employee.email} already exist"
            ).model_dump(),
            status_code=403,
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        role=employee.role
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return ORJSONResponse(
        content=DefaultResponseModel(
            message=f"employee with {new_employee.email} created",
            content={
                "id": new_employee.id,
                "name": new_employee.name,
                "email": new_employee.email,
                "department": new_employee.department,
                "role": new_employee.role
            }
        ).model_dump(),
        status_code=201,
    )

@router.get("/", response_model=list[EmployeeCreate])
def list_employees(
    department: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    current_user = Depends(Auth.get_current_user)
):
    limit = 10
    offset = (page - 1) * limit

    query = db.query(Employee)
    
    if department:
        query = query.filter(Employee.department == department)
    if role:
        query = query.filter(Employee.role == role)
    
    employees = query.offset(offset).limit(limit).all()
    employee_list = [
        {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "role": employee.role,
            "date_joined": employee.date_joined
        }
        for employee in employees
    ]
    return ORJSONResponse(
        content=DefaultResponseModel(
            message=f"found {len(employee_list)} employees",
            content={"employees": employee_list}
        ).model_dump(),
        status_code=200,
    )

@router.get("/{id}/", response_model=EmployeeCreate)
def get_employee(id: str,
                 db: Session = Depends(get_db),
                 current_user = Depends(Auth.get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        return ORJSONResponse(
            content=DefaultResponseModel(
                message=f"employee with '{id}' not found",
                content={}
            ).model_dump(),
            status_code=404,
        )
    return ORJSONResponse(content=DefaultResponseModel(
        message=f"employee with '{id}' found",
        content={
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "role": employee.role,
            "date_joined": employee.date_joined
        }
        ).model_dump(),
        status_code=200,
    )

@router.put("/{id}/", response_model=EmployeeCreate)
def update_employee(id: str,
                    employee_update: EmployeeUpdate,
                    db: Session = Depends(get_db),
                    current_user = Depends(Auth.get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        return ORJSONResponse(
            content=DefaultResponseModel(
                message=f"employee with '{id}' not found",
                content={}
            ).model_dump(),
            status_code=404,
        )

    for key, value in employee_update.dict(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return ORJSONResponse(
        content=DefaultResponseModel(
            message=f"employee with '{id}' updated",
            content={
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "role": employee.role,
                "date_joined": employee.date_joined
            }
        ).model_dump(),
        status_code=200,
    )

@router.delete("/{id}/", response_model=DefaultResponseModel)
def delete_employee(id: str,
                    db: Session = Depends(get_db),
                    current_user = Depends(Auth.get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        return ORJSONResponse(
            content=DefaultResponseModel(
                message=f"employee with '{id}' not found",
                content={}
            ).model_dump(),
            status_code=404,
        )

    db.delete(employee)
    db.commit()
    return ORJSONResponse(
        content=DefaultResponseModel(
            message=f"employee with '{id}' deleted",
            content={}
        ).model_dump(),
        status_code=204,
    )
