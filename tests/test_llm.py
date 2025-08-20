from dotenv import load_dotenv; load_dotenv()
from src.llms.groqllm import GroqLLM
print(GroqLLM().chat("Say 'VisAgent online' once."))
