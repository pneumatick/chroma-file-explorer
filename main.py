import chromadb
from hashlib import sha256

client = chromadb.PersistentClient(path='.')

def testing_init():
    collection = client.create_collection(name='testing')
    collection.add(
        documents=[
            "This is a document about pineapples",
            "This is a document about oranges",
            "This is a document about warfare",
            "This is a picture of a dog",
            "This is a recipe for a cake",
            "This is a meme about cats",
        ],
        ids=["id1", "id2", "id3", "id4", "id5", "id6"]
    )

def chroma_query(prompt):
    collection = client.get_collection(name='testing')
    results = collection.query(
        query_texts=[prompt], 
        n_results=3
    )

    print(f"Results for query: {prompt}")
    for result in results["documents"][0]:
        print(result)

def add_item(data, metadata = None):
    id = sha256(data.encode()).hexdigest()
    collection = client.get_collection(name='testing')

    if metadata:
        collection.add(
            documents=[data],
            ids=[id],
            metadata=[metadata]
        )
    else:
        collection.add(
            documents=[data],
            ids=[id]
        )
    
    print(f"Added item with id: {id}")

""" REPL Functions """

def add():
    data = input("Enter the data you would like to add: ")

    add_item(data)

def search():
    query = input("What are you looking for?: ")
    chroma_query(query)

if __name__ == "__main__":
    command = ""

    while command != "!!":
        command = input("What would you like to do? ((a)dd, (s)earch): ").lower()

        if command == "a" or command == "add":
            add()
        elif command == "s" or command == "search":
            search()
        elif command == "!!":
            print("Quitting...")
            break
        else:
            print("Invalid command \"{command}\"") 