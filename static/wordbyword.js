document.addEventListener('DOMContentLoaded',function() {
    const story = document.querySelector('#curr_story');
    const addWord = document.querySelector('#add_word');
    const errorMessage = document.querySelector('#apology');
    // const endStory = document.querySelector('#end_story');
    
    function updateStory () {
        axios.get('/story')
            .then(function(response) {
                if (response.data) {
                    story.innerHTML = response.data;
                }
                // if (!response.data) {
                //     document.querySelector('#end_story').style.visibility = 'hidden';
                // }
                // else {
                //     document.querySelector('#end_story').style.visibility = 'visibile';
                // }
            })
    }
    
    setInterval(updateStory, 500);

    function resetErrorMessage(){
        errorMessage.style.color = "rgb(115, 115, 115)";
        errorMessage.innerHTML = "Type a single word and press enter to submit";
    }

    // show error if submits word and then keeps typing
    addWord.addEventListener('keypress',function(event){
        axios.get('/session_error')
            .then(function(response) {
                if (response.data === 'True') {
                    errorMessage.style.color = "#D8000C";
                    errorMessage.innerHTML = "It's someone else's turn to add a word!";
                    setInterval(resetErrorMessage, 10000);
                }
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        // if (event.code === 'Enter') {
        //     axios.get('/dict_error')
        //     .then(function(response) {
        //         if (response.data === 'False') {
        //             errorMessage.style.display = 'inline';
        //             errorMessage.innerHTML = "Word not found in dictionary";
        //         }
        //     })
        //     .catch(function (error) {
        //         // handle error
        //         console.log(error);
        //     })
        // }
    })
    
});

