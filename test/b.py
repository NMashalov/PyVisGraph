import uuid
import collections

from pydantic import BaseModel

class Cat(BaseModel):
    blue: int
    white : int
    @property
    def blind(self):
        return self.blue + self.white

print(Cat(blue=10,white=1).blind)

d = collections.defaultdict(lambda: 0)

d[1]+=1

print(d)