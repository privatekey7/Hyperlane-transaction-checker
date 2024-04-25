import requests
import csv
from tqdm import tqdm


def get_wallet_transactions(wallet_address):
    base_url = 'https://explorer.hyperlane.xyz/api'
    action = 'module=message&action=search-messages'
    url = f'{base_url}?{action}&query={wallet_address}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data["status"] == "1":
        return len(data["result"])
    else:
        print(f"Error occurred while fetching transactions for wallet {wallet_address}.")
        return None


def main():
    try:
        with open('wallets.txt', 'r') as file:
            wallet_addresses = file.readlines()
            wallet_addresses = [address.strip() for address in wallet_addresses]

        results = []
        for wallet_address in tqdm(wallet_addresses, desc="Processing"):
            transaction_count = get_wallet_transactions(wallet_address)
            if transaction_count is not None:
                results.append((wallet_address, transaction_count))
            else:
                print(f"Failed to get transaction count for wallet {wallet_address}")

        with open('result.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Wallet Address', 'Transaction Count'])
            csv_writer.writerows(results)

        print("Результаты успешно записаны в файл result.csv")

    except FileNotFoundError:
        print("Файл wallets.txt не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
