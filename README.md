# Scheduled_ETL_pipeline_Covid19_Data

In this project, I designed and implemented a robust and scheduled data pipeline to automate the extraction, transformation, and loading (ETL) of data from an external API into Google Drive. The primary objectives of the project were to ensure data reliability, cleanliness, and accessibility for further analysis and reporting.

Key Technologies and Tools Used:
- Apache Airflow: I leveraged Apache Airflow, an open-source orchestration tool, to create a flexible and scalable workflow for managing the data pipeline. Airflow allowed for task scheduling, error handling, and easy monitoring of data transfer processes.

- Python 3: I utilized Python 3 as the primary programming language to develop custom scripts and data processing logic. Python's extensive libraries and ecosystem enabled efficient data manipulation and transformation.

- Ubuntu: The project ran on an Ubuntu-based environment, providing a stable and secure platform for executing data pipeline tasks.

- Google Drive API: I integrated the Google Drive API into the project to programmatically interact with Google Drive, facilitating the storage and organization of extracted data files.

- Flask: Flask is a lightweight Python web framework used for building web applications and APIs with simplicity and flexibility.

- Tableau: Tableau is a powerful data visualization and business intelligence tool that creates interactive, insightful visualizations from various data sources.

Project Workflow:
1. Data Extraction: I configured the pipeline to retrieve data from the external API at scheduled intervals. This ensured that the most up-to-date information was available for analysis.

2. Data Processing and Transformation: After data retrieval, I applied data cleaning and transformation operations using Python. This step included data validation, normalization, and enrichment to prepare the data for downstream consumption.

3. File Upload to Google Drive: I employed the Google Drive API to seamlessly upload the processed data files to designated folders in Google Drive. Each file was given a meaningful name and stored in an organized structure.
