from typing import List, Dict, Any, Optional

class GLM4Flash:
    def __init__(self, zhipu_token: str):
        from zhipuai import ZhipuAI
        self.client = ZhipuAI(api_key=zhipu_token)
        self.history = []
        print("Zhipu client initialized.")

    def _wrap_user_prompt(self, prompt: str) -> List[Dict[str, str]]:
        prompt = [{"role":"system", "content":""}, {"role":"user", "content":prompt}]
        self.history.extend(prompt)
        return prompt

    def _manage_history(self, response):
        completion_dict = [
            {
                "role": response.choices[0].message.role,
                "content": response.choices[0].message.content,
            }
        ]
        self.history.extend(completion_dict)
        print("History updated, current history:", self.history)

    def __call__(self, prompt):
        if isinstance(prompt, str):
            self._wrap_user_prompt(prompt)
        response = self.client.chat.completions.create(
            model="glm-4-flash",
            messages=self.history,
            stream=False,
            top_p=0.7,
            temperature=0.95,
            max_tokens=2048,
        )
        self._manage_history(response)
        return response.choices[0].message.content
    @property
    def _llm_type(self) -> str:
        return "GLM4Flash"


if __name__ == "__main__":
    # llm = Yuan2B("D:/Datasets/Pretrained Models/IEITYuan/Yuan2-2B-Mars-hf")
    llm = GLM4Flash("91ecc3cf6cf58d4b2d6c25ed7507ee5c.7cQgS9UjeIOzs4WX")
    response = llm(prompt="你好")
    print(llm.history)
