from tool_use import tool_use

class RepeatTool:
  @tool_use
  def repeat(self, text: str, times: int) -> str:
    """Repeats a string exactly the specified number of times.

    :param text: the text to repeat
    :type text: str
    :param times: how many times the text should be repeated.
    :type times: int
    """
    return str(text) * int(times)