const information = document.getElementById('info')
information.innerText = `This app is using Chrome (v${versions.chrome()}), Node.js (v${versions.node()}), and Electron (v${versions.electron()})`

const func = async () => {
    const response = await window.versions.ping()
    console.log(response) // prints out 'pong'
}
  
func()

/* Front-end Functionality */

const query_button = document.getElementById('query-button');
query_button.addEventListener('click', async () => {
    const text = document.getElementById('query-text').value;
    const numResults = document.getElementById('n-results').value;
    const response = await window.chroma.query(text, numResults);
    console.log(response);
});