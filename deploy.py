from flask import Flask, render_template, request,send_from_directory,redirect,url_for
import os
from werkzeug import secure_filename
from code import process

up = 'up/'
down = 'down/'

app = Flask(__name__,template_folder = 'static/')
app.static_folder = 'static/'

@app.route('/')
def feed():
   return redirect(url_for('upload'))

@app.route('/upload')
def upload():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      global fname
      fname = f.filename
      f.save(os.path.join(up,secure_filename(f.filename)))
      path = os.path.join(up,fname)
      process(path,down)
      return redirect(url_for('fetch'))

@app.route('/fetch')
def fetch():
   fname = 'output.csv'
   return send_from_directory(directory = down,filename = fname,mimetype = 'text/csv')

   
if __name__ == '__main__':
   app.run()

