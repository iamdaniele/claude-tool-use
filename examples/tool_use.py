from runner import Runner

from .tools.repeat_tool import RepeatTool
from .tools.math_tool import MathTool

tools = [RepeatTool(), MathTool()]
runner = Runner(tools)

answer = runner.request('can you repeat this string for me 42 times: cat')
print(answer)