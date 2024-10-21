from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from data.tasks.base_task import BaseTask
from data.templates.image_generation_template import ImageTemplate

class ImageGenerationTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.dalle_wrapper = DallEAPIWrapper(
            model="dall-e-3",
        )

    def _build_llm(self):
        return OpenAI()

    def _build_template(self):
        prompt = ImageTemplate().prompt
        return ChatPromptTemplate.from_template(prompt)
    
    def _build_chain(self):
        return self.prompt_template | self.llm

    def _build_parser(self):
        pass

    def execute(self, content):
        query = self.chain.invoke({"text": content})
        image_url = self.dalle_wrapper.run(query)
        return image_url
