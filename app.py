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
        # I_L_whole_text, summary_I_L, len_I_L_whole_text, len_summary_I_L = Story_Summarizer(file, source_lang, percentage_input)
    return render_template('summary.html', I_L_whole_text=I_L_whole_text, len_I_L_whole_text=len_I_L_whole_text, summary_I_L=summary_I_L, len_summary_I_L=len_summary_I_L, text=text, len_text=len_text, summary=summary, len_summary=len_summary)
    # return render_template('summary.html', I_L_whole_text=I_L_whole_text, summary_I_L=summary_I_L, len_I_L_whole_text=len_I_L_whole_text, len_summary_I_L=len_summary_I_L)

if __name__ == "__main__":
    app.run(debug=True)






# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, emit
# import json
# from summarizatio_tf_idf import Story_Summarizer

# app = Flask(_name_)

# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# @socketio.on('connect')
# def test_connect():
#     print('Client connected')
#     emit('my response', {'data': 'Connected'})

# def start_progress(total):
#     print("Starting progress bar")
#     socketio.emit('start_progress', {'total': total})

# def update_progress(current, total):
#     percent_complete = (current / total) * 100
#     print(f"Updating progress: {percent_complete}%")
#     socketio.emit('progress', {'percentage': percent_complete})

# def end_progress():
#     print("Ending progress bar")
#     socketio.emit('end_progress', {})

# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/analyze', methods=['GET', 'POST'])
# def analyze():
#     if request.method == "POST":
#         file = request.files['file']
#         file.save(file.filename)
#         source_lang = request.form['source_lang']
#         percentage_input = int(request.form['percentage_input'])

#         # create a progress bar
#         start_progress(100)

#         I_L_whole_text, len_I_L_whole_text, summary_I_L, len_summary_I_L, text, len_text, summary, len_summary = Story_Summarizer(file, source_lang, percentage_input)

#         end_progress()

#         return render_template('summary.html', I_L_whole_text=I_L_whole_text, len_I_L_whole_text=len_I_L_whole_text, summary_I_L=summary_I_L, len_summary_I_L=len_summary_I_L, text=text, len_text=len_text, summary=summary, len_summary=len_summary)

#     return render_template('index.html')

# if _name_ == "_main_":
#     socketio.run(app, debug=True)