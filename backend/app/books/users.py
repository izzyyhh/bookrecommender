import os
from datetime import date
from typing import List, Optional, Union

import pandas as pd
from pydantic.dataclasses import dataclass

users = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/BX-User-cleaned.csv', sep=";", converters = {"User-ID": str,"Location":str,"Age": str}, encoding="CP1252", escapechar='\\')

os.path.dirname(os.path.realpath(__file__))
@dataclass
class User:
    userId: Optional[str]
    age: int
    country: str
    favoriteAuthor: Optional[str]
    favoritePublisher: Optional[str]
    favorites: Optional[List[int]]


users = list(map(lambda x: User(x[0], int(x[1]), x[4], None, None, None), users.values.tolist()))
usershash = {}
maxuid = 0
for u in users:
    a = int(u.userId)
    if maxuid < a:
        maxuid = int(u.userId)
        
for u in users:
    usershash[u.userId] = u
