from pydantic import BaseModel, ConfigDict


class SShortUrl(BaseModel):
    id: int
    number_of_transitions: int
    short_url: str
    qr_code: str
    is_activ: bool


class SUrl(BaseModel):
    id: int
    original_url: str
    short_urls: list["SShortUrl"]

    model_config = ConfigDict(from_attributes=True)


class SCreateShortUrl(BaseModel):
    number_of_transitions: int
    short_url: str
    qr_code: str
    is_activ: bool

    model_config = ConfigDict(from_attributes=True)


class SCreateUrlAndShortUrl(BaseModel):
    url: str
    short_url: str

    model_config = ConfigDict(from_attributes=True)

