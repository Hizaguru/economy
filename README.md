This is easy portfolio asset calculator for jupyter-notebook.

Use pip or conda to calculate the assets of your portfolio. Here's how:

1. Clone the project `git clone https://github.com/Hizaguru/economy.git`

2. Create a Python virtual environment using venv: `python3 -m venv venv`

3. Activate the environment for macOS/Linux/WSL `source venv/bin/activate`
For Windows: `venv\Scripts\activate`

4. Install the required libraries by running the following command from the project directory: `pip install -r requirements.txt`
5. Open Jupyter Notebook: `jupyter-notebook`

6. In Jupyter Notebook, navigate to the directory where you cloned the project and open the notebook file (e.g., Portfolio_template.ipynb).

7. In the notebook, find the section where the tickers array is defined. Add the tickers of your portfolio to this array, separating each ticker with a comma. For example: `tickers = ['AAPL', 'GOOG', 'MSFT']`

8. Run the script by executing each cell in the notebook. This will calculate the assets of your portfolio based on the provided tickers.

Note: Ensure that you have an active internet connection while running the script, as it retrieves stock data from online sources.

Remember to save your modified notebook after adding your tickers, and feel free to customize the notebook further according to your requirements.

If you encounter any issues or have further questions, please let me know!
