from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langsmith import traceable, Client
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# --- LangSmith Configuration ---
if os.getenv("LANGSMITH_API_KEY"):
    print(f"LangSmith is configured. Project: {os.getenv('LANGSMITH_PROJECT')}")

# --- Schema Definition ----
class QAResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    confidence: str = Field(description="Confidence Level: high, medium or low")
    reasoning: str = Field(description="The reason behind the answer")
    follow_up_questions: List[str]= Field(description="A list of follow up questions related to the topcic", default_factory=list)
    sources_needed: bool = Field(description="Indicates whether sources are needed for the answer", default=False)


# --- Bot Implementation ---
class QnABot:
    def __init__(
            self,
            model_name: str = "gemini-2.5-flash-lite",
            temperature: float = 0.3
            ):
        
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature
        ).with_structured_output(QAResponse)

        self.prompt = ChatPromptTemplate.from_messages(
            [
            ('system',
             """You are a knowledgeable QnA assistant.

             Your Guidelines:
             - Answer questions accurately and correctly
             - Be honest about uncertainty - set confidence to 'low' if unsure
             - Provide clear reasoning for your answers
             - Suggest relevant follow up questions
             - Indicate if external sources would help

             Always respond with accurate, helpful information.
             
             """),
             ('human','{question}')
            ])
        
        self.chain = self.prompt | self.model

    @traceable(name="ask_question", run_type="chain")
    def ask(self, question:str) -> QAResponse:
        try:
            response = self.chain.invoke({'question':question})
            return response
        except Exception as e:
            return QAResponse(
                answer="I'm sorry, I cannot process your question at this time",
                confidence='low',
                reasoning=str(e),
                follow_up_questions=['Could you please try again?'],
                sources_needed=False
            )
        
    @traceable(name="ask_batch", run_type="chain")  
    def ask_batch(self, questions: List[str]) -> List[QAResponse]:
        """Ask multiple questions in parallel"""
        inputs = [{"question": q} for q in questions]
        return self.chain.batch(inputs)
        

# --- Demo ---

def demo():
    bot = QnABot()

    questions = [
        'what is the capital of france?',
        'what is photosynthesis?'
    ]

    for question in questions:
        response= bot.ask(question)
        print(f"Question :{question}")
        print(f"Answer : {response.answer}")
        print(f"Confidence : {response.confidence}")
        print(f"Reasoning : {response.reasoning}")
        print(f"Follow up questions : {response.follow_up_questions}")
        print(f"Sources Needed : {response.sources_needed}")
        print("-"*50)

if __name__=="__main__":
    try:
        demo()
    finally:
        Client().flush() #Ensure all traces are sent to langsmith
  