from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
from openai import OpenAI
import random
import os
from datetime import datetime


app = Flask(__name__)

# Set up OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    pages = conn.execute('SELECT * FROM pages ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('index.html', pages=pages)

@app.route('/vote/<int:page_id>/<string:action>', methods=['POST'])
def vote(page_id, action):
    conn = get_db_connection()
    page = conn.execute('SELECT * FROM pages WHERE id = ?', (page_id,)).fetchone()

    if action == 'upvote':
        new_votes = page['votes'] + 1
    elif action == 'downvote':
        new_votes = page['votes'] - 1

    conn.execute('UPDATE pages SET votes = ? WHERE id = ?', (new_votes, page_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():

    random_keyword = generate_subject()
    content = generate_content(random_keyword)
    generated_title = generate_title(content)
    generated_keywords = generate_keywords(content)
    timestamp = datetime.now()

    conn = get_db_connection()
    conn.execute('INSERT INTO pages (title, content, keywords, votes, timestamp) VALUES (?, ?, ?, ?, ?)',
                 (generated_title, content, generated_keywords, 0, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


def get_latest_page():
    conn = get_db_connection()
    page = conn.execute('SELECT * FROM pages ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if not page:
        return {
            'content': 'No previous content. Go crazy!'
        }
    return page


def generate_subject():
    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f"You are going to be used to generate subjects to create articles on a web blog. \
                Give me a random subject or topic that is somewhat related to todays date"},
            {"role": "user", "content": f"todays date: {datetime.now().isoformat()}. please respond with just the random subject"}
        ]
    )
    return completion.choices[0].message.content

def generate_content(keyword):
    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f"You are going to help me generate web articles that will attempt to reach the top of googles searches.\
                I will provide you with a topic and I hope that you will generate an interesting article about that topic. And generate the \
                produce the output as if you were a latina suburbian housewife who loves her husband but also wants to bone the neighbor. You will\
                also be given the previous content, and you should try to make it like a story where the articles plot develops and a story will \
                be created as the content progresses. Just respond with the article content. Do not prefix the content with a title. I will generate \
                that later. Please respond in English."},
            {"role": "user", "content": f"previous_content: {get_latest_page()['content']}  ----------{keyword}"}
        ]
    )
    return completion.choices[0].message.content

def generate_title(content): 
    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f"Summarize the content into a good title. Respond with only the title. Do not prefix it with 'title' \
             or append any extra characters. Absolutely no punctuation.  Please respond in English."},
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message.content  

def generate_keywords(content): 
    openai_client = OpenAI()

    completion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f"Give a bunch of comma seperated keywords I can put in the document page keywords tag. \
             Respond with only the csv seperated keywords. Do not prefix it with 'keywords'. Include a random city in the US as well as one of the kewyords. \
             Don't append any extra characters. Absolutely no punctuation.  Please respond in English."},
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message.content  

@app.route('/page/<int:page_id>')
def page(page_id):
    conn = get_db_connection()
    if page_id == 0:
        page_id = 1
    page = conn.execute('SELECT * FROM pages WHERE id = ?', (page_id,)).fetchone()
    if not page:
        return redirect('/')
    conn.close()

    return render_template('page.html', page=page)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    conn = get_db_connection()
    pages = conn.execute('SELECT id, timestamp FROM pages').fetchall()
    conn.close()

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

    # Static URLs
    sitemap_xml += '<url><loc>https://www.ispillthetea.com/</loc></url>'

    # Dynamic URLs
    for page in pages:
        url = url_for('page', page_id=page['id'], _external=True)
        # lastmod = page['timestamp']
        sitemap_xml += f'<url><loc>{url}</loc></url>'

    sitemap_xml += '</urlset>'

    return Response(sitemap_xml, mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
    # app.run()
