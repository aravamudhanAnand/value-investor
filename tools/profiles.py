"""Business profiles for every company: what it is, how it makes money, how the stock is valued (analyst judgment).
build.py adds the calculated multiples, the sector comparison and the fair value."""
from profiles_a import P as A
from profiles_b import P as B
from profiles_c import P as C
from profiles_d import P as D
from profiles_e import P as E
from profiles_f import P as F
from profiles_g import P as G

PROFILE = {**A, **B, **C, **D, **E, **F, **G}
