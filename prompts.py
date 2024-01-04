import json
from descriptors import ToolDescriptor

def system_prompt(tools: list[ToolDescriptor]):
  tool_list = { 'tools': []}
  for tool in tools:
    tool_list['tools'].append(tool.description)

  json_sample_call = {
        "function_calls": [
            {
                "tool_name": "$TOOL_NAME",
                "parameters": {
                    "$PARAMETER_NAME": "$PARAMETER_VALUE"
                }
            }
        ]
    }

  return f"""In this environment you will have access to a set of tools you can use to help answer the user's question.

You can call them like this:
<tool_use>
{json.dumps(json_sample_call)}
</tool_use>

Here are the tools available:
{json.dumps(tool_list)}

Make sure to call one tool at a time. Make sure to respect the parameter type, ensuring to wrap string values in quotes, and leaving numeric values unwrapped. Feel free to use as many tools as you need. Once you're done, print the result in <answer></answer> tags.

If you can't find the right tool for your purpose, say "I'm sorry, I don't have the right tools in my toolbelt to answer that question".
"""