def system_prompt(tools: str):
  return f"""In this environment you will have access to a set of tools you can use to help answer the user's question.

You can call them like this:
<tool_use>
<invoke>
<tool_name>
$TOOL_NAME
</tool_name>
<arguments>
<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>
...
</arguments>
</invoke>
</tool_use>

Here are the tools available:
<tools>
{tools}
</tools>

Make sure to call one tool at a time. Once you're done, respond with your answer in <answer></answer> tags.
"""