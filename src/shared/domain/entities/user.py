from pydantic import BaseModel


class User(BaseModel):
  id: int
  name: str
  age: int
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.strnameeet,
      "age": self.age,
    }
  
  def from_dict(self, data: dict) -> 'User':
    return User(
      id=data.get("id"),
      name=data.get("name"),
      age=data.get("age"),
    )