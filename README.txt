# arxiv_subscriber

about: arxiv_subscriber will query the arxiv API for articles within the last 2 days then
send an email with results passing filters to your own email account. 

This is a small project repository to play around with local large language models. The intention
is to enable users to easily modify aspects of the API request and LLM prompt to perform a task.
Currently, the LLM is used to summarize the main result from the abstract in a few sentences.

Currently, I assume that the user has access to a gmail account.

###Installation steps:

* Install ollama from their website: https://ollama.com/
* Install dependencies: conda env create -f environment.yml
* Create a web-app password for the app to send emails autonomously. This can be done in your google settings.
* Set an environment variable called "password" to be accessed from within conda virtual environment
* Using the templates in filters.py, create filters that you want to search over daily arxiv papers
* Add the names of your filters to __filters__ list in filters.py
* Create a cron job or scheduled task to run the script daily

Enjoy!
