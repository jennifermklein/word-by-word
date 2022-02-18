document.addEventListener('DOMContentLoaded',function() {
    const story = document.querySelector('#curr_story');
    
    function updateStory () {
        axios.get('/story')
            .then(function(response) {
                story.innerHTML = response.data;
                // if (!response.data) {
                //     document.querySelector('#end_story').style.display = 'none';
                // }
                // else {
                //     document.querySelector('#end_story').style.display = 'inline';
                // }
            })
    }
    
    setInterval(updateStory, 500);

});

