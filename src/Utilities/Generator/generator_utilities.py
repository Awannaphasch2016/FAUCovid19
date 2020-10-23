import itertools
from typing import Any
from typing import Iterable
from typing import Tuple
from typing import Union


def peek(iterable) -> Union[None, Tuple[Any, Iterable]]:
    """Return None if generator is empty.

    usesage is shwon below
    ...code
      res = peek(mysequence)
      if res is None:
          # sequence is empty.  Do stuff.
      else:
          first, mysequence = res
          # Do something with first, maybe?
          # Then iterate over the sequence:
          for element in mysequence:
              # etc.
    """

    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)
