from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl, RootModel, model_validator, field_validator

import yaml

class ChannelEnum(str, Enum):
    default = "default"
    esr = "esr"
    release = "release"
    beta = "beta"
    daily = "daily"

class OperatingSystemEnum(str, Enum):
    win = "win"
    macosx = "macosx"
    linux = "linux"
    freebsd = "freebsd"
    openbsd = "openbsd"
    netbsd = "netbsd"
    solaris = "solaris"
    other = "other"

class Profile(BaseModel):
    locales: list[str] | None = None
    versions: list[str] | None = None
    channels: list[ChannelEnum] | None = None
    operating_systems: list[OperatingSystemEnum] | None = None

class SeverityEnum(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

class TypeEnum(str, Enum):
    donation = "donation"
    message = "message"
    security = "security"
    blog = "blog"

class Targeting(BaseModel):
    percent_chance: float | None = None
    exclude: list[Profile] | None = None
    include: list[Profile] | None = None

    @field_validator('percent_chance')
    @classmethod
    def min_max_percent_chance(cls, v: float):
       if v < 0 or v > 100:
            raise ValueError("'percent_chance' must be a value from 0 to 100")


class Notification(BaseModel):
    id: UUID
    start_at: datetime
    end_at: datetime
    title: str
    description: str
    URL: HttpUrl | None = None
    CTA: str | None = None
    severity: SeverityEnum
    type: TypeEnum
    targeting: Targeting

    @model_validator(mode="after")
    def cta_requires_url(self):
        if self.CTA and not self.URL:
            raise ValueError("if 'CTA' is present, 'URL' must be present too")
        return self

class NotificationSchema(RootModel):
  root: list[Notification]

  def yaml_to_data(yaml_str):
    try:
      return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
      print(f'Error parsing YAML file: {e}')
      return None

  def from_yaml(in_fname):
    """Static function to generate NotificationSchema from a yaml file"""
    with open(in_fname, "r") as fh:
      contents = fh.read()
      data = NotificationSchema.yaml_to_data(contents)
      return NotificationSchema(data)

