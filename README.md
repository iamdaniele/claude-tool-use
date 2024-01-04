# claude-tool-use

This Python module facilitates seamless function calling within Anthropic's Claude environment. It enables users to annotate their functions with specific documentation, allowing Claude to interpret and execute these functions based on user prompts.

## Why it's cool

- You don't need to figure out the right prompt. Just bring your own documentation and you're good to go!
- You only need a decorator on functions you want to expose to Claude. That's the only change you need if your functions/methods already return a JSON-serializable value.

## Getting Started

### Usage
To start using `claude-tool-use`, follow these simple steps:

1. **Define Functions:** Define any function (standalone or instance method) to be used within Claude. Decorate the function with `@tool_use` and annotate it with proper documentation.

    ```python
    from claude_tool_use.tool_use import tool_use

    @tool_use
    def repeat(self, text: str, times: int) -> str:
      """Repeats a string exactly the specified number of times.

      :param text: the text to repeat
      :type text: str
      :param times: how many times the text should be repeated.
      :type times: int
      """
      return str(text) * int(times)
    ```

    It also works with instance methods:

    ```python
    from claude_tool_use.tool_use import tool_use

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
    ```

2. **Utilize the `Runner`:** Instantiate the `Runner` class, passing the annotated functions as a list. Use the `request` method to trigger function execution based on user prompts.

    ```python
    from claude_tool_use.runner import Runner

    # Create instances of annotated functions
    tools = [repeat, MathTool()]

    # Initialize Runner with the annotated functions
    runner = Runner(tools)

    # Send a prompt to Claude for function execution
    answer = runner.request('please repeat the word "cat" a number of times equivalent to this equation: x = 3 + 2')
    print(answer)
    ```

    Behind the scenes, `Runner` will pass the prompt (along with the function calling descriptions) to Claude. Claude will first solve the equation by calling `MathTool.add(3, 2)`, which will return `5`. Runner will then feed the result into the prompt, and feed it back to Claude. Claude will then decide to call `repeat("cat", 5)`.

    This code will then output:

    ```
    catcatcatcatcat
    ```

Feel free to experiment with different functions and prompts to leverage the capabilities of `claude-tool-use`.

## Roadmap (in no particular priority)
- [ ] Function retries
- [ ] Logging
- [ ] Benchmarking and performance improvements
- [ ] Configurable client parameters
- [ ] Switch to Claude's Messages API

## Contributing
If you find bugs, have feature requests, or would like to contribute to the development of `claude-tool-use`, please feel free to open issues or pull requests.

Enjoy using `claude-tool-use` and simplify function calling within Claude!
