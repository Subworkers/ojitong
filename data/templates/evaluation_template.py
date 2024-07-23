from data.templates.base_template import BaseTemplate
from langchain_core.prompts import ChatPromptTemplate

class QGQATemplate(BaseTemplate***REMOVED***:
    @property
    def prompt(self***REMOVED***:
        if not hasattr(self, '_prompt'***REMOVED***:
            self._prompt = {
                "qg": self._generate_questions_prompt(***REMOVED***,
                "qa_reference": self._answer_questions_from_news_prompt(***REMOVED***,
                "qa_hypothesis": self._answer_questions_from_blog_prompt(***REMOVED***
            ***REMOVED***
            self._prompt = {key: self.clean_whitespace_prompt_set(value***REMOVED*** for key, value in self._prompt.items(***REMOVED******REMOVED***
        return self._prompt

    def clean_whitespace_prompt_set(self, prompt_set***REMOVED***:
        roles, messages = zip(*prompt_set***REMOVED***
        cleaned_messages = map(self.clean_whitespace, messages***REMOVED***
        return list(zip(roles, cleaned_messages***REMOVED******REMOVED***

    def _generate_questions_prompt(self***REMOVED***:
        # prompt_set: (role, message***REMOVED***
        return [
            ("system", "You are an AI trained to generate insightful questions from a given article."***REMOVED***,
            ("user", """
                1. Read the article about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                8. Create 2 questions to identify the main points of the news (date of the incident, subway line of the incident***REMOVED***. The questions should be 5-way multiple choice questions where you have to choose one of the choices from 1 to 5. One of the options must be “Unknown” and the selection for the “Date of Event” question must be in the format 2018년 3월 18일. Hint is provided with every questions
                
                Example Question: 'Where did the subway incident occur? (1***REMOVED*** Gangnam Station (2***REMOVED*** Seongsu Station (3***REMOVED*** Suyu Station (4***REMOVED*** Ankguk Station (5***REMOVED*** Unknown.',
                Example Hint: ''
                News Article: {input***REMOVED***
                """
            ***REMOVED***,
            (
                "system", """
                Generate 2 questions. All responses should be in Korean ONLY. Use the template provided for formatting.
                
                Template:
                Question1: {{***REMOVED******REMOVED***,
                Hint1: {{***REMOVED******REMOVED***,
                Question2: {{***REMOVED******REMOVED***,
                Hint2: {{***REMOVED******REMOVED***
                """
            ***REMOVED***
        ***REMOVED***

    def _answer_questions_from_news_prompt(self***REMOVED***:
        return [
            ("system", "You read a news article and answer a question accurately based on what you read."***REMOVED***, # 페르소나 부여
            ("user", """
                You read a news article like this:
                1. Read the article about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                Then you answer a question accurately based on what you read.
                
                Example: '1번, 5번, 4번'
                News Article: {input***REMOVED***
                Questions: {question***REMOVED***
            """***REMOVED***,
            ("system", "Template(MUST FOLLOW***REMOVED***: Answer1: {{answer_1***REMOVED******REMOVED***번, Answer2: {{answer_2***REMOVED******REMOVED***번"***REMOVED***
        ***REMOVED***

    def _answer_questions_from_blog_prompt(self***REMOVED***:
        return [
            ("system", "You read a blog article and answer a question accurately based on what you read."***REMOVED***, # 페르소나 부여
            ("user", """
                You read a blog article like this:
                1. Read the blog about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                Then you answer a question accurately based on what you read.
            
                Example: '1번, 5번, 4번'
                Blog Article: {input***REMOVED***
                Questions: {question***REMOVED***
            """***REMOVED***,
            ("system", """"Template(MUST FOLLOW***REMOVED***: Answer1: {{answer_1***REMOVED******REMOVED***번, Answer2: {{answer_2***REMOVED******REMOVED***번"""***REMOVED***
        ***REMOVED***


class GEvalEvaluationTemplate(BaseTemplate***REMOVED***:
    @property
    def prompt(self***REMOVED***:
        if not hasattr(self, '_prompt'***REMOVED***:
            self._prompt = {
                "Consistency": self._consistency_prompt(***REMOVED***,
                "Human_Likeness": self._human_likeness_prompt(***REMOVED***,
                "Coherence": self._coherence_prompt(***REMOVED***,
                "Blog": self._blog_prompt(***REMOVED***,
                "Fluency": self._fluency_prompt(***REMOVED***,
            ***REMOVED***
            self._prompt = {key: self.clean_whitespace(value***REMOVED*** for key, value in self._prompt.items(***REMOVED******REMOVED***
        return self._prompt

    def _consistency_prompt(self***REMOVED***:
        """
        Compare and evaluate the blog content you created with the article.
        First, Extract the key information from the article. (time,date,subway line***REMOVED***
        You need to decide whether the key information is entailed by the CONTEXT by choosing one of the following rating:
        1. 5 point: The blog content follows logically from the information contained in the article.
        2. 1 point: The blog content is logically false from the information contained in the article.
        3. an integer score between 1 and 5 and if such integer score does not exist,
        use 1: It is not possible to determine whether the blog content is true or false without further information.
        Read the passage of information thoroughly and select the correct answer from the three answer labels.
        Read the CONTEXT thoroughly to ensure you know what the CONTEXT entails.
        Note the blog content is generated by a computer system, it can contain certain symbols, which should not be a negative factor in the evaluation. Scores(SCORE ONLY***REMOVED***:{{***REMOVED******REMOVED***
        Reason:{{***REMOVED******REMOVED***
        """

    def _human_likeness_prompt(self***REMOVED***:
        """
        Evaluating the human-likeness of a blog post involves a few key steps to ensure that the writing is coherent, engaging, and natural. Here's a step-by-step guide to evaluating this dimension:
        
        Step 1: Read the Entire Post
        Read the entire blog post from start to finish to get an overall sense of its flow, coherence, and readability. This first read-through will help you understand the main points and the structure of the writing.
        
        Step 2: Sentence Flow
        Check if each sentence flows naturally into the next. Look for transitions between sentences and paragraphs that are smooth and logical. Ensure there are no abrupt changes in topic or tone that can disrupt the reader’s experience.
        
        Step 3: Tone and Style
        Assess the tone and style of the writing. It should be consistent throughout the post and appropriate for the intended audience. The style should not be overly robotic or mechanical; instead, it should reflect a human touch with a personal or conversational tone where appropriate.
        
        Step 4: Engagement and Personality
        Consider the engagement and personality of the writing. A human-like blog post often includes anecdotes, rhetorical questions, humor, or opinions that make the writing more relatable and engaging. Look for elements that add personality and a human touch.
        
        Step 5: Consistency and Natural Language
        Ensure that the language used is consistent with how a human would naturally speak or write. Avoid awkward phrasing, overly technical jargon (unless appropriate for the audience***REMOVED***, and repetitive language. The post should sound like it was written by someone knowledgeable and passionate about the topic.
        
        Step 6: Score the Post
        Based on the observations from the steps above, score the blog post on a scale of 1 to 5:
        - 1: The writing is highly unnatural, robotic, and difficult to read.
        - 2: The writing has significant unnatural elements and lacks flow.
        - 3: The writing is somewhat natural but has noticeable issues with flow, tone, or engagement.
        - 4: The writing is mostly natural with minor issues that do not significantly detract from the reading experience.
        - 5: The writing is highly natural, engaging, and indistinguishable from high-quality human-written content.
        Scores (SCORE ONLY***REMOVED***: {{***REMOVED******REMOVED***
        Reason : {{***REMOVED******REMOVED***
        """

    def _coherence_prompt(self***REMOVED***:
        """
        Evaluating the human-likeness of a blog post involves a few key steps to ensure that the writing is coherent, engaging, and natural. Here's a step-by-step guide to evaluating this dimension:
        
        Step 1: Read the Entire Post
        Read the entire blog post from start to finish to get an overall sense of its flow, coherence, and readability. This first read-through will help you understand the main points and the structure of the writing.
        
        Step 2: Sentence Flow
        Check if each sentence flows naturally into the next. Look for transitions between sentences and paragraphs that are smooth and logical. Ensure there are no abrupt changes in topic or tone that can disrupt the reader’s experience.
        
        Step 3: Tone and Style
        Assess the tone and style of the writing. It should be consistent throughout the post and appropriate for the intended audience. The style should not be overly robotic or mechanical; instead, it should reflect a human touch with a personal or conversational tone where appropriate.
        
        Step 4: Engagement and Personality
        Consider the engagement and personality of the writing. A human-like blog post often includes anecdotes, rhetorical questions, humor, or opinions that make the writing more relatable and engaging. Look for elements that add personality and a human touch.
        
        Step 5: Consistency and Natural Language
        Ensure that the language used is consistent with how a human would naturally speak or write. Avoid awkward phrasing, overly technical jargon (unless appropriate for the audience***REMOVED***, and repetitive language. The post should sound like it was written by someone knowledgeable and passionate about the topic.
        
        Step 6: Score the Post
        Based on the observations from the steps above, score the blog post on a scale of 1 to 5:
        - 1: The writing is highly unnatural, robotic, and difficult to read.
        - 2: The writing has significant unnatural elements and lacks flow.
        - 3: The writing is somewhat natural but has noticeable issues with flow, tone, or engagement.
        - 4: The writing is mostly natural with minor issues that do not significantly detract from the reading experience.
        - 5: The writing is highly natural, engaging, and indistinguishable from high-quality human-written content.
        
        Scores (SCORE ONLY***REMOVED***: {{***REMOVED******REMOVED***
        Reason : {{***REMOVED******REMOVED***
        """

    def _blog_prompt(self***REMOVED***:
        """
        Evaluating the human-likeness of a blog post involves a few key steps to ensure that the writing is coherent, engaging, and natural. Here's a step-by-step guide to evaluating this dimension:
        
        Step 1: Read the Entire Post
        Read the entire blog post from start to finish to get an overall sense of its flow, coherence, and readability. This first read-through will help you understand the main points and the structure of the writing.
        
        Step 2: Sentence Flow
        Check if each sentence flows naturally into the next. Look for transitions between sentences and paragraphs that are smooth and logical. Ensure there are no abrupt changes in topic or tone that can disrupt the reader’s experience.
        
        Step 3: Tone and Style
        Assess the tone and style of the writing. It should be consistent throughout the post and appropriate for the intended audience. The style should not be overly robotic or mechanical; instead, it should reflect a human touch with a personal or conversational tone where appropriate.
        
        Step 4: Engagement and Personality
        Consider the engagement and personality of the writing. A human-like blog post often includes anecdotes, rhetorical questions, humor, or opinions that make the writing more relatable and engaging. Look for elements that add personality and a human touch.
        
        Step 5: Consistency and Natural Language\n\nEnsure that the language used is consistent with how a human would naturally speak or write. Avoid awkward phrasing, overly technical jargon (unless appropriate for the audience***REMOVED***, and repetitive language. The post should sound like it was written by someone knowledgeable and passionate about the topic.
        
        Step 6: Score the Post
        Based on the observations from the steps above, score the blog post on a scale of 1 to 5:
        - 1: The writing is highly unnatural, robotic, and difficult to read.
        - 2: The writing has significant unnatural elements and lacks flow.
        - 3: The writing is somewhat natural but has noticeable issues with flow, tone, or engagement.
        - 4: The writing is mostly natural with minor issues that do not significantly detract from the reading experience.
        - 5: The writing is highly natural, engaging, and indistinguishable from high-quality human-written content.
        
        Scores (SCORE ONLY***REMOVED***: {{***REMOVED******REMOVED***
        Reason : {{***REMOVED******REMOVED***
        """

    def _fluency_prompt(self***REMOVED***:
        """
        Evaluating the human-likeness of a blog post involves a few key steps to ensure that the writing is coherent, engaging, and natural. Here's a step-by-step guide to evaluating this dimension:
        
        Step 1: Read the Entire Post
        Read the entire blog post from start to finish to get an overall sense of its flow, coherence, and readability. This first read-through will help you understand the main points and the structure of the writing.
        
        Step 2: Sentence Flow
        Check if each sentence flows naturally into the next. Look for transitions between sentences and paragraphs that are smooth and logical. Ensure there are no abrupt changes in topic or tone that can disrupt the reader’s experience.
        
        Step 3: Tone and Style
        Assess the tone and style of the writing. It should be consistent throughout the post and appropriate for the intended audience. The style should not be overly robotic or mechanical; instead, it should reflect a human touch with a personal or conversational tone where appropriate.
        
        Step 4: Engagement and Personality
        Consider the engagement and personality of the writing. A human-like blog post often includes anecdotes, rhetorical questions, humor, or opinions that make the writing more relatable and engaging. Look for elements that add personality and a human touch.
        
        Step 5: Consistency and Natural Language
        Ensure that the language used is consistent with how a human would naturally speak or write. Avoid awkward phrasing, overly technical jargon (unless appropriate for the audience***REMOVED***, and repetitive language. The post should sound like it was written by someone knowledgeable and passionate about the topic.
        
        Step 6: Score the Post
        Based on the observations from the steps above, score the blog post on a scale of 1 to 5:
        - 1: The writing is highly unnatural, robotic, and difficult to read.
        - 2: The writing has significant unnatural elements and lacks flow.
        - 3: The writing is somewhat natural but has noticeable issues with flow, tone, or engagement.
        - 4: The writing is mostly natural with minor issues that do not significantly detract from the reading experience.
        - 5: The writing is highly natural, engaging, and indistinguishable from high-quality human-written content.
        
        Scores (SCORE ONLY***REMOVED***: {{***REMOVED******REMOVED***
        Reason : {{***REMOVED******REMOVED***
        """        
