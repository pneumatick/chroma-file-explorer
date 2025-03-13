import chromadb
from hashlib import sha256
import subprocess

client = chromadb.PersistentClient(path='.')

def db_init(name):
    collection = client.create_collection(name=name)
    print(f"Created collection with name: {name}")
    return collection

def chroma_query(collection, prompt, n_results):
    results = collection.query(
        query_texts=[prompt], 
        n_results=n_results
    )
    
    return results

def add_item(collection, data, metadata = None):
    id = sha256(data.encode()).hexdigest()

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

def add(collection):
    desc = input("Enter a description of the file's contents: ")
    path = input("Enter the file's path (Enter to skip): ")
    filetype = input("Enter the file's type (Enter to skip): ")

    if path:
        metadata = {
            "path": path,
            "type": filetype
        }
        add_item(collection, desc, metadata)
    else:
        add_item(collection, desc)

def search(collection):
    command = ""
    while (command != "n" and command != "!!"):
        query = input("What are you looking for?: ")
        results = chroma_query(collection, query, 3)

        for i, desc in enumerate(results["documents"][0]):
            print(
                "\n" +
                f"Result {i + 1}: " +
                f"{desc}, " +
                f"{results['metadatas'][0][i]}, " +
                f"Distance: {results['distances'][0][i]}" +
                "\n"
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
            coll_name = command
            command = input(f"{command} not found. Create new collection with this name? (y/n): ").lower()
            if command == "y":
                collection = db_init(coll_name)

    # Main REPL
    while command != "!!":
        command = input("What would you like to do? ((a)dd, (s)earch), (q)uit: ").lower()

        if command == "a" or command == "add":
            add(collection)
        elif command == "s" or command == "search":
            command = search(collection)
        elif command == "!!" or command == "q" or command == "quit":
            break
        else:
            print("Invalid command \"{command}\"") 
    
    print("Quitting...")