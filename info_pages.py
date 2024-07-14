from flask import Blueprint, render_template_string

info_pages = Blueprint('info_pages', __name__)

# Define the HTML strings for each page
about_us_html = """
<!DOCTYPE html>
<html>
<head>
    <title>About Us</title>
    <link rel="stylesheet" href="static/index.css">
</head>
<body>
    <h1>About Us</h1>
    <p>Welcome to our blog! We share tips and stories about gardening and neighborhood gossip. Whether you're looking for advice on growing your own vegetables or just want to catch up on the latest news in the community, you're in the right place.</p>
    <p>Thanks for visiting and happy reading!</p>
</body>
</html>
"""

contact_us_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Us</title>
    <link rel="stylesheet" href="static/index.css">
</head>
<body>
    <h1>Contact Us</h1>
    <p>If you have any questions, suggestions, or just want to say hello, feel free to contact us using the form below:</p>
    <form action="/submit_contact_form" method="post">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email"><br>
        <label for="message">Message:</label><br>
        <textarea id="message" name="message"></textarea><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

privacy_policy_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy</title>
    <link rel="stylesheet" href="static/index.css">
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Your privacy is important to us. We do not share your personal information with third parties.</p>
    <p>Any data we collect is used solely to improve your experience on our blog.</p>
</body>
</html>
"""

terms_of_service_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Terms of Service</title>
    <link rel="stylesheet" href="static/index.css">
</head>
<body>
    <h1>Terms of Service</h1>
    <p>By using our blog, you agree to comply with our rules and regulations. Please be respectful in your comments and interactions with others.</p>
    <p>We reserve the right to remove any content that we deem inappropriate.</p>
</body>
</html>
"""

disclaimer_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Disclaimer</title>
    <link rel="stylesheet" href="static/index.css">
</head>
<body>
    <h1>Disclaimer</h1>
    <p>The information provided on our blog is for general informational purposes only. We do our best to ensure that the content is accurate and up-to-date, but we make no guarantees regarding its completeness or reliability.</p>
    <p>Any actions you take based on the information found on this blog are at your own risk.</p>
</body>
</html>
"""



# Define the routes for each page
@info_pages.route('/about')
def about_us():
    return render_template_string(about_us_html)

@info_pages.route('/contact')
def contact_us():
    return render_template_string(contact_us_html)

@info_pages.route('/privacy')
def privacy_policy():
    return render_template_string(privacy_policy_html)

@info_pages.route('/terms')
def terms_of_service():
    return render_template_string(terms_of_service_html)

@info_pages.route('/disclaimer')
def disclaimer():
    return render_template_string(disclaimer_html)



