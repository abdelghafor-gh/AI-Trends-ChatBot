from azure.cosmos import CosmosClient

class AuthDBFactory:
    _client = None
    _database = None

    @classmethod
    def get_container(cls,url, key, database_name, container_name):
        """
        Retrieve a Cosmos DB container client, initializing the connection if necessary.

        :param url: Cosmos DB URL
        :param key: Cosmos DB primary key
        :param database_name: Name of the database
        :param container_name: Name of the container
        :return: Container client
        """
        if cls._client is None:
            # Initialize the Cosmos DB client and database connection
            cls._client = CosmosClient(url, credential=key)
            cls._database = cls._client.get_database_client(database_name)

        if cls._database is None:
            raise ValueError("Database connection could not be established.")

        # Retrieve the specified container client
        return cls._database.get_container_client(container_name)
