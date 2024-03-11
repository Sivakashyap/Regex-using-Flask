from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    matched_strings = None

    if request.method == "POST":
        test_string = request.form.get("testString")
        regex_pattern = request.form.get("regexPattern")
        flags = request.form.getlist("flags")  
        matched_strings = get_matched_strings(test_string, regex_pattern, flags)

    return render_template("index.html", matched_strings=matched_strings)

@app.route("/results", methods=["POST"])
def results():
    test_string = request.form.get("testString")
    regex_pattern = request.form.get("regexPattern")
    flags = request.form.getlist("flags")
    matched_strings = get_matched_strings(test_string, regex_pattern, flags)
    return render_template("results.html", test_string=test_string, regex_pattern=regex_pattern, flags=flags, matched_strings=matched_strings)

@app.route("/validate-email", methods=["POST"])
def validate_email():
    email = request.form.get("email")
    is_valid = is_valid_email(email)
    return jsonify({"is_valid": is_valid})

def get_matched_strings(test_string, regex_pattern, flags):
    import re
    re_flags = 0
    for flag in flags:
        re_flags |= getattr(re, flag.upper())
    
    regex = re.compile(regex_pattern, re_flags)
    matched_strings = regex.findall(test_string)
    return matched_strings

def is_valid_email(email):
    import re
    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

if __name__ == "__main__":
    app.run(debug=True)
