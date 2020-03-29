from typing import TYPE_CHECKING
from typing_extensions import Literal

from pydantic import BaseModel

L1 = Literal["1"]

class AModel(BaseModel):
    an_att: L1

m = AModel(an_att="1")
if TYPE_CHECKING:
    m_errors_mypy = AModel(an_att="nope")


L2 = Literal["2"]

L12 = Literal[L1, L2]

_1: L12 = "1"
_2: L12 = "2"

errors_mypy: L12 = "nope"

class AnotherModel(BaseModel):
    an_att: Literal[L1, L2]

another_m = AnotherModel(an_att="1")
another_m = AnotherModel(an_att="nope")

"""
$ mypy literals_bug_example.py
literals_bug_example.py:13: error: Argument "an_att" to "AModel" has incompatible type "Literal['nope']"; expected "Literal['1']"
literals_bug_example.py:23: error: Incompatible types in assignment (expression has type "Literal['nope']", variable has type "Union[Literal['1'], Literal['2']]")
literals_bug_example.py:29: error: Argument "an_att" to "AnotherModel" has incompatible type "Literal['nope']"; expected "Union[Literal['1'], Literal['2']]"


$ python literals_bug_example.py 
Traceback (most recent call last):
  File "literals_bug_example.py", line 28, in <module>
    another_m = AnotherModel(an_att="1")
  File "/Users/dbcerigo/miniconda3/envs/helios/lib/python3.7/site-packages/pydantic/main.py", line 274, in __init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 1 validation error for AnotherModel
an_att
  unexpected value; permitted: typing_extensions.Literal['1'], typing_extensions.Literal['2'] (type=value_error.const; given=1; permitted=(typing_extensions.Literal['1'], typing_extensions.Literal['2']))
"""
