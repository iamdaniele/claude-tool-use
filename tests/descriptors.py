from descriptors import TaskDescriptor
import unittest

task_str = """<tool_use>
<invoke>
<tool_name>Cat.meow</tool_name>
<arguments>
<times>3<times>
</arguments>
</invoke>
</tool_use>"""

class TestTaskDescriptor(unittest.TestCase):
  def test_completion_hydration(self):
    descriptor = TaskDescriptor.from_completion(task_str)
    print(descriptor)
    self.assertIs(type(descriptor), TaskDescriptor)
    self.assertEqual(descriptor.tool_name, 'Cat.meow')
    self.assertEqual(descriptor.arguments['times'], '3')

if __name__ == "__main__":
  unittest.main()