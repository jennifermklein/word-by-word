document.addEventListener('DOMContentLoaded',function() {
    
    document.querySelector('#newPara').addEventListener("click", function() {
        const labelNode = document.createElement('label');
        labelNode.innerHTML = 'test';
        words += '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
        storyText.innerHTML = words;
        submitWord.focus();
    });

});