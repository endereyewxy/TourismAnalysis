base_url = "https://travel.qunar.com/travelbook/list.htm?page=1&order=hot_heat"
month_tag = ["&month=1_2_3", "&month=4_5_6", "&month=7_8_9", "&month=10_11_12"]
days_tag = ["&days=1_2_3", "&days=4_5_6_7", "&days=8to10", "&days=11to15", "&days=16tom"]
avg_price_tag = ["&avgPrice=1", "&avgPrice=2", "&avgPrice=3", "&avgPrice=4", "&avgPrice=5"]
actor_type_tag = ["&actorType=1", "&actorType=2", "&actorType=3", "&actorType=4", "&actorType=5", "&actorType=6",
                  "&actorType=7"]
trip_type_tag = ["", "26", "24", "15", "27", "16", "36", "10", "19", "6", "9", "3", "20", "21", "1", "2", "4", "5",
                 "7", "8", "11", "12", "13", "17", "18", "14", "22", "23", "39", "29"]
i = 0
for month in month_tag:
    for days in days_tag:
        for avg_price in avg_price_tag:
            new_url = base_url + month + days + avg_price
            i += 1
            print(new_url)

print(i)
