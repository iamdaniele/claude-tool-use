from descriptors import TaskDescriptor, ToolDescriptor
from examples.tools.repeat_tool import RepeatTool
import unittest
import json

task_str = """ <tool_use>
{"function_calls": [{"tool_name": "RepeatTool.repeat", "parameters": {"text": "cat", "times": 42}}]}
</tool_use>"""

expected_descriptor = {
  'tool_name': 'RepeatTool.repeat', 
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

class TestTaskDescriptor(unittest.TestCase):
  def test_completion_hydration(self):
    descriptor = TaskDescriptor.from_completion(task_str)
    self.assertIs(type(descriptor), TaskDescriptor)
    self.assertEqual(descriptor.tool_name, 'RepeatTool.repeat')
    self.assertEqual(descriptor.parameters['times'], 42)


class ToolDescriptor(unittest.TestCase):
  def test_descriptor(self):
    tool = RepeatTool()
    descriptors = tool.describe_all_for_claude()
    self.assertIn('RepeatTool.repeat', descriptors)
    descriptor = descriptors['RepeatTool.repeat'].description
    self.assertDictEqual(descriptor, expected_descriptor)

if __name__ == "__main__":
  unittest.main()