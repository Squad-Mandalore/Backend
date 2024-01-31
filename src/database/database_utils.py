from typing import Optional, Type
import uuid
from src.database.database_setup import DBModel, session


# warning does not apply here
def add(db_model: DBModel) -> None:
    # Errorhandling needs to be done
    session.add(db_model)
    session.commit()
    session.refresh(db_model)       # i dont know what this does

def delete(db_model: DBModel) -> None:
    session.delete(db_model)
    session.commit()

def get_by_id(table: Type[DBModel], id: str) -> Optional[DBModel]:
    # how to query SELECT * WHERE id = id
    result = session.query(table).filter(table.id == id).first()
    return result

def get_all(table: Type[DBModel]) -> Optional[list[DBModel]]:
    # how to query SELECT *
    results = session.query(table).all()
    return results


def get_uuid() -> str:
    return str(uuid.uuid4())

# # how to filter
# r1 = session.query(Person).filter(Person.age == 19)
# # !!! Attention r1 is a list, therefore you have to iterate through it
# for r in r1:
#     print(r)

# # how to do crazy stuff
# r2 = session.query(Person).filter(Person.firstname.in_(["Ronny", "Lucas"]))
# for r in r2:
#     print(r)

# # how to query over multiple tables
# r3 = session.query(Person, Thing).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Ole")
# for r in r3:
#     print(r)
