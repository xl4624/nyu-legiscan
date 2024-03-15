from client import LegiscanClient
from config import LEGISCAN_API_KEY


def main():
    client = LegiscanClient(LEGISCAN_API_KEY)
    monitor_list = client.get_monitor_list()
    print(monitor_list[0])


if __name__ == "__main__":
    main()
