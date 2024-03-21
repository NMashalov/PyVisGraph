const form = document.querySelector('.input-group');
form.addEventListener('submit', handleFormSubmit);


base_url = '127.0.0.1'


async function handleFormSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);    
    const formJSON = Object.fromEntries(data.entries());
    alert(formJSON)
    // const response = await fetch(
    //     "http://example.com/movies.json",{
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json;charset=utf-8'
    //         },
    //         body: JSON.stringify(user),
    //     }
    // );
    // let result = await response.json();
    // alert(result.message);
    // const results = document.querySelector('.results pre');
//   results.innerText = JSON.stringify(formJSON, null, 2);
}