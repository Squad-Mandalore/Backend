from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, CHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker




# with sqlalchemy you are able to store python objects in a database, therefore you first need to create some python classes

# Base class to inherit from
Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    #attributes
    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender}, {self.age})"


class Thing(Base):
    __tablename__ = "things"
    tid = Column("tid", Integer, primary_key=True)
    name = Column("name", String)
    owner = Column(Integer, ForeignKey("people.ssn"))

    def __init__(self, tid, name, owner):
        self.tid = tid
        self.name = name
        self.owner = owner

    def __repr__(self):
        return f"({self.tid}) {self.name} is owned by ({self.owner})"


#basic db setup and creating tables
engine = create_engine("sqlite:///example.db", echo=True)

#for in memory db do so:
#engine = create_engine("sqlite:///:memory:")

Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()





#how to add something
p1 = Person(12345, "Moritz", "Bosch", "m", 19)
p2 = Person(12346, "Markus", "Siegert", "m", 20)
p3 = Person(12347, "Lucas", "Buchholz", "m", 21)
p4 = Person(12348, "Ronny", "Seinvater", "m", 25)
p5 = Person(12349, "Ole", "Seinvater", "m", 19)

session.add(p1)
session.add(p2)
session.add(p3)
session.add(p4)
session.add(p5)
session.commit()

t1 = Thing(1, "Lambo", 12349)
t2 = Thing(2, "Schlambo", p3.ssn)
t3 = Thing(3, "Rambo", 12347)
lot = [t1, t2, t3]
session.add_all(lot)
session.commit()


#how to query
# SELECT *
results = session.query(Person).all()
print(results)

#how to filter
r1 = session.query(Person).filter(Person.age == 19)
# !!! Attention r1 is a list, therefore you have to iterate through it
for r in r1:
    print(r)

#how to do crazy stuff
r2 = session.query(Person).filter(Person.firstname.in_(["Ronny", "Lucas"]))
for r in r2:
    print(r)

#how to query over multiple tables
r3 = session.query(Person, Thing).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Ole")
for r in r3:
    print(r)