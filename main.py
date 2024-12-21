from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {}


@app.post('/post')
def post(post: Timestamp | None = None):
    if post is None:
        return post_db[-1]
    post_db.append(post)
    return post_db[-1]


@app.get('/dog')
def get_dogs():
    return [dogs_db[dog] for dog in dogs_db]


@app.get('/dog/{kind}')
def get_dogs_by_kind(kind: str):
    return [dogs_db[dog] for dog in dogs_db if dogs_db[dog].kind == kind]


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    if dogs_db.get(pk) is None:
        return HTTPException(status_code=400, detail='Not found')
    return [dogs_db[dog] for dog in dogs_db if dogs_db[dog].pk == pk]


@app.patch('/dog/{pk}')
def patch_dog_by_pk(pk: int, dog: Dog):
    if dogs_db.get(pk) is None:
        return HTTPException(status_code=400, detail='Not found')
    dog.pk = pk
    dogs_db[pk] = dog
    return dogs_db[pk]


@app.post('/dog')
def create_dog(dog: Dog):
    idx = len(dogs_db)
    dog.pk = idx
    dogs_db[idx] = dog
    return dog
