from .tools.repeat_tool import RepeatTool

obj = RepeatTool()
print(obj.describe_for_claude(obj.repeat))

class test_r:
  def __init__(self):
    self.tools = {}

  def add_tools(self, obj):
    for x in dir(obj):
      method = getattr(obj, x, None)
      if callable(method):
        tool_name = f'{obj.__class__.__name__}.{method.__name__}'
        self.tools[tool_name] = method
  
  def run(self, name, **args):
    return self.tools[name](**args)
  

class runnable_test:
  hi = "hello world"
  def hello(self):
    return self.hi

class cat:
  def meow(self, times: int):
    return 'meow ' * times
  

r = test_r()
r.add_tools(runnable_test())
r.add_tools(cat())

print(r.run('cat.meow', times=2))
print(r.run('runnable_test.hello'))