import { ChromaClient, Collection } from "chromadb";

const client = new ChromaClient();

async function initChroma() {
    const collection = await client.getOrCreateCollection({
        name: "testing"
    });
    return collection;
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


const collection = await initChroma();
await addDocument(collection);
collection.query({
    queryTexts: "orange",
    nResults: 3
}).then((result) => {
    console.log(result);
});
