from descriptors import ToolDescriptor
from examples.tools.repeat_tool import RepeatTool
from prompts import system_prompt
import unittest

prompt_description = '{"tools": [{"tool_name": "RepeatTool.repeat", "arguments": [{"name": "text", "type": "str", "description": "the text to repeat"}, {"name": "times", "type": "int", "description": "how many times the text should be repeated."}]}]}'

class PromptDescriptor(unittest.TestCase):
  def test_completion_hydration(self):
    tool = RepeatTool()
    desc = tool.describe_all_for_claude()
    prompt = system_prompt([desc['RepeatTool.repeat']])
    self.assertNotEqual(prompt.find(prompt_description), -1)

if __name__ == "__main__":
  unittest.main()