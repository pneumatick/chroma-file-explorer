import { ChromaClient, Collection } from "chromadb";

const client = new ChromaClient();

async function initChroma() {
    const collection = await client.getOrCreateCollection({
        name: "testing"
    });
    return collection;
}

async function db_query(collection: Collection, queryText: string, nResults: number) {
    const result = await collection.query({
        queryTexts: queryText,
        nResults: nResults
    });
    return result;
}

async function addDocument(collection: Collection) {
    await collection.upsert({
        documents: [
            "This is a document about pineapple",
            "This is a document about oranges",
        ],
        ids: ["id1", "id2"],
    });
}

async function main() {
    const collection = await initChroma();

    db_query(collection, "pineapple", 3).then((result) => {
        console.log(result);
    });
}

main();