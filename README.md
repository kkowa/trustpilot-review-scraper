Project Setup Guide
Follow the steps below to set up your environment and run the scripts.

Steps to Set Up

1. Install Conda

Download and install Conda from the Anaconda or Miniconda website.

2. Create a New Python Environment

Create a new Python environment using the following command:
`conda create --name myenv --file requirements.txt 3. Activate the Environment`

Activate the environment with the following command:
`conda activate myenv `

4. Prepare Data

Create a folder named raw inside the data directory.
Transfer the student data sheet from Monday to this folder.

5. Run the Scraping Script

Run the scraper script to scrape data:
`python -i scraper.py`

Note: This might take a few seconds.

6. Run the Data Manipulation Script

After scraping, run the script to perform matching service:
`python -i matching-service.py `

7. Exit Python Console

Once finished, exit the Python console by using the following command:
`exit()`

8. Disactivate conda enviroment
   `conda disactivate myenv `
