# Hydrachain Staking Statistics
A console based tool for generating staking statistics from a exported csv file.



- **Usage**:

  

  **Download the latest version** from [here](https://github.com/ItsGosho/hydrachain-staking-statistics/releases) and store the **hydrachain-staking-statistics.exe** somewhere.

  **Export your transactions data** from the **Hydra GUI Interface** by going to the **Transactions** tab and clicking at the **Export** button down right.

  **Run the program** by opening a **Windows Terminal** and providing the **exported file** as **argument**.

  - `.\hydrachain-staking-statistics.exe --csv-file-path "C:\Users\itsgo\Desktop\hydra-export-1.csv"`

  <img src=".\pics\example_output_1.png" alt="example_output_1.png" />

  

  - You can change the **Month End**, **Today** & **Diff** column currencies by providing the `--currency "BGN"` argument.
  - **Note:** ***When first started***, a prices and currency rates synchronization will be made. It will take some time. That is due to rate limiting from CoinGecko's API. 

- **Feature**:
  - Option to get the staking statistics by public address
  - Option to export the full monthly staking statistics data as a json.
  - Option to visualize only selected columns.



- **References:**



**APIs:**

- [exchangerate.host](https://exchangerate.host) - providing a **free** currency rates historical retrieval.
  - The project is completely **free**. You can **[donate](https://exchangerate.host/#/donate)** them to keep projects like this one running.
- [coingecko.com](https://www.coingecko.com/en/api) - providing a **free** hydra price historical retrieval.
  - They have different plans. We are using a **free** one, which comes with **[limitations](https://www.coingecko.com/en/api/pricing)**, but for **free** - **we can't complaint** :)

**Python Libraries:**

- [PrettyTable](https://pypi.org/project/prettytable/) - Viewing data as tables at the terminal.

- [TinyDB](https://pypi.org/project/tinydb/) - Lightweight document oriented database.



- **Feedback**:

**If there are any problems**, please start the program in debug mode by passing the `--log-level "DEBUG"` argument. The log contains detailed information about the state of the program. Open a pull request with the provided log.

**!Note** that the log contains information about all of your transactions!
