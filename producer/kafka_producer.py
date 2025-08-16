import json
import random
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
from faker import Faker

# Initialisation
fake = Faker()
ref_start_time = datetime(2025, 6, 1, 0, 0, 0)

# Liste d'utilisateurs "frauduleux" (répétés souvent)
fraudulent_users = [f"u{uid}" for uid in range(9990, 9995)]

# Connexion à Kafka
try:
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(" Connexion à Kafka réussie")
except Exception as e:
    print(" Échec de la connexion à Kafka :", e)
    exit(1)

# Fonction pour générer une transaction fictive
def generate_transaction(i, start_time):
    timestamp = start_time + timedelta(seconds=i)

    # 20% des transactions viennent d'utilisateurs "frauduleux"
    if random.random() < 0.2:
        user_id = random.choice(fraudulent_users)
    else:
        user_id = f"u{random.randint(1000, 9999)}"

    return {
        "user_id": user_id,
        "transaction_id": f"t-{i:07}",
        "amount": round(random.uniform(5.0, 5000.0), 2),
        "currency": random.choice(["EUR", "USD", "GBP"]),
        "timestamp": timestamp.isoformat(),
        "location": fake.city(),
        "method": random.choice(["credit_card", "debit_card", "paypal", "crypto"])
    }

# Boucle d'envoi continue
if __name__ == "__main__":
    print(" Lancement du producteur... Appuyez sur Ctrl+C pour arrêter.")
    i = 0
    try:
        while True:
            num_events = random.randint(10, 100)
            for _ in range(num_events):
                event = generate_transaction(i, ref_start_time)
                producer.send("transactions", value=event)
                print(f" Sent: {event['transaction_id']} | {event['user_id']} | {event['amount']} {event['currency']} | {event['method']}")
                i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Producteur arrêté par l'utilisateur.")
