import yaml
import json
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, RootModel, model_validator

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
    displayed_notifications: Optional[list[str]] = Field(default=None, description="An id of an event previously displayed by the client.")
    locales: Optional[list[str]] = Field(default=None, description="The selected UI language of the client.")
    versions: Optional[list[str]] = Field(default=None, description="A client application version string.")
    channels: Optional[list[ChannelEnum]] = Field(default=None, description="The client release channel name.")
    operating_systems: Optional[list[OperatingSystemEnum]] = Field(default=None, description="The operating system the client is running under.")

class SeverityEnum(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

class TypeEnum(str, Enum):
    donation = "donation"
    donation_old = "donation_old"
    message = "message"
    security = "security"
    blog = "blog"

class Targeting(BaseModel):
    percent_chance: Optional[float] = Field(None, ge=0, le=100)
    exclude: Optional[list[Profile]] = Field(default=None)
    include: Optional[list[Profile]] = Field(default=None)

class Notification(BaseModel):
    id: UUID = Field(..., description="Unique ID set by the server")
    start_at: datetime = Field(..., description="UTC Timestamp after which Thunderbird will show the event after startup")
    end_at: datetime = Field(..., description="UTC Timestamp after which Thunderbird will never show the event, even if it has never been shown to the user.")
    title: str = Field(..., description="Short sentence describing the event which will be displayed in the Thunderbird UI.")
    description: str = Field(..., description="A short paragraph that can contain HTML and will be displayed in the Thunderbird UI.")
    URL: Optional[HttpUrl] = Field(default=None, description="URL to open from the CTA, if any.")
    CTA: Optional[str] = Field(default=None, description="Link text to show for the URL.")
    severity: SeverityEnum = Field(..., description="Severity level, where 1 is the most important/urgent and 5 is the least.")
    type: TypeEnum = Field(..., description="Category of notification.")
    targeting: Targeting = Field(..., description="Targeting criteria for the notification")

    @model_validator(mode="after")
    def cta_requires_url(self):
        if self.CTA and not self.URL:
            raise ValueError("if 'CTA' is present, 'URL' must be present too")
        return self

class NotificationModel(RootModel):
  root: list[Notification]

  @staticmethod
  def yaml_to_data(yaml_str):
    """Static method to load YAML from a string and return the corresponding python object"""
    try:
      return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
      print(f'Error parsing YAML file: {e}')
      return None

  @staticmethod
  def from_yaml(file_name):
    """Static method to generate NotificationSchema from a yaml file"""
    with open(file_name, "r") as fh:
      contents = fh.read()
      data = NotificationModel.yaml_to_data(contents)
      return NotificationModel(data)

  @staticmethod
  def generate_json_schema(schema_file_name):
      """Static method to write a JSON schema file based on pydantic model"""
      schema = NotificationModel.model_json_schema()
      with open(schema_file_name, "w") as f:
            f.write(json.dumps(schema, indent=2))
