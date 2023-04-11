import requests
import pandas as pd
import csv
import time

# URL-адрес
url = "https://api.binance.com/api/v3/klines"

symbol = "BTCUSDT"

interval = "1h"

hours_in_per = 100 * 24

data = []

for i in range(hours_in_per):
    # время начала и конца интервала
    end_time = int(time.time() - i * 3600)
    start_time = end_time - 3600

    # параметры запроса
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time * 1000,
        "endTime": end_time * 1000
    }

    # отправляем GET-запрос к API
    response = requests.get(url, params=params)

    # если запрос был успешным, то добавляем данные в список data
    if response.status_code == 200:
        json_data = response.json()
        if len(json_data) > 0:
            quote = json_data[0]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote[0] / 1000))
            data.append([timestamp, quote[1], quote[2], quote[3], quote[4]])
        else:
            print("No data in the response")
    else:
        print(f"Request failed with status code {response.status_code}")

# создаём dataframe из списка data
df = pd.DataFrame(data, columns=["Timestamp", "Open", "High", "Low", "Close"])

# Сохраняем его в csv-файл
df.to_csv("general_version.FIASCO.csv", index=False)

# Выводим информацию об окончании выполнения скрипта
print(f"Data collection complete. {len(data)} rows of data were collected and saved to file 'general_version.FIASCO.csv'.")