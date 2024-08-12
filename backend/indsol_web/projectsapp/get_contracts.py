import json

with open("./data/111.json", mode="r", encoding="utf-8-sig") as file:
    data_dict = json.load(file)[0]
    data_dict["contract_number"] = data_dict.pop("НомерДокумента")
    print(data_dict)
