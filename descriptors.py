from dataclasses import dataclass
from typing import Callable, Union
from bs4 import BeautifulSoup
import json

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
  tool_name: str
  description: str
  method: Callable

@dataclass
class TaskDescriptor:
  tool_name: str
  parameters: Union[dict, None]

  @classmethod
  def from_completion(cls, completion):
    completion = ''.join([line.strip() for line in completion.splitlines()])
    data = BeautifulSoup(completion, features='xml')

    if getattr(data, 'tool_use', None) is None:
      raise ValueError('No <tool_use></tool_use> tag found')
    
    payload = json.loads(data.tool_use.string)

    return TaskDescriptor(**payload['function_calls'][0])