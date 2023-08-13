import nest_asyncio
import json
import re
import os
import openai
import logging
import sys
from typing import List
from section_names import SECTIONS_10K, SECTIONS_10Q

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

nest_asyncio.apply()
from data_loader import *

os.environ["OPENAI_API_KEY"] = ""

openai.api_key = os.environ["OPENAI_API_KEY"]
os.environ["NUMEXPR_MAX_THREADS"] = "16"

query_str = """
    Can you provide a comprehensive summary of the given text? The summary should cover all the key points and numerical figures presented in the original text, while also condensing the information. 
"""


def get_response(
    doc: str,
    query_str: str,
    chunk_size: int = 1024,
    chunk_overlap: int = 128,
    verbose: bool = True,
    use_async: bool = True,
):
    service_context = ServiceContext.from_defaults(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    summarizer = TreeSummarize(
        verbose=verbose, service_context=service_context, use_async=use_async
    )

    response = summarizer.get_response(query_str, [doc])
    return response


def get_summary(
    docs: List[str], metadata: List[dict], ticker, year, filing_type: str = "10-K",quarters:str=""
):
    os.makedirs("summaries",exist_ok=True)
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
        if filing_type=="10-Q":
            file_name = f"{ticker}_{year}_{filing_type}_{quarters}.txt"
        elif filing_type == "10-K":
            file_name = f"{ticker}_{year}_{filing_type}.txt"

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
    quarters:bool="ALL"
):
    docs, metadata = load_documents(ticker, year, filing_type,include_amends,num_workers,quarters)
    final_summary = get_summary(
        docs,
        metadata,
        ticker,
        year,
        filing_type,
        quarters=quarters
    )

    return final_summary
