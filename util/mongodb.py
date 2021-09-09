from typing import List, Any

import pymongo
import gridfs

class MongoConnection():
    """
    This class handles all the MongoDB related operations.
    """

    def __init__(self, username: str, password: str, server: str, database: str):
        self.username = username
        self.password = password
        self.server = server
        self.database = database
        self.db = None

    def connect(self):
        """
        Connect to the desired mongodb instance
        :return: MongoDB database
        """
        client = pymongo.MongoClient(
            "mongodb://{0}:{1}@{2}:27017/{3}?ssl=true&replicaSet=atlas-bzsgmi-shard-0&authSource=admin&retryWrites=true&w=majority"
                .format(self.username, self.password, self.server, self.database))
        self.db = client[self.database]
        return self.db

    def get_collection(self, collection_name: str):
        """
        Get MongoDB collection
        :param collection_name: The name of the collection
        :return: Database collection
        """
        return self.db[collection_name]

    def create_index(self, name: str, collection: str, fields: List[Any]) -> str:
        """
        Creates an index on the collection, using the mentioned fields.
        :param name: Index name
        :param collection: Collection name
        :param fields: List of fields and their specifics
        :return: The created index name
        """
        index_name = collection.create_index(fields, name=name)
        return index_name

    def search_by_text_field(self, collection, field_name: str, search_text: str):
        """
        Search by the desired text field
        :param collection: Collection instance
        :param field_name: Field name by which to search
        :param search_text: Text used for searching
        :return: The document matching the search criteria
        """
        result = collection.find_one({"$text": {"$search": search_text}})
        return result

    def find_by_fields(self, collection, search_field_values, multiple=True):
        """
        Search documents by field name and values
        :param collection: Collection instance
        :param search_field_values: Field by which to search
        :return: The documents matching the search criteria
        """
        if multiple:
            result = collection.find(search_field_values)
        else:
            result = collection.find_one(search_field_values)
        return result

    def find_by_fields_and_update(self, collection, search_field_values, field_to_update: str, value_for_update: object):
        """
        Search document by field name and update the values for a key in the searched document
        :param collection:
        :param search_field_values:
        :param field_to_update:
        :param value_for_update:
        :return: Whether update has been successfully performed or not
        """
        new_values = { "$set": { field_to_update: value_for_update }}

        collection.update_one(search_field_values, new_values)
        return True

    def add_document(self, collection, document):
        """
        Add a new document to the collection
        :param collection: Collection instance
        :param document: Document JSON
        :return: THe document id returned after inserting in collection
        """
        document_id = collection.insert_one(document).inserted_id
        return document_id

    def drop_all_indexes(self, collection) -> bool:
        """
        Drop all the indexes in the collection
        :param collection: Collection instance
        :return: Boolean value to indicate whether the operation was successful
        """
        collection.drop_indexes()
        return True



    def test(self):
        client = pymongo.MongoClient(
            "mongodb://apurva:{0}@cluster0-shard-00-00.ke7sx.mongodb.net:27017,cluster0-shard-00-01.ke7sx.mongodb.net:27017,cluster0-shard-00-02.ke7sx.mongodb.net:27017/hied?ssl=true&replicaSet=atlas-bzsgmi-shard-0&authSource=admin&retryWrites=true&w=majority".format(
                "Check.mate01#"))
        db = client.test

        # GridFS

        fs = gridfs.GridFS(db)
        file_id = fs.put(open('C:\\Users\\223033329\Downloads\\config.txt', 'rb'), metadata={'filename': 'config.txt'},
                         filename='config.txt')
        file = fs.get(file_id)
        data = file.read()

        file = fs.find_one({'filename': {'$regex': 'config*'}})
        data = file.read()
        file._id
        file2 = fs.get(file_id=file._id)

        file_id = fs.put(open('C:\\Users\\223033329\Downloads\\config.txt', 'rb'), metadata={'filename': 'config.txt'},
                         filename='config.txt', file_id=file._id)
        file = fs.get(file_id)
        file._id

        # PyMongo

        db.list_collection_names()
        user_documents = db['user-documents']

        user_document = {"author": "ak", "tags": ["SOP"], "university_id": 1}
        user_document_id = user_documents.insert_one(user_document).inserted_id
        user_document_id

        user_documents.drop_indexes()
        user_documents.create_index([("author", pymongo.ASCENDING), ("university_id", pymongo.DESCENDING)],
                                    name='user_doc_author_university')
        user_documents.create_index([("author", "text")], name='user_doc_author')
        user_documents.find_one({"$text": {"$search": "ak"}})
