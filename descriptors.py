from dataclasses import dataclass
from typing import Callable, Union
from bs4 import BeautifulSoup

def xml_to_dict(element):
  data = {}
  children = getattr(element, 'children', list())

  for child in children:
    child_data = xml_to_dict(child)
    if child.name is None:
      return child.string
    
    if child.name in data:
      if type(data[child.name]) == list:
        data[child.name].append(child_data)
      else:
        data[child.name] = [data[child.name], child_data]
    else:
      data[child.name] = child_data
  
  return data

@dataclass
class ToolDescriptor:
  description: str
  method: Callable

@dataclass
class TaskDescriptor:
  tool_name: str
  arguments: Union[dict, None]

  @classmethod
  def from_completion(cls, completion):
    completion = ''.join([line.strip() for line in completion.splitlines()])
    soup = BeautifulSoup(completion, features='xml')
    data = xml_to_dict(soup)

    if 'tool_use' in data and 'invoke' in data['tool_use']:
      return TaskDescriptor(**data['tool_use']['invoke'])