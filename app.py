from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Resume & LinkedIn Optimizer</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 40px; }
        .box { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 15px; }
        textarea { width: 100%; height: 160px; margin: 10px 0 20px; padding: 12px; font-size: 14px; }
        button { background: black; color: white; padding: 14px 24px; border: none; border-radius: 8px; cursor: pointer; }
        .result { background: #eeeeee; padding: 20px; margin-top: 25px; border-radius: 10px; white-space: pre-wrap; }
    </style>
</head>
<body>
<div class="box">
    <h1>Resume & LinkedIn Optimizer</h1>
    <p>Paste your resume and a job description. This app will score your resume, suggest keywords, and create LinkedIn content.</p>

    <form method="POST">
        <h3>Your Resume</h3>
        <textarea name="resume" placeholder="Paste your resume here..."></textarea>

        <h3>Job Description</h3>
        <textarea name="job" placeholder="Paste the job description here..."></textarea>

        <button type="submit">Optimize</button>
    </form>

    {% if result %}
    <div class="result">
        <h2>Results</h2>
        {{ result }}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

def optimize_resume(resume, job):
    resume_lower = resume.lower()
    job_lower = job.lower()

    score = 100
    tips = []

    if len(resume.split()) < 120:
        score -= 15
        tips.append("Add more details to your experience, projects, education, or activities.")

    if "skills" not in resume_lower:
        score -= 10
        tips.append("Add a clear Skills section.")

    if "leadership" not in resume_lower:
        score -= 10
        tips.append("Add leadership examples if you have them.")

    action_words = ["created", "managed", "improved", "organized", "led", "developed", "increased", "assisted"]
    if not any(word in resume_lower for word in action_words):
        score -= 15
        tips.append("Use stronger action verbs like led, created, improved, managed, or developed.")

    job_words = job_lower.replace(",", " ").replace(".", " ").split()
    resume_words = resume_lower.replace(",", " ").replace(".", " ").split()

    missing_keywords = []
    for word in job_words:
        if len(word) > 6 and word not in resume_words and word not in missing_keywords:
            missing_keywords.append(word)

    missing_keywords = missing_keywords[:12]

    result = f"""
Resume Score: {score}/100

Missing Job Keywords:
{", ".join(missing_keywords) if missing_keywords else "No major missing keywords found."}

Resume Improvement Tips:
- """ + "\n- ".join(tips if tips else ["Your resume looks solid. Add numbers and specific results to make it stronger."]) + """

Better Resume Bullet Examples:
- Led a team project by organizing tasks, communicating updates, and meeting deadlines.
- Improved efficiency by creating a simple system to track responsibilities and progress.
- Assisted customers or team members by solving problems and keeping communication clear.

LinkedIn Headline:
Motivated Student | Future Healthcare Professional | Leadership, Communication, and Teamwork

LinkedIn About Section:
I am a motivated student interested in healthcare, leadership, and professional growth. I enjoy learning through hands-on experiences, working with others, and building skills that prepare me for future opportunities. I am currently focused on gaining experience, improving my communication skills, and contributing positively wherever I work or volunteer.
"""
    return result

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        resume = request.form.get("resume", "")
        job = request.form.get("job", "")

        result = optimize_resume(resume, job)

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)