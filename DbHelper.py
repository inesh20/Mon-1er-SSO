
import boto3
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

class DynamoDBHelper():

    # Init function
    def __init__(self, table_name):
        ## WARN : A ne pas faire dans la vraie vie!!!!
        self.ACCESS_KEY_ID = os.getenv(self.ACCESS_KEY_ID)
        self.ACCESS_SECRET_KEY = os.getenv(self.ACCESS_SECRET_KEY)
        self.table = None

        self.dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=self.ACCESS_KEY_ID,
        aws_secret_access_key=self.ACCESS_SECRET_KEY,
        region_name='eu-west-3'
        )

        try:
            self.table = self.dynamodb.create_table(
                TableName=table_name,
                # Clé primaire
                KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
                # Type String
                AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],  
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )

            print(f"Table {table_name} en cours de création...")
            # Wait until the table exists.
            self.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

        except:
            self.table = self.dynamodb.Table(table_name)
            self.table.load()  # Charge les métadonnées pour vérifier l'existence
            print(f"La table '{table_name}' existe déjà.")
     
    def add_user(self, data):
        # Insérer un élément dans la table
        self.table.put_item(Item=data)

    def get_user(self, email):
        # Récupérer un élément
        return self.table.get_item(Key={'email': email})
    
    def login(self, email, password):
        account = self.get_user(email)
        if account and self.check_password(password, account['Item']['password']):
            return {"identified": True}
        else:
            return {"identified": False}
    

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()  # Generate a salt
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
        return hashed.decode('utf-8')  # Convert bytes to string

    
    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))