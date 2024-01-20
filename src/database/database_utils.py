import uuid
from ..main import session


def add(db_model):
    # Errorhandling needs to be done
    session.add(db_model)
    session.commit()
    session.refresh(db_model)


def get_all():
    # how to query SELECT *
    results = session.query().all()
    return results


def get_uuid():
    return uuid.uuid4()

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
