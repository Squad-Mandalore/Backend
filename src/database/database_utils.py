from typing import Optional, Type
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.database.database_setup import SessionLocal
from src.models.models import Base

 # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type warning does not apply here
def add(db: Session, db_model: Base) -> None:
    # Errorhandling needs to be done
    db.add(db_model)
    db.commit()
    db.refresh(db_model)       # i dont know what this does


def delete(db: Session, table: Type[Base], id: str) -> Optional[HTTPException]:
    result = db.query(table).filter(table.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="User not found")
    db.delete(result)
    db.commit()


def get_by_id(db: Session, table: Type[Base], id: str) -> Base | HTTPException:
    # how to query SELECT * WHERE id = id
    result = db.query(table).filter(table.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="User not found")

    return result


def get_all(db: Session, table: Type[Base]) -> list[Base] | HTTPException:
    # how to query SELECT *
    results = db.query(table).all()
    if not results:
        return HTTPException(status_code=404, detail="No users found")

    return results


def get_uuid() -> str:
    return str(uuid.uuid4())

# # how to filter
# r1 = db.query(Person).filter(Person.age == 19)
# # !!! Attention r1 is a list, therefore you have to iterate through it
# for r in r1:
#     print(r)

# # how to do crazy stuff
# r2 = db.query(Person).filter(Person.firstname.in_(["Ronny", "Lucas"]))
# for r in r2:
#     print(r)

# # how to query over multiple tables
# r3 = db.query(Person, Thing).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Ole")
# for r in r3:
#     print(r)
