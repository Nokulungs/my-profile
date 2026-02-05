from flask import Flask, render_template, send_from_directory, request
from email.message import EmailMessage
import smtplib
import os

app = Flask(__name__)

@app.route("/")
def home():
    tools = [
        "VS Code",
        "NetBeans",
        "Android Studio",
        "Figma",
        "Git",
        "Power BI",
        "Azure",
        "Docker",
    ]
    return render_template("index.html", tools=tools)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact')
def contact():
    return render_template('contacts.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/download_cv')
def download_cv():
    return send_from_directory('static', 'Sibongokuhle_Bembe_Resume.pdf', as_attachment=True)

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form.get("subject", "Portfolio Contact")
        message = request.form["message"]

        msg = EmailMessage()
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = "nokulungabembe@gmail.com"
        msg["Subject"] = subject
        msg.set_content(f"""
New portfolio message:

Name: {name}
Email: {email}

Message:
{message}
        """)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            smtp.send_message(msg)

        return render_template("contact.html", success=True)

    return render_template("contact.html")

@app.route('/project/<project_name>')
def project_detail(project_name):
    print(f"DEBUG: Requesting project: '{project_name}'")
    
    # Check what templates exist
    try:
        template_files = os.listdir('templates')
        print(f"DEBUG: Available templates: {template_files}")
    except Exception as e:
        print(f"DEBUG: Error listing templates: {e}")
        template_files = []
    
    # Map URL parameters to template files
    project_templates = {
        'apply-smart': 'apply_smart.html',
        'power_bi': 'power_bi.html',
        'meb_hub': 'mebhub.html',
        'contract_guard': 'contract_guard.html',
        'pulse_checkAI': 'pulse_checkAI.html',
        'bais_audit': 'bias_audit.html',  # URL has typo 'bais' but template is 'bias_audit.html'
    }
    
    if project_name in project_templates:
        template_file = project_templates[project_name]
        print(f"DEBUG: Looking for template: {template_file}")
        
        # Check if template exists
        if template_file in template_files:
            print(f"DEBUG: Found template, rendering...")
            return render_template(template_file)
        else:
            # Try alternative names (case-insensitive)
            for actual_file in template_files:
                if actual_file.lower() == template_file.lower():
                    print(f"DEBUG: Found case-insensitive match: {actual_file}")
                    return render_template(actual_file)
            
            print(f"DEBUG: Template '{template_file}' not found. Available: {template_files}")
            return f"""
            <h1>Template Not Found</h1>
            <p>Template file '{template_file}' was not found in the templates folder.</p>
            <p>Requested project: {project_name}</p>
            <p>Available templates: {template_files}</p>
            <p>Try creating the file: templates/{template_file}</p>
            """, 404
    else:
        print(f"DEBUG: Project '{project_name}' not in mapping. Available keys: {list(project_templates.keys())}")
        return f"""
        <h1>Project Not Found</h1>
        <p>Project '{project_name}' was not found.</p>
        <p>Available projects: {list(project_templates.keys())}</p>
        """, 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)