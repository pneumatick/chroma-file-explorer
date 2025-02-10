import chromadb
from hashlib import sha256
import subprocess

client = chromadb.PersistentClient(path='.')

def db_init(name):
    collection = client.create_collection(name=name)
    print(f"Created collection with name: {name}")
    return collection

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
    collection = None

    # Create or load collection
    while command == "n" or command == "" and command != "!!":
        command = input("Load or create collection (Enter name OR skip to create): ")
        try:
            collection = client.get_collection(name=command)
            print(f"Loaded collection with name: {command}")
        # Note: Presumptuous to assume that the error is due to the collection not existing
        except:
            if command == "!!":
                break
            
            # Create new collection
            command = input(f"{command} not found. Create new collection with this name? (y/n): ").lower()
            if command == "y":
                collection = db_init(command)

    # Main REPL
    while command != "!!":
        command = input("What would you like to do? ((a)dd, (s)earch), (q)uit: ").lower()

        if command == "a" or command == "add":
            add()
        elif command == "s" or command == "search":
            command = search()
        elif command == "!!" or command == "q" or command == "quit":
            break
        else:
            print("Invalid command \"{command}\"") 
    
    print("Quitting...")