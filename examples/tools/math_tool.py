from tool_use import tool_use

class MathTool:
  @tool_use
  def add(self, num1: int, num2: int):
    """Adds two numbers.

    :param num1: The first number.
    :type num1: int
    :param num2: The second number.
    :type num2: int
    """
    return num1 + num2
  
  @tool_use
  def subtract(self, num1: int, num2: int):
    """Subtracts two numbers.

    :param num1: The first number.
    :type num1: int
    :param num2: The second number.
    :type num2: int
    """
    return num1 - num2