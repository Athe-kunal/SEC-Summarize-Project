from sec_filings import SECExtractor
import time
import json
import concurrent.futures
from collections import defaultdict
import os


# os.makedirs("data", exist_ok=True)


def multiprocess_run(se: SECExtractor, tic, num_workers: int = 8):
    # print(f"Started for {tic}")
    tic_dict = se.get_accession_numbers(tic)
    text_dict = defaultdict(list)
    for tic, fields in tic_dict.items():
        # os.makedirs(f"data/{tic}", exist_ok=True)
        print(f"Started for {tic}")

        field_urls = [field["url"] for field in fields]
        years = [field["year"] for field in fields]
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_workers
        ) as executor:
            results = executor.map(se.get_text_from_url, field_urls)
        for idx, res in enumerate(results):
            all_text, filing_type = res
            text_dict[tic].append(
                {
                    "year": years[idx],
                    "ticker": tic,
                    "all_texts": all_text,
                    "filing_type": filing_type,
                }
            )
    return text_dict


def get_data(
    ticker: str,
    year: str,
    filing_type: str,
    include_amends: bool = True,
    num_workers: int = 8,
):
    assert filing_type in [
        "10-K",
        "10-Q",
    ], "The supported document types are 10-K and 10-Q"

    if filing_type == "10-K":
        year = str(int(year) + 1)
        start = year + "-01-01"
        end = year + "-12-31"
        amount = 1
    elif filing_type == "10-Q":
        start = year + "-01-01"
        end = year + "-12-31"
        amount = 3
    se = SECExtractor(
        [ticker],
        amount=amount,
        filing_type=filing_type,
        include_amends=include_amends,
        start_date=start,
        end_date=end,
    )

    full_data = multiprocess_run(se, ticker, num_workers)

    return full_data
