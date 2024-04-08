from typing import Optional, Type

from sqlalchemy import Engine
from sqlalchemy.engine.create import event
from sqlalchemy.orm import Session

from src.database.database_setup import engine
from src.models.models import Base


@event.listens_for(Engine, "connect")
def enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

 # Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Type warning does not apply here
# TODO: All those methods should have error handling with try except
def add(db_model: Base, db: Session) -> None:
    # Errorhandling needs to be done
    db.add(db_model)
    db.commit()
    db.refresh(db_model)       # i dont know what this does


def delete(table: Type[Base], id: str, db: Session) -> None:
    result: Base | None = db.get(table, id)
    db.delete(result)
    db.commit()


#def get_by_id(table: Type[Base], id: str, db: Session) -> Optional[Base]:
#    """
#
#    @rtype: object
#    """
#    # how to query SELECT * WHERE id = id
#    result: Base | None = db.get(table, id)
#    return result


def get_all(table: Type[Base], db: Session) -> list[Base]:
    # how to query SELECT *
    results: list[Base] = db.query(table).all()
    return results


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
