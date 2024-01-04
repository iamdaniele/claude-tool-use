from runner import Runner
from tool_use import tool_use
import datetime

from .tools.repeat_tool import RepeatTool
from .tools.math_tool import MathTool

@tool_use
def current_time() -> str:
  """Returns the current UTC time."""
  return datetime.datetime.now(datetime.UTC).isoformat()

tools = [RepeatTool(), MathTool(), current_time]
runner = Runner(tools)

# prompt = 'please repeat the word "cat" a number of times equivalent to this equation: x = 3 + 2'
prompt = 'what time is it in Oakland, California?'
print('You:', prompt)
answer = runner.request(prompt)
print('Claude:', answer)