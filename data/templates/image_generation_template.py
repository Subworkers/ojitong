from data.templates.base_template import BaseTemplate

class ImageTemplate(BaseTemplate***REMOVED***:
    @property
    def prompt(self***REMOVED***:
        if not hasattr(self, '_prompt'***REMOVED***:
            self._prompt = """
                Create an image that looks like a cartoon based on the text you read.
                The image should not contain any numbers, letters, text, symbols, or characters. 
                All scenarios depicted occurred in South Korea. 
                The image should not depict any scenarios where humans are harmed, threatened, or have their bodies altered in any way. 
                Additionally, the image should not be grotesque or depict anything hateful or offensive: {text***REMOVED***
            """
        return self.clean_whitespace(self._prompt***REMOVED***
