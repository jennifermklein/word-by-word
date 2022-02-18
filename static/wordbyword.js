document.addEventListener('DOMContentLoaded',function() {
    const story = document.querySelector('#curr_story');
    
    function updateStory () {
        axios.get('/story')
            .then(function(response) {
                story.innerHTML = response.data;
            })
    }
    
    setInterval(updateStory, 500);

});

