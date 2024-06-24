from pydantic import BaseModel, ConfigDict, Field


class ShortUrlSchema(BaseModel):
    id: int
    number_of_transitions: int
    short_url: str
    qr_code: str
    three_words: str
    is_activ: bool


class UrlSchema(BaseModel):
    id: int
    original_url: str
    short_urls: list["ShortUrlSchema"]

    model_config = ConfigDict(from_attributes=True)


class CreateShortUrlSchema(BaseModel):
    number_of_transitions: int
    short_url: str = Field(min_length=1, max_length=8)
    qr_code: str
    three_words: str
    is_activ: bool

    model_config = ConfigDict(from_attributes=True)


class CreateUrlAndShortUrlSchema(BaseModel):
    url: str
    short_url: str = Field(min_length=1, max_length=8)

    model_config = ConfigDict(from_attributes=True)


class DisableShortUrlSchema(BaseModel):
    short_url: str

    model_config = ConfigDict(from_attributes=True)


class AddShortUrlSchema(BaseModel):
    url_id: int
    short_url: str = Field(min_length=1, max_length=8)

    model_config = ConfigDict(from_attributes=True)
