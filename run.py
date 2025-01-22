from worker import RequestParams, Worker
from dataset_models import QuerySet
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# Load custom BASE_URL and API_KEY from .env file

DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

LINGYI_BASE_URL = os.getenv('LINGYI_BASE_URL')
LINGYI_API_KEY = os.getenv('LINGYI_API_KEY')

async def main():
    # Example usage with deepseek. But you can use any api provider:    

    # Step 1: Instantiate a QuerySet object
    
    # Only csv and xlsx files supported
    query_set=QuerySet("example_queries.csv")

    # You can use a local list instead
    
    # query_list = [
    #     "What's the city with the lowest annual average temperature in the world?",
    #     "Which city has the highest population density in the world?",
    #     "What is the capital of France?",
    #     "Who wrote 'Romeo and Juliet'?",
    #     "What is the largest ocean on Earth?",
    #     "Which country is known as the Land of the Rising Sun?",
    #     "What is the currency of Japan?",
    #     "Who painted the Mona Lisa?",
    #     "What is the tallest mountain in the world?"
    # ]
    # query_set = QuerySet(query_list)

    # Step 2: Create a RequestParams object. It's like a reusable worker profile.
    
    deepseek_params = RequestParams(
        base_url=DEEPSEEK_BASE_URL,
        api_key=DEEPSEEK_API_KEY,
        model="deepseek-chat"
    )
    
    lingyi_params = RequestParams(
        base_url=LINGYI_BASE_URL,
        api_key=LINGYI_API_KEY,
        model="yi-lightning"
    )
    
    # Create a worker (QuerySet-> ResponseSet)
    deepseek_worker = Worker(deepseek_params)
    lingyi_worker = Worker(lingyi_params)

    # Step 3: Organize tasks
    
    async def deepseek_task():
        # Custom query key available in invoke method. Default to "query".
        result = await deepseek_worker.invoke(query_set)
        
        # Note: Will overwrite existing files
        result.store_to("deepseek.xlsx")
    
    async def lingyi_task():
        result = await lingyi_worker.invoke(query_set)
        result.store_to("lingyi.xlsx")
    
    # Step 4: Hit and run!
    
    await asyncio.gather(deepseek_task(), lingyi_task())
    
if __name__ == "__main__":
    asyncio.run(main())