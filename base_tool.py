from docstring_parser import parse, DocstringParam
from abc import ABC
from typing import Callable, final
from functools import wraps
from descriptors import ToolDescriptor

def prepare_arguments(params: list[DocstringParam]) -> str:
  out = []
  for param in params:
    out.append({
      'name': param.arg_name,
      'type': param.type_name,
      'description': param.description
    })

  return out

class BaseTool(ABC):
  @final
  def describe_for_claude(self, fn: Callable) -> str:
    parsed = parse(fn.__doc__)
    return {
      'tool_name': f'{self.__class__.__name__}.{fn.__name__}',
      'arguments': prepare_arguments(parsed.params)
    }
  
  @final
  def describe_all_for_claude(self) -> dict[ToolDescriptor]:
    tools = {}
    for obj in dir(self):
      attr = getattr(self, obj)
      if callable(attr) and getattr(attr, '__tool_use__', None) is not None:
        description = self.describe_for_claude(attr)
        tool_name = f'{self.__class__.__name__}.{attr.__name__}'
        tools[tool_name] = ToolDescriptor(tool_name=tool_name, description=description, method=attr)
    
    return tools

def tool_use(fn: Callable):
  @wraps(fn)
  def _wrapped(*a, **kw):
    return fn(*a, **kw)
  
  _wrapped.__tool_use__ = True

  return _wrapped