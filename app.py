import json, os, re
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

english_json_url = os.path.join(SITE_ROOT, "static", "english_dictionary.json")
english_data = json.load(open(english_json_url))

bangla_json_url = os.path.join(SITE_ROOT, "static", "bangla_dictionary.json")
bangla_data = json.load(open(bangla_json_url))

def clean_english_value(value):
    value = value.replace("\n\n", "<br>")
    value = value.replace("\n", "<br>")
    match = re.findall(r'(\d+\.)', value)
    for i in range(len(match)):
        replace_str = "</li><li>"
        if i == 0:
            replace_str = "<ol><li>"
        if i == (len(match) - 1):
            replace_str = "</li></ol>"
        elif int(match[i][:-1]) < int(match[i-1][:-1]):
            replace_str = "</li></ol><ol><li>"
        value = value.replace(match[i], replace_str, 1)
    return value

def clean_bangla_value(bangla_dict):
    opposite_value = ''
    bangla_value = "<br><div class='well text-dark'><b>Bangla: </b>"+bangla_dict['bangla']+"</div>"
    opposite_list = bangla_dict["opposite"]
    if len(opposite_list) > 0:
        opposite_value += "<div class='well text-dark'><b>Antonyms:</b><br><ul>"
        for opposite in opposite_list:
            opposite_value += "<li>"+opposite+"</li>"
        opposite_value += "</ul></div>"
    return bangla_value + opposite_value

@app.route('/words', methods=['GET','POST'])
def fetch_word():
    if request.method == "POST":
        word = request.form.get("word")
        word = word.strip()
        if word == '':
            return ''
        word_lower = word.lower()
        bangla_value = ''
        english_value = ''
        if word_lower in english_data:
            english_value = clean_english_value(english_data[word_lower])
            if word_lower in bangla_data:
                bangla_value = clean_bangla_value(bangla_data[word_lower])
        return english_value + bangla_value
    else:
        return redirect(url_for('show_index'))

@app.route('/')
@app.route('/index')
def show_index():
    return render_template("index.html")

@app.errorhandler(403)
def not_found_error(error):
    error_code = "Error 403 - Forbidden"
    error_message = "Sorry, access denied or forbidden!"
    return render_template('error.html',
                           error_code = error_code,
                           error_message=error_message), 403

@app.errorhandler(404)
def not_found_error(error):
    error_code = "Error 404 - File not found"
    error_message = "Sorry, requested page is not found!"
    return render_template('error.html',
                           error_code = error_code,
                           error_message=error_message), 404

@app.errorhandler(405)
def not_allowed_error(error):
    error_code =  "Error 405 - Method not allowed"
    error_message = "Sorry, this method is not allowed!"
    return render_template('error.html',
                           error_code = error_code,
                           error_message = error_message), 405

@app.errorhandler(500)
def internal_error(error):
    error_code = "Error 500 - Internal error"
    error_message = "Sorry, internal error occurred!"
    return render_template('error.html',
                           error_code = error_code,
                           error_message = error_message), 500

if __name__ == '__main__':
    app.run(debug = True)
