from typing import Optional, Dict
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home() -> Dict:
    return {"message": "Hello world"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#validaciones: query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length = 1,
        max_length = 50,
        title = "Person name",
        description = "This is the name of the person"
    ),
    age: str = Query(
        ...,
        title = "Age of the person",
        description = "The age of the person"
    )
):

    return {name: age}


#validaciones: path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0
    )
):
    return {person_id: "Its exits!"}


#Validations: Body parameters, request body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "person ID",
        description = "This is the person ID",
        gt = 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

