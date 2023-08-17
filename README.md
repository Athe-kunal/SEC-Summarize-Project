## SEC FILINGS SUMMARIZATION

* In this repo, we are summarizing the SEC filings. You can launch the app after installing all the dependencies

```python
cd app
pip install -r requirements.txt
```

Fill in your OpenAI API Key in the `.env` file

Launch the app by 

```
streamlit run Home.py
```

Also, you can run the Dockerfile (image name is sec-summarize) by

```
docker build -t sec-summarize .
```
Run the docker container by

```
docker run -p 8501:8501 sec-summarize
```
Here is an example of summary for Tesla Q3 2022

```
FINANCIAL STATEMENTS


MANAGEMENT DISCUSSION
The company's mission is to accelerate the world's transition to sustainable energy. They design, develop, manufacture, lease, and sell electric vehicles, solar energy systems, and energy storage products. They also offer maintenance, installation, operation, financial, and other services related to their products. The company is focused on increasing vehicle production, capacity, and delivery capabilities, improving battery technologies, and expanding their global infrastructure. They have produced 929,910 vehicles and delivered 908,573 vehicles in 2022. They have also deployed 4.08 GWh of energy storage products and 248 megawatts of solar energy systems. The company has recognized total revenues of $21.45 billion and $57.14 billion for the three and nine months ended September 30, 2022, respectively. Their net income attributable to common stockholders was $3.29 billion and $8.87 billion for the same periods. They ended the third quarter of 2022 with $21.11 billion in cash and cash equivalents and marketable securities. The company's cash flows provided by operating activities during the nine-month period ended September 30, 2022, was $11.45 billion. Their capital expenditures amounted to $5.30 billion during the same period. In the three months ended September 30, 2022, interest income increased by $109 million, or 352%, compared to the same period in 2021. In the same period, interest expense decreased by $73 million, or 58%, compared to the three months ended September 30, 2021. Other (expense) income, net, changed unfavorably by $79 million in the three months ended September 30, 2022, compared to the same period in 2021. The provision for income taxes increased by $82 million, or 37%, in the three months ended September 30, 2022, compared to the same period in 2021. Net income attributable to noncontrolling interests and redeemable noncontrolling interests decreased by $2 million, or 5%, in the three months ended September 30, 2022, compared to the same period in 2021. In the nine months ended September 30, 2022, interest income increased by $109 million, or 352%, compared to the same period in 2021. In the same period, interest expense decreased by $142 million, or 47%, compared to the nine months ended September 30, 2021. Other (expense) income, net, changed unfavorably by $68 million in the nine months ended September 30, 2022, compared to the same period in 2021. The provision for income taxes increased by $449 million, or 110%, in the nine months ended September 30, 2022, compared to the same period in 2021. Net income attributable to noncontrolling interests and redeemable noncontrolling interests decreased by $92 million, or 89%, in the nine months ended September 30, 2022, compared to the same period in 2021. As of September 30, 2022, the company had $19.53 billion of cash and cash equivalents, with balances held in foreign currencies having a U.S. dollar equivalent of $6.28 billion. The company had $2.41 billion of unused committed amounts under its credit facilities as of September 30, 2022. Net cash provided by operating activities increased by $4.53 billion to $11.45 billion during the nine months ended September 30, 2022, compared to the same period in 2021. Capital expenditures were $5.30 billion for the nine months ended September 30, 2022, mainly for the expansions of various manufacturing facilities. Net cash used in financing activities decreased by $914 million to $3.03 billion during the nine months ended September 30, 2022, compared to the same period in 2021. The fair market value of the company's remaining holdings of digital assets as of September 30, 2022, was $226 million.

MARKET RISK DISCLOSURES
The company conducts global business in multiple currencies, which exposes them to foreign currency risks. These risks include revenue, costs of revenue, operating expenses, and localized subsidiary debt denominated in currencies other than the U.S. dollar. The company is generally a net receiver of currencies other than the U.S. dollar for their foreign subsidiaries. Fluctuations in exchange rates impact their revenue and operating results in U.S. dollars, as they do not typically hedge foreign currency risk. The company has experienced fluctuations in net income due to gains or losses on the settlement and re-measurement of monetary assets and liabilities denominated in non-local currencies. Based on historical trends, adverse changes in foreign currency exchange rates of 10% for all currencies could be experienced in the near-term. These changes would have resulted in a gain or loss of $56 million at September 30, 2022, and $277 million at December 31, 2021, assuming no foreign currency hedging. The company is also exposed to interest rate risk on their borrowings with floating rates. They utilize derivative instruments to manage some of this risk, but not for trading or speculative purposes. A hypothetical 10% change in interest rates on their floating rate debt would have had an immaterial impact on interest expense for the nine months ended September 30, 2022, and 2021.

CONTROLS AND PROCEDURES


LEGAL PROCEEDINGS
The text discusses litigation related to the acquisition of SolarCity. It does not provide any specific numerical figures.

RISK FACTORS
The given text discusses various risks and challenges faced by the company, including the impact of the global COVID-19 pandemic on operations, disruptions in the supply chain, and government regulations. It also mentions the shortage of semiconductors, labor shortages, and worker absenteeism. The text highlights the importance of suppliers, stable production workforce, and government cooperation for sustaining production and meeting demand. It mentions delays in launching and ramping production of new products, as well as potential challenges during production ramps. The text also emphasizes the impact of disruptions in the supply chain and the global shortage of semiconductors on production. 

Numerical figures mentioned in the text include the company's outstanding indebtedness of $2.41 billion as of September 30, 2022, and the various currencies in which the company transacts business and has debt denominated, including the Chinese yuan, euro, South Korean won, and pound sterling.

USE OF PROCEEDS
In March 2017, warrants were sold to several entities, including Goldman, Sachs & Co., Deutsche Bank Securities Inc., Citigroup Global Markets Inc., National Bank of Canada (assigned from Citigroup), Morgan Stanley & Co. LLC, and Barclays Capital Inc. These warrants were connected to the offering of the 2.375% Convertible Senior Notes due 2022. Between July 1, 2022, and August 15, 2022, a total of 28,853,619 shares of common stock were issued to the 2017 Warrantholders upon exercising their warrants. These shares were issued under an exemption from registration provided by Rule 3(a)(9) of the Securities Act of 1933.

DEFAULTS


MINE SAFETY


OTHER INFORMATION
```