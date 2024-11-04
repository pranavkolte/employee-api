# employee-api

Setup DB
docker run --name employee_db -p 127.0.0.1:5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -d postgres
docker exec -it employee_db createdb --username=root --owner=root employee
docker exec -it employee_db createdb --username=root --owner=root users

Migarte DB
alembic revision --autogenerate -m "message"
alembic upgrade head

INSTALL REQUIREMENTS
pip install -r requirements.txt

RUN Server
uvicorn app:app --reload

Run test case
pytest tests/test_employee.py