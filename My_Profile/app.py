from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/project/<project_name>')
def project_detail(project_name):
    if project_name == 'apply-smart':
        return render_template('apply_smart.html')
    elif project_name == 'power_bi':
        return render_template('power_bi.html')
    elif project_name == 'meb_hub':
            return render_template('mebhub.html')
    else:
        return "Project not found", 404

if __name__ == '__main__':
    app.run(debug=True)