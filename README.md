# Hydrachain Staking Statistics
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ItsGosho/hydrachain-staking-statistics/blob/main/LICENSE)
[![Version](https://img.shields.io/github/v/release/ItsGosho/Button-Enhanced?include_prereleases)](https://github.com/ItsGosho/hydrachain-staking-statistics/releases)

A console based tool for generating staking statistics from a exported csv file. View by each month how much hydra you have acquired from staking, the earned reward in selected currency and additional statistics. The program is open-source and requires no payment for usage thanks to the used APIs.



## Usage:

**1. Download the latest version** from [here](https://github.com/ItsGosho/hydrachain-staking-statistics/releases) and store the **hydrachain-staking-statistics.exe** somewhere.

**2. Export your transactions data** from the **Hydra GUI Interface** by going to the **Transactions** tab and clicking at the **Export** button down right.

**3. Run the program** by opening a **Windows Terminal** and providing the **exported file** as **argument**.

- `.\hydrachain-staking-statistics.exe --csv-file-path "C:\Users\itsgo\Desktop\hydra-export-1.csv"`

<img src=".\pics\example_output_1.png" alt="example_output_1.png" />

- *The example output in the image is taken from a random address!*
- You can change the **Month End**, **Today** & **Diff** column currencies by providing the `--currency "BGN"` argument.
- **Note:** When first started, a prices and currency rates synchronization will be made. It will take some time. That is due to rate limiting from CoinGecko's API. 



## Column Explanation:

- **Monthly Staking Statistics:**

| Column                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| Month                           | The month for which the transactions statistics in the row are for. There is a ***** at the end of the month if the month is the current one. |
| Transactions                    | The total staking transactions for the month.                |
| Mined                           | The total staking hydra income for the month.                |
| Daily Transactions              | The average transactions per day for the month. If the month is not yet finished, then it is calculated by the passed days of the month. |
| Daily Mined                     | The average mined per day for the month. If the month is not yet finished, then it is calculated by the passed days of the month. |
| Hydra Monthly Price             | The hydra price at the last day of the month in USD. The value will be **-** if the month is not yet finished. |
| Income Monthly *CURRENCY*       | The total staking earnings by the hydra price at the last day of the month in a selected currency. The value will be **-** if the month is not yet finished. |
| Income Today *(PRICE CURRENCY)* | The total staking earnings by the today hydra price in a selected currency. |
| Income Change *CURRENCY*        | The total win/lose of hydra price change by Income Monthly *CURRENCY* and Income Today *CURRENCY* in selected currency. The value will be **-** if the month is not yet finished. |
| Lowest Block                    | The lowest mined block for the month.                        |
| Highest Block                   | The highest mined block for the month.                       |
| Avg Block                       | The average mined block for the month                        |

- **Overall Staking Statistics:**

| Column                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| Transactions                    | The total staking transactions.                              |
| Mined                           | The total staking hydra income.                              |
| Income Today *(PRICE CURRENCY)* | The total staking earning by the today hydra price in a selected currency. |

## Future:

- Option to get the staking statistics by public address
- Option to export the full monthly staking statistics data as a json.
- Option to visualize only selected columns.



## References:

**APIs:**

- [exchangerate.host](https://exchangerate.host) - **Free** currency rates historical retrieval.
  - The project is completely **free**. You can **[donate](https://exchangerate.host/#/donate)** them to keep projects like this one running.
- [coingecko.com](https://www.coingecko.com/en/api) - **Free** hydra price historical retrieval.
  - They have different plans. We are using a **free** one, which comes with **[limitations](https://www.coingecko.com/en/api/pricing)**, but for **free** - **we can't complaint**!

**Python Libraries:**

- [PrettyTable](https://pypi.org/project/prettytable/) - Viewing data as tables at the terminal.

- [TinyDB](https://pypi.org/project/tinydb/) - Lightweight document oriented database.



## Feedback:

**If there are any problems**, please start the program in debug mode by passing the `--log-level "DEBUG"` argument. The log contains detailed information about the state of the program. Open a [issue](https://github.com/ItsGosho/hydrachain-staking-statistics/issues) with the provided log.

**Note:** The log contains information about all of your transactions!
