from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    
    return f"<h1>Hello, {name}!</h1>"

@app.route('/comment', methods=['POST'])
def post_comment():
    comment = request.form.get('comment', '')
    
    html = f"""
    <html>
        <body>
            <h2>Your comment:</h2>
            <p>{comment}</p>
        </body>
    </html>
    """
    
    return html

@app.route('/search')
def search():
    from markupsafe import escape
    query = request.args.get('q', '')

    return render_template_string("<h1>Search results for: {{ query }}</h1>", query=query)

@app.route('/profile')
def profile():
    username = request.args.get('user', 'Anonymous')
    bio = request.args.get('bio', '')
    
    page = f"""
    <html>
        <head><title>User Profile</title></head>
        <body>
            <h1>{username}</h1>
            <div>{bio}</div>
        </body>
    </html>
    """
    
    return page

@app.route('/error')
def error_page():
    error_msg = request.args.get('msg')
    
    return f"<div class='error'>{error_msg}</div>"

@app.route('/dashboard')
def dashboard():
    user_input = request.args.get('data', '')
    
    response = make_response(f"<p>Dashboard data: {user_input}</p>")
    return response

def render_user_content(content):
    return f"<div class='user-content'>{content}</div>"

if __name__ == '__main__':
    app.run(debug=True)
