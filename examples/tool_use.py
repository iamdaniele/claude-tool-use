from runner import Runner

from .tools.repeat_tool import RepeatTool
from .tools.math_tool import MathTool

tools = [RepeatTool(), MathTool()]
runner = Runner(tools)

answer = runner.request('please repeat the word "cat" a number of times equivalent to this equation: x = 3 + 2')
print(answer)