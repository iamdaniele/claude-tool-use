from descriptors import TaskDescriptor, ToolDescriptor
from examples.tools.repeat_tool import RepeatTool
import unittest
from datetime import datetime, timezone
from helpers import describe_all_for_claude, describe_for_claude
from uuid import UUID

task_str = """ <tool_use>
{"function_calls": [{"tool_name": "RepeatTool.repeat", "parameters": {"text": "cat", "times": 42}}]}
</tool_use>"""

expected_descriptor = {
  'tool_name': 'RepeatTool.repeat', 
  'description': 'Repeats a string exactly the specified number of times.',
  'arguments': [
    {
      'name': 'text', 
      'type': 'str', 
      'description': 'the text to repeat'
    }, 
    {
      'name': 'times', 
      'type': 'int', 
      'description': 'how many times the text should be repeated.'
    }
  ]
}

def is_uuid(value: str) -> bool:
  try:
    id = UUID(value, version=4)
  except:
    return False
  
  return str(id) == value

def current_time() -> str:
  """Returns the current UTC time"""
  return str(datetime.now(timezone.utc))

class TestTaskDescriptor(unittest.TestCase):
  def test_completion_hydration(self):
    descriptor = TaskDescriptor.from_completion(task_str)
    self.assertIs(type(descriptor), TaskDescriptor)
    self.assertEqual(descriptor.tool_name, 'RepeatTool.repeat')
    self.assertEqual(descriptor.parameters['times'], 42)


class TestToolDescriptor(unittest.TestCase):
  def test_descriptor(self):
    tool = RepeatTool()
    descriptors = describe_all_for_claude(tool)
    descriptor = None
    for k in descriptors:
      if is_uuid(k):
        expected_descriptor['tool_name'] = k
        descriptor = descriptors[k]
        break

    self.assertDictEqual(descriptor.description, expected_descriptor)
  
  def test_descriptor_no_args(self):
    desc = describe_for_claude(current_time)
    descriptor = ToolDescriptor(tool_name=desc['tool_name'], description=desc, method=current_time)
    self.assertEqual(len(descriptor.description['arguments']), 0)
    

if __name__ == "__main__":
  unittest.main()