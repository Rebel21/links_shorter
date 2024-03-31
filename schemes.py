from pydantic import BaseModel, ConfigDict


class SToken(BaseModel):
    id: int
    number_of_transitions: int
    original_url: str
    short_url: str
    qr_code: str
    is_activ: bool

    model_config = ConfigDict(from_attributes=True)


class SUrl(BaseModel):
    url: str


class SShortUrl(BaseModel):
    short_url: str
