installation steps:

* install ollama from their website
* install dependencies: conda env create -f environment.yml
* Create a password for the app to send emails
* set an environment variable called "password" to be accessed from within conda virtual environment
* using the templates in filters.py, create filters that you want to use to pass daily arxiv papers
* add the names of your filters to __filters__ list in filters.py
* create a cron job to run the script daily

Enjoy!
