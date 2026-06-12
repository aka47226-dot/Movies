from pydantic import BaseModel


class MovieData(BaseModel):
    name: str
    imageUrl: str
    price: int
    description: str
    location: str
    published: bool
    genreId: int