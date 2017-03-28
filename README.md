# redditlike-webapp
Hello!
I've created a reddit-like website having some features of reddit such as voting system, karma system, hierarchical comment system, various sorting methods and a few more features.

Backend has been created with Python/Django using only Class Based Views. Frontend however has been created with HTML, CSS, Bootstrap and a little bit of jQuery.

This project consits of three apps: r (the main one), user and message.

The main app (r) handles everything related to the subforums, posts, comments, voting, user registration and authentication etc.

The user app stores and processes the data about the activity of the given user (created threads, comments etc.)

The last app (message) allows to send private messages, as well as stores data about the replies to your threads, comments, shows the post/threads in which you were mentioned (e.g. @nazen93) and keeps the sent messages history.
