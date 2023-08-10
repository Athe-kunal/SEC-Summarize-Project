from summarize import generate_summary

ticker = "TSLA"
year = "2021"
filing_type = "10-K"

if __name__ == "__main__":
    final_summary = generate_summary(ticker,year,filing_type)
    print(final_summary)
    


    
