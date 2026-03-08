from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]
    jobdesc = request.form["jobdesc"]

    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    skills = [
        "python","java","sql","machine learning",
        "data analysis","excel","power bi",
        "html","css"
    ]

    found = []
    missing = []

    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)
        else:
            missing.append(skill)

    score = int((len(found)/len(skills))*100)

    job_words = jobdesc.lower().split()
    resume_words = text.lower().split()

    match = 0

    for word in job_words:
        if word in resume_words:
            match += 1

    match_percent = int((match/len(job_words))*100) if job_words else 0

    suggestions = []

    if score < 50:
        suggestions.append("Add more technical skills")

    if "project" not in text.lower():
        suggestions.append("Add project experience")

    if "internship" not in text.lower():
        suggestions.append("Add internship experience")

    if "github" not in text.lower():
        suggestions.append("Add GitHub profile")

    return render_template(
        "result.html",
        skills=found,
        missing=missing,
        score=score,
        match=match_percent,
        suggestions=suggestions
    )

if __name__ == "__main__":
    app.run(debug=True)