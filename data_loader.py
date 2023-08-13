import json
import re
import os
from typing import List
from data_extraction import get_data


def get_input_files(ticker_name: str, year: str, document_type: List[str]):
    file_names_list = []
    for files in os.listdir(f"data/{ticker_name}/{year}"):
        if files.startswith(document_type):
            file_names_list.append(f"data/{ticker_name}/{year}/{files}")
    return file_names_list


def find_files(filing_type):
    file_list = []
    for root, _, filenames in os.walk("data"):
        for file in filenames:
            if file.startswith(filing_type):
                file_list.append(os.path.join(root, file))
    return file_list


def post_process(text):
    text = re.sub(r"\\.", "", text)
    sentence_splits = text.split(".")
    sentence_with_delimiter = ".\n".join(sentence_splits)
    sentence_with_delimiter = re.sub(r" {2,}", "\n\n", sentence_with_delimiter)
    return sentence_with_delimiter


def load_documents(
    ticker_name: str,
    year: str,
    filing_type: str,
    include_amends: bool,
    num_workers: int,
    quarters:str
):
    full_data = get_data(
        ticker=ticker_name,
        year=year,
        filing_type=filing_type,
        include_amends=include_amends,
        num_workers=num_workers,
        quarters=quarters
    )

    documents = []
    metadata = []

    for tic_data in full_data[ticker_name]:
        curr_year = tic_data["year"]
        ticker = tic_data["ticker"]
        filing_type = tic_data["filing_type"]

        for section, section_text in tic_data["all_texts"].items():
            documents.append(section_text)
            metadata.append(
                {
                    "year": curr_year,
                    "ticker": ticker,
                    "section": section,
                    "filing_type": filing_type,
                }
            )
    post_process_docs = [post_process(doc) for doc in documents]
    post_process_metadata = []
    for sm in metadata:
        metadata_dict = {}
        metadata_dict.update(
            {
                "full_metadata": sm["ticker"]
                + "_"
                + sm["year"]
                + "_"
                + sm["section"]
                + "_"
                + sm["filing_type"]
            }
        )

        post_process_metadata.append(metadata_dict)

    assert len(post_process_docs) == len(
        post_process_metadata
    ), f"Length of splitted docs and metadata should be the same, but got {len(post_process_docs)} and {len(post_process_metadata)} respectively"

    return post_process_docs, post_process_metadata


# docs,metadata = load_documents("TSLA","2021","10-K")
