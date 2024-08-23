import requests
import xml.etree.ElementTree as ET
import ollama
import os



#standard library
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#I'll define __all__ = [] inside filter
#which will define all of the filters that should be run in seperate emails.
#from filter import filter
from filters import __filters__

#OPTIONS
VERBOSE = False
USE_OLLAMA = True
TO_EMAIL = "andrew.william.engel@gmail.com"
SUBJECT = "Daily Arxiv Digest"

def query_arxiv(max_results=10):
    # Calculate the date for one day ago
    one_day_ago = datetime.now() - timedelta(days=2)
    date_filter = one_day_ago.strftime('%Y%m%d')
    now = datetime.now().strftime('%Y%m%d')

    #requests library is messing this up for us. build it ourselves.
    #submitted date seemingly doesn't play with categories. we will have to sort ourselves.
    url = f'http://export.arxiv.org/api/query?search_query=submittedDate:[{date_filter}+TO+{now}]&max_results={max_results}&start:0&'
    # Send the request to the arXiv API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.text)
        
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        if entries == []:
            print("Successful query, but returned no results. Check your query.")

        n_entries = len(entries)
        # Extract and print details for each paper

        with open('./result.txt','w') as f:

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):

                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                link = entry.find('{http://www.w3.org/2005/Atom}id').text
                category = [category.get('term') for category in entry.findall('{http://www.w3.org/2005/Atom}category')]


                for filter in __filters__:
                    if filter(title, summary, authors, published, link, category):
                        if USE_OLLAMA:
                            ollama_summary = summarize_with_ollama(summary)
                        if VERBOSE:
                            print(f"Filter Satisfied: {filter.__name__}")
                            print(f"Title: {title}")
                            print(f"Authors: {', '.join(authors)}")
                            print(f"Published: {published}")
                            print(f"Summary: {summary}")
                            print(f"Link: {link}\n")
                            print(f"Category: {category}\n")
                            if USE_OLLAMA:
                                print(f"Ollama Summary: {ollama_summary}")

                        f.write(f"Filter Satisfied: {filter.__name__}\n")
                        f.write(f"Title: {title}\n")
                        f.write(f"Authors: {', '.join(authors)}\n")
                        f.write(f"Link: {link}\n")
                        if USE_OLLAMA:
                            f.write(f"Ollama Summary: {ollama_summary}\n")
                        else:
                            f.write(f"Summary: {summary}\n")

                        f.write('\n----------------------------------------------------\n')
        
    else:
        print(f"Failed to retrieve data from arXiv. Status code: {response.status_code}")

def send_email(to_email, subject, password):
    # Email configuration
    from_email = "andrew.william.engel@gmail.com"
    from_password = password  # You may need an app-specific password if using Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    with open('./result.txt','r') as f:
        body = f.read()

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, from_password)  # Login to the email account
        
        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main(max_results,to_email,subject,password):
    #this function queries the arxiv, uses OLLAMA to summarize, writes to result.txt
    query_arxiv(max_results)

    #now send an email to myself based on the result.txt
    send_email(to_email,subject,password)

if __name__ == '__main__':
    if USE_OLLAMA:
        ollama.pull('llama3.1')
        def summarize_with_ollama(abstract):
            # Command to call Ollama with the abstract
            response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'user',
                'content': f'Please summarize the following research paper abstract in a few sentences; only respond with the summary: {abstract}',
            },
            ])

            return response['message']['content']

    #get password from environment variable
    password = os.environ.get('password')

    main(4000,TO_EMAIL,SUBJECT,password)