from typing import Callable
from functools import wraps

def tool_use(fn: Callable):
  @wraps(fn)
  def _wrapped(*a, **kw):
    return fn(*a, **kw)
  
  _wrapped.__tool_use__ = True

  return _wrapped