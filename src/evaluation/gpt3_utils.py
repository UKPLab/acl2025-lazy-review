import tqdm
import pandas as pd

from dotenv import load_dotenv, find_dotenv
from openai import AzureOpenAI
import os


def load_gpt():

    _ = load_dotenv(find_dotenv())

    client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"), api_version="2023-12-01-preview", azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))

    return client


def cost_calculation(prompt_price, completion_price, prompt_tokens, completion_tokens):

    prompt_cost = prompt_tokens * prompt_price / 1000
    completion_cost = completion_tokens * completion_price / 1000

    return prompt_cost + completion_cost