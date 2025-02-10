import chromadb
from hashlib import sha256
import subprocess

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

def chroma_query(prompt, n_results):
    collection = client.get_collection(name='testing')
    results = collection.query(
        query_texts=[prompt], 
        n_results=n_results
    )
    
    return results

def add_item(data, metadata = None):
    id = sha256(data.encode()).hexdigest()
    collection = client.get_collection(name='testing')

    if metadata:
        collection.add(
            documents=[data],
            ids=[id],
            metadatas=[metadata]
        )
    else:
        collection.add(
            documents=[data],
            ids=[id]
        )
    
    print(f"Added item with id: {id}")

def open_file(path):
    subprocess.run(["open", path])

""" REPL Functions """

def add():
    desc = input("Enter a description of the file's contents: ")
    path = input("Enter the file's path (Enter to skip): ")

    if path:
        metadata = {
            "path": path
        }
        add_item(desc, metadata)
    else:
        add_item(desc)

def search():
    command = ""
    while (command != "n" and command != "!!"):
        query = input("What are you looking for?: ")
        results = chroma_query(query, 3)

        for i, desc in enumerate(results["documents"][0]):
            print(
                f"Result {i + 1}: " +
                f"{desc}, " +
                f"{results['metadatas'][0][i]}, " +
                f"Distance: {results['distances'][0][i]}"
            )
        command = input("View file or search again? (Enter number OR (s)earch): ").lower()

        if command.isnumeric():
            open_file(results["metadatas"][0][int(command) - 1]["path"])
            command = input("Search again? (y/n): ").lower()
        elif command == "s" or command == "search":
            continue
        
        if command == "y":
            continue
        elif command == "n" or command == "!!":
            return command
        else:
            print("Invalid command \"{command}\"")

if __name__ == "__main__":
    command = ""

    while command != "!!":
        command = input("What would you like to do? ((a)dd, (s)earch): ").lower()

        if command == "a" or command == "add":
            add()
        elif command == "s" or command == "search":
            command = search()
        elif command == "!!":
            print("Quitting...")
            break
        else:
            print("Invalid command \"{command}\"") 