import random 
import datetime as dt
import pandas as pd
import numpy as np 
import time 
import json 
from kafka import KafkaProducer

data = pd.read_csv("/home/thynguyen1/data-pipeline/data/logistic_data_TEST.csv") 

suppliers = data["final_deli_supplier"].unique()
destination_regions = data["destination_region"].unique()
districts = data["destination_district"].unique()
depart_regions = data["departure_region"].unique()
sellers = data[data["seller_id"] < 2400]["seller_id"].unique()
routes = data["route"].unique()



def generate_order() -> dict:
    print("Generator")
    random_order_code = int(random.randrange(11111, 99999, 5))
    random_distance = int(random.randrange(1, 2695))
    random_supplier = random.choice(suppliers)
    random_destination_region = random.choice(destination_regions)
    random_districts = random.choice(districts)
    random_departure_region = random.choice(depart_regions)
    random_seller_id = int(random.choice(sellers))
    random_route = random.choice(routes)
    random_product = int(random.randrange(1, 200))

    return {
        'order_code': random_order_code,
        'distance': random_distance,
        'final_deli_supplier': random_supplier,
        'destination_region': random_destination_region,
        'destination_district': random_districts,
        'departure_region': random_departure_region,
        'seller_id': random_seller_id,
        'route': random_route,
        'product_id': random_product,
        'created_at':dt.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    }


# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=serializer
)


if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    while True:
        # Generate a message
        dummy_message = generate_order()
        print(dummy_message)
        print(json.dumps(dummy_message))
        # Send it to our 'messages' topic
        # print(f'Producing message @ {dt.date.now()} | Message = {str(dummy_message)}')
        producer.send('orders', dummy_message)
        producer.flush()
        
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(5, 11)
        time.sleep(time_to_sleep)