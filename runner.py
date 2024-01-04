from descriptors import TaskDescriptor
from prompts import system_prompt
from anthropic import Anthropic, AI_PROMPT, HUMAN_PROMPT
import dotenv
import json
from typing import Any, Callable, Union
from helpers import describe_all_for_claude, describe_for_claude, is_tool_use
dotenv.load_dotenv()

class Runner:
  def __init__(self, tools: list[Union[Callable, object]], model: str = 'claude-2.1', max_tokens_to_sample: int = 1024):
    self.tools = {}
    for tool in tools:
      if is_tool_use(tool):
        self.tools.update(describe_for_claude(tool))
      else:
        self.tools.update(describe_all_for_claude(tool))

    self.model = model
    self.max_tokens_to_sample = max_tokens_to_sample
    self.start_tag = '<tool_use>'
    self.stop_tag = '</tool_use>'
    self.answer_start_tag = '<answer>'
    self.answer_stop_tag = '</answer>'
    self.client = Anthropic()

  def request(self, prompt: str):
    prompt = f"{system_prompt(self.tools.values())}{HUMAN_PROMPT} {prompt} {AI_PROMPT}"

    while True:   
      completion = self.client.completions.create(
        prompt=prompt,
        model=self.model,
        stop_sequences=[HUMAN_PROMPT, self.stop_tag],
        max_tokens_to_sample=self.max_tokens_to_sample)

      # Claude is invoking a tool
      if completion.stop_reason == 'stop_sequence' and completion.stop == self.stop_tag:
        # parse tool
        # find <tool_use>
        tool_idx = completion.completion.find(self.start_tag)
        if tool_idx < 0:
          raise Exception(f"Found {self.stop_tag} without {self.start_tag}")
        
        request = TaskDescriptor.from_completion(completion.completion[tool_idx:] + self.stop_tag)
        
        # invoke tool
        if request.tool_name not in self.tools:
          raise Exception(f"Claude attempted to invoke a non-existing tool: '{request.tool_name}'")
        
        # get result and format
        result = self.tools[request.tool_name].method(**request.parameters)
        formatted_result = self._format_result_for_claude(request.tool_name, result)

        # feed into the prompt
        prompt += f"{completion.completion} {self.stop_tag} {formatted_result}"
      else:
        # just return the response
        start_idx = completion.completion.find(self.answer_start_tag) + len(self.answer_start_tag)
        stop_idx = completion.completion.find(self.answer_stop_tag)
        return completion.completion[start_idx:stop_idx].strip()
  
  def _format_result_for_claude(self, tool_name: str, result: Any) -> str:
    json_result = { 'result': {
      'tool_name': tool_name,
      'result': result
    }}
    return f"""<tool_results>{json.dumps(json_result)}</tool_results>"""
