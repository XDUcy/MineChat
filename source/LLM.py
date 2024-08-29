import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.chains import LLMChain
from langchain.llms.base import LLM

from typing import Any, List, Optional

class Yuan2B():
    """
    class for Yuan-2B LLM
    """
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path :str):
        print("Creat tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, add_eos_token=False, add_bos_token=False, eos_token="<eod>"
        )
        self.tokenizer.add_tokens(
            [
                "<sep>",
                "<pad>",
                "<mask>",
                "<predict>",
                "<FIM_SUFFIX>",
                "<FIM_PREFIX>",
                "<FIM_MIDDLE>",
                "<commit_before>",
                "<commit_msg>",
                "<commit_after>",
                "<jupyter_start>",
                "<jupyter_text>",
                "<jupyter_code>",
                "<jupyter_output>",
                "<empty_output>",
            ],
            special_tokens=True,
        )

        print("Creat model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, torch_dtype=torch.bfloat16, trust_remote_code=True
        ).cuda()

    def __call__(self, prompt: str, 
              stop: Optional[List[str]] = None,
              **kwargs: Any) -> str:
        prompt = prompt.strip()
        prompt += "<sep>"
        inputs = self.tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        outputs = self.model.generate(inputs, do_sample=False, max_length=2048)
        output = self.tokenizer.decode(outputs[0])
        response = output.split("<sep>")[-1].split("<eod>")[0]

        return response

    @property
    def _llm_type(self) -> str:
        return "Yuan2.0-2B"

if __name__ == "__main__":
    llm = Yuan2B("D:/Datasets/Pretrained Models/IEITYuan/Yuan2-2B-Mars-hf")
    response = llm(prompt="你好")
    print(response)