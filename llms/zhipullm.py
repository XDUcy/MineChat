from agents.extensions.models.litellm_model import LitellmModel
from .litellms import LiteLLMsBase
from dotenv import load_dotenv
import asyncio
import os

class ZhipuLLM(LiteLLMsBase):
    """
    Litellm 初始化智谱AI大模型的示例类。
    """
    SUPPORTED_MODELS = ["glm-4.5-flash"]  # 支持的模型列表
    BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
    API_KEY = "ZHIPU_API_KEY"


    def __init__(self, model_name, api_key = None, **kwargs):
        if api_key is None:
            api_key = os.getenv(self.API_KEY)
        if not api_key:
            raise ValueError("API key for ZhipuAI is required. Please set it via parameter or environment variable")

        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model_name}. Supported models are: {self.SUPPORTED_MODELS}")
        
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        self.base_url = self.BASE_URL
        self.provider_model = f"openai/{model_name}"
        self._load_model()

    def _load_model(self):
        self.client = LitellmModel(model=self.provider_model,
                                   base_url=self.base_url,
                                   api_key=self.api_key)
        return self.client
    
    async def generate(self, prompt, **kwargs):
        pass
        



if __name__ == "__main__":
    from agents import Agent, Runner, set_tracing_disabled
    load_dotenv()  # 从 .env 文件加载环境变量
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    zhipu_llm = ZhipuLLM(model_name="glm-4.5-flash", api_key=zhipu_api_key)
    agent = Agent(name="TestAgent", model=zhipu_llm.client, instructions="你是一个Minecraft游戏智能助手，提供最符合用户需求的简短明确的建议。")
    async def test_agent():
        response = await Runner.run(agent, "我每次一死东西就掉完了。。有什么指令吗。。")
        print("Agent response:", response.final_output)
    asyncio.run(test_agent())