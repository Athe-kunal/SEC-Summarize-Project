import json
import re
import os
import openai
import logging
import sys
from typing import List
from app.section_names import SECTIONS_10K, SECTIONS_10Q
from llama_index.llms import OpenAI
from llama_index.callbacks import CallbackManager
from llama_index.llms import (
    CustomLLM, 
    CompletionResponse, 
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.llms.base import llm_completion_callback
from typing import Any

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index import (
    VectorStoreIndex,
    ListIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
)
from llama_index.response_synthesizers import TreeSummarize
from dotenv import load_dotenv

# import nest_asyncio
# nest_asyncio.apply()
from app.data_loader import *

# Load variables from .env file
load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_base = os.getenv("OPENAI_API_BASE")

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = openai_api_base
os.environ["NUMEXPR_MAX_THREADS"] = "16"

# query_str = """
#     Can you provide a comprehensive summary of the given text? The summary should cover all the key points and numerical figures presented in the original text, while also condensing the information. 
# """

query_str = """
 You are financial statement analyst, provide a comprehensive summary of the given text which covers the key points and ALL the numerical figures presented in the original text, while also condensing the information. DON'T MISS OUT ON ANY NUMERICAL FIGURES.

"""
context_window = 1024
num_output = 512
model_name = "meta-llama/Llama-2-70b-chat-hf"

class AnyscaleLLM(CustomLLM):

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=context_window,
            num_output=num_output,
            model_name=model_name
        )
    
    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        chat_completion = openai.ChatCompletion.create(
            model="meta-llama/Llama-2-70b-chat-hf",
            messages=[{"role": "system", "content": "You are a financial statement expert, provide a comprehensive summary of the given text. The summary should cover all the key points and numerical figures presented in the original text, while also condensing the information."}, {"role": "user", "content": prompt}],
            # temperature=0.7
            )
        text = chat_completion["choices"][0]["message"]["content"]
        print(text)
        return CompletionResponse(text=text)
    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        raise NotImplementedError()
    
def get_response(
    doc: str,
    query_str: str,
    chunk_size: int = 1024,
    chunk_overlap: int = 128,
    verbose: bool = True,
    use_async: bool = True,
):
    service_context = ServiceContext.from_defaults(
        # llm_predictor=AnyscaleLLM(),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    summarizer = TreeSummarize(
        verbose=verbose, service_context=service_context, use_async=use_async
    )

    response = summarizer.get_response(query_str, [doc])
    return response


def get_summary(
    docs: List[str],
    metadata: List[dict],
    ticker,
    year,
    filing_type: str = "10-K",
    quarters: str = "",
):
    os.makedirs("summaries", exist_ok=True)
    if filing_type == "10-K":
        ALL_SECTIONS = SECTIONS_10K
    elif filing_type == "10-Q":
        ALL_SECTIONS = SECTIONS_10Q
    full_summary = ""
    for section in ALL_SECTIONS:
        summary = ""
        # Give me the idxs in splitted metadata for which we have this section

        sections_docs = ""
        section_amended_docs = ""
        for idx, meta in enumerate(metadata):
            sm = meta["full_metadata"]
            if section in sm:
                if sm.endswith(filing_type):
                    sections_docs = docs[idx]
                elif sm.endswith(f"{filing_type}/A"):
                    # elif sm.endswith("10-K/A"):
                    section_amended_docs = docs[idx]
        if filing_type == "10-Q":
            file_name = f"summaries/{ticker}_{year}_{filing_type}_{quarters}.txt"
        elif filing_type == "10-K":
            file_name = f"summaries/{ticker}_{year}_{filing_type}.txt"

        if sections_docs == "":
            summary += " ".join(section.split("_")) + "\n"
            summary += ""
            summary += "\n\n"
            full_summary += summary
            with open(file_name, "a") as f:
                f.write(summary)
        elif section_amended_docs == "" and sections_docs != "":
            response = get_response(sections_docs, query_str)
            summary += " ".join(section.split("_")) + "\n"
            summary += response
            summary += "\n\n"
            full_summary += summary
            with open(file_name, "a") as f:
                f.write(summary)
        elif section_amended_docs != "" and sections_docs != "":
            section_response = get_response(sections_docs, query_str)
            section_amended_response = get_response(section_amended_docs, query_str)
            summary += " ".join(section.split("_")) + "\n"
            summary += section_response + "\n\n"
            summary += "Amended Section: \n" + section_amended_response
            summary += "\n\n"
            full_summary += summary
            with open(file_name, "a") as f:
                f.write(summary)
    return full_summary


def generate_summary(
    ticker: str,
    year: str,
    filing_type: str = "10-K",
    include_amends: bool = True,
    num_workers: int = 8,
    quarters: bool = "",
):
    docs, metadata = load_documents(
        ticker, year, filing_type, include_amends, num_workers, quarters
    )
    final_summary = get_summary(
        docs, metadata, ticker, year, filing_type, quarters=quarters
    )

    return final_summary
