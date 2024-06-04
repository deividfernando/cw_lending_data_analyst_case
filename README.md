## Data Analyst Case Study

### Overview
This repository contains the solution to a Data Analyst case study aimed at assessing proficiency in SQL and data visualization. The case involves analyzing and managing loan and client data from a Brazilian bank to provide valuable business insights.

### Table of Contents
1. [Introduction](#introduction)
2. [Dataset Description](#dataset-description)
3. [Analysis and Results](#analysis-and-results)
4. [Methodology](#methodology)
5. [Setup and Usage](#setup-and-usage)
6. [Contact](#contact)

### Introduction
The goal of this case study is to evaluate skills in SQL and data visualization. The tasks involve using SQL to query data from a PostgreSQL database and utilizing Python libraries for data analysis and visualization. The dataset includes information about clients and their loan transactions.

### Dataset Description
- **Clients Table:** Contains information about the clients, including their status, credit limits, and interest rates.
- **Loans Table:** Contains details about loans, including the amount, due dates, and payment status.

### Analysis and Results
This section includes detailed analysis and insights derived from the dataset. Each analysis includes SQL queries, Python code, and visualizations to support the findings.

1. **Best Month for Loan Issuance:** Identify the month with the highest number of loans issued.
2. **Batch Adherence:** Determine which batch of clients had the highest loan adherence.
3. **Interest Rates and Loan Outcomes:** Analyze the impact of different interest rates on loan default rates.
4. **Client Ranking:** Rank the top 10 and bottom 10 clients based on loan performance.
5. **Default Rate Analysis:** Calculate the default rate by month and batch.
6. **Profitability Assessment:** Evaluate the profitability of the loan operations over time.

### Methodology
The analysis follows a structured approach:
1. **Data Loading:** Load the data from CSV files into a PostgreSQL database.
2. **SQL Queries:** Use SQL to perform data extraction and manipulation.
3. **Data Visualization:** Utilize Python libraries such as Pandas and Matplotlib for data analysis and visualization.
4. **Documentation:** Provide a clear explanation of the logic and methodology used in each step of the analysis.

### Setup and Usage
To reproduce the analysis, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/data-analyst-case-study.git

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Set Up PostgreSQL Database:**
- Create a PostgreSQL database and update the connection details in the .env file.
- Load the data into the database using the provided scripts.

4. **Run the Jupyter Notebook:**
- Open the Jupyter Notebook to view and run the analysis.

### Contact
For any questions or further information, please contact Devid Fernando at [deivid.silva@cloudwalk.io].
