from fine_tuning.data.i_data import IData


from typing import Any


class Data(IData):

    def __init__(self, data_id: str, data: Any, data_type: str):
        if data_id is None or not isinstance(data_id, str):
            raise ValueError("data_id cannot be None")
        self.data_id = data_id
        if data is None:
            raise ValueError("data cannot be None")
        self.data = data
        if data_type is None or not isinstance(data_type, str):
            raise ValueError("data_type cannot be None")
        self.data_type = data_type

    def get_data(self) -> Any:
        return self.data

    def get_data_type(self) -> str:
        return self.data_type

    def get_id(self) -> str:
        return self.data_id

    def __str__(self):
        return f"Data: {self.data_id}, {self.data}, {self.data_type}"


def main():
    data = Data("test", "test23", "test")
    print(data)


if __name__ == "__main__":
    main()
