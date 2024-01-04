from docstring_parser import parse, DocstringParam
from abc import ABC
from typing import Callable
from descriptors import ToolDescriptor
from uuid import uuid4

def prepare_arguments(params: list[DocstringParam]) -> str:
  out = []
  for param in params:
    out.append({
      'name': param.arg_name,
      'type': param.type_name,
      'description': param.description
    })

  return out

def describe_for_claude(fn: Callable) -> str:
  parsed = parse(fn.__doc__)
  return {
    'tool_name': str(uuid4()),
    'description': f"{parsed.short_description} {parsed.long_description if parsed.long_description is not None else ''}".strip(),
    'arguments': prepare_arguments(parsed.params)
  }

def is_tool_use(fn: Callable):
  return callable(fn) and getattr(fn, '__tool_use__', None) is not None


def describe_all_for_claude(instance: object) -> dict[ToolDescriptor]:
  tools = {}
  for obj in dir(instance):
    attr = getattr(instance, obj)
    if is_tool_use(attr):
      description = describe_for_claude(attr)
      tool_name = description['tool_name']
      tools[tool_name] = ToolDescriptor(tool_name=tool_name, description=description, method=attr)
  
  return tools