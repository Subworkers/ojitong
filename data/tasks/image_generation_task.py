from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from data.tasks.base_task import BaseTask
from data.templates.image_generation_template import ImageTemplate

class ImageGenerationTask(BaseTask***REMOVED***:
    def __init__(self***REMOVED***:
        super(***REMOVED***.__init__(***REMOVED***
        self.dalle_wrapper = DallEAPIWrapper(
            model="dall-e-3",
        ***REMOVED***

    def _build_llm(self***REMOVED***:
        return OpenAI(***REMOVED***

    def _build_template(self***REMOVED***:
        prompt = ImageTemplate(***REMOVED***.prompt
        return ChatPromptTemplate.from_template(prompt***REMOVED***
    
    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm

    def _build_parser(self***REMOVED***:
        pass

    def execute(self, content***REMOVED***:
        query = self.chain.invoke({"text": content***REMOVED******REMOVED***
        image_url = self.dalle_wrapper.run(query***REMOVED***
        return image_url
