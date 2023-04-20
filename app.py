from flask import Flask, render_template, request
from summarizatio_tf_idf import Story_Summarizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == "POST":
        file = request.files['file']
        file.save(file.filename)
        source_lang = request.form['source_lang']
        percentage_input = int(request.form['percentage_input'])
        
        I_L_whole_text, len_I_L_whole_text, summary_I_L, len_summary_I_L, text, len_text, summary, len_summary = Story_Summarizer(file, source_lang, percentage_input)
    return render_template('summary.html', I_L_whole_text=I_L_whole_text, len_I_L_whole_text=len_I_L_whole_text, summary_I_L=summary_I_L, len_summary_I_L=len_summary_I_L, text=text, len_text=len_text, summary=summary, len_summary=len_summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






