# Word by Word

#### Video Demo:  https://www.youtube.com/watch?v=-nwS44wn3hQ
#### Overview:
Word by Word is a web app that allows users to collaboratively build a story, one word at a time. The landing page shows the story currently being written. The user can enter a new word at the end of the existing story. Users must wait for someone else to contribute to the story before they can add another word. No one can predict how the story will develop. At any point, except immediately after submitting a word, a user can chose to end the story by clicking the "end story" button. When a user ends the story, the story is inserted into a database and the user gets to add a title. After the user adds a title, the user is routed to the archive page, which displays all of the previously submitted stories. I hope you'll check out Word by Word and see what we can create together!

#### Description:
word_style.css contains all of the styles for the html pages. The overall style is simple and intuitive, with a calm color scheme. I formated the input fields to autofocus, blend into the background, and appear on the same line as the story in progress to create the illusion of adding to a story seamlessly. The links and buttons have hover effects with gradual transitions. The error message also gradually transitions for a less jarring effect. 

wordbyword.js contains the code that updates the story in real time. The js file sends a get request to a route that returns the current story. By running the function every half second, the user will continue to see the most up-to-date story without having to refresh the page. The js file sends a get request to another route to determine whether the same user is trying to submit two words in a row. If so, the code updates the inner html of the message field on the landing page to remind the user to wait until someone else has added a word to submit another word. after 10 seconds, the error message automatically disappears and the instruction message is reset.

layout.html provides a shell for the other html pages, with blocks for each pages navigation bar and main content. 

index.html displays an instruction for how to submit a word, and it shows the current story using jinga. The index page provides an input field immediately after the last word of the current story, through which the user can submit a new word. If the user tries to submit multiple words in a row, the instruction is replaced with an error message reminding the user to wait for another turn. Finally, the page has an 'end story' button which causes the current story to be archived in a SQL database and routes the user to the title page. 

title.html shows an autofocused input field for the user to add a title and an instruction message, and it displays the story that just ended with jinja. After a user submits a title, she is routed to the archive page. archive.html uses jinja to display all of the previously submitted stories, along with their title and submission date, in reverse chronological order. about.html is a simple page with a container describing the site and a little bit about me, with a link to my LinkedIn page. 

helpers.py contains all of the helper functions user by app.py to querying the database for the words and stories submitted and check for user error.
    
The get_current_story_num function queries the database for the current story and returns the maximum story id number. The get_current_story function takes a number argument and queries the database for all words the story with that number id. The function then returns the queried story formatted as a string.
    
The same_session function queries the database for the session id of the most rencently submitted word and compares it with the session id for a new word being submitted. If the session ids are the same, the function returns true. Otherwise the function returns false.
    
The insert_word function takes a string and number as arguments. It trims extra spaces from the word passed in and and checks to ensure that only one word has been submitted, i.e. that there are no internal spaces. If so, the function inserts the new word into a word table in the database with the story id passed to the function and the current session id and returns true. Otherwise the word is not inserted and the function returns false.

The archive_story function takes a number argument and adds a string of the most recently submitted story to a story table, along with the date submitted. The function then inserts a blank new story into the table to be updated after users write a new story. 

app.py routes the user throughout the site with use of the functions in helpers.py.

The index page is rendered with index.html and by passing in a string of the current story by calling in the get_current_story function. When the user tries to submit a word in the input field, app.py calls the same_session function. If the function returns true, the user is redirected back to the index page, essentially rejecting the new submission. If the function returns false, app.py calls the insert_word function to check if a valid word has been submitted. If so, the word is accepted and the user is redirected to the index page again. Otherwise, if the user clicks the end story button and the story is not blank, the archive_story function is called and the user is redirected to the title page. 

The story route is used by the js file to continually update the story displayed on the index page so that users can see the up-to-date story without refreshing the page. The session error route is also used by the js file to check if a user is attempting to submit two words in a row.

The archive route queries the stories table for the story with the highest id, i.e. the most recent story. The route then creates a dictionary of the story containing the stories title, date, and content. The dictionary is passed in when the archive.html file is rendered so that the previously submitted stories can be displayed.

The title route displays the story that was just archived by passing in a string of that story's content. When a user submits a title through the input field, the stories database is updated to add that title to that story's row. Finally, the about page simply renders the content on the about.html page.