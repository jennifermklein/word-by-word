document.addEventListener('DOMContentLoaded',function() {
    const story = document.querySelector('#curr_story');
    const addWord = document.querySelector('#add_word');
    const errorMessage = document.querySelector('#apology');
    const endStory = document.querySelector('#end_story');
    
    function updateStory () {
        axios.get('/story')
            .then(function(response) {
                if (response.data) {
                    story.innerHTML = response.data;
                }
                // if (!response.data) {
                //     document.querySelector('#end_story').style.display = 'none';
                // }
                // else {
                //     document.querySelector('#end_story').style.display = 'inline';
                // }
            })
    }
    
    setInterval(updateStory, 500);

    // show error if submits word and then keeps typing
    addWord.addEventListener('keypress',function(event){
        axios.get('/session_error')
            .then(function(response) {
                if (response.data === 'True') {
                    errorMessage.style.display = 'inline';
                    errorMessage.innerHTML = "It's someone else's turn to add a word";
                }
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
    })

    // endStory.addEventListener('click',function(event){
    //     axios.get('/session_error')
    //         .then(function(response) {
    //             if (response.data === 'True') {
    //                 errorMessage.style.display = 'inline';
    //                 errorMessage.innerHTML = "It's someone else's turn to add a word";
    //             }
    //         })
    //         .catch(function (error) {
    //             // handle error
    //             console.log(error);
    //         })
    // })

});


      // if (event.code === 'Enter') {
        //     document.querySelector('.buttons').style.backgroundColor = 'red';
        // }

