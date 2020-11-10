# -*- coding: utf-8 -*-
from flask import *
from datetime import timedelta
import os
from utils import add_watermark, read_watermark

app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)

app.config["SECRET_KEY"] = "RUIN"

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/convert/')
def convert():
    return render_template('converter.html')

src_filename = 'kanata.jpg'
wm_filename = 'watermark.jpg'
wmget_filename = 'watermark.jpg'

@app.route('/watermark/', methods=['POST', 'GET'])
def watermark():
    canDownload = False
    global src_filename, wm_filename
    if request.method == 'POST':
        f = request.files['src']
        g = request.files['wm']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        if f.filename == '':
            flash('Please select your image!')
            canDownload = False
        else:
            if g.filename != '':
                src_filename = f.filename
                wm_filename = g.filename
                src_upload_path = os.path.join(basepath, 'static/img/upload', src_filename)
                wm_upload_path = os.path.join(basepath, 'static/img/upload', wm_filename)
                f.save(src_upload_path)
                g.save(wm_upload_path)
                add_watermark(src_upload_path, wm_upload_path)
            else:
                src_filename = f.filename
                src_upload_path = os.path.join(basepath, 'static/img/upload', src_filename)
                f.save(src_upload_path)
                add_watermark(src_upload_path)
            canDownload = True
            flash('Done! You can download the processed image now.')

    return render_template('watermark.html', src='img/upload/' + src_filename, wm='img/upload/' + wm_filename, res='img/res/'+src_filename[:-4]+'_res.png', canDownload = canDownload)

@app.route('/extractor/', methods=['POST', 'GET'])
def extract():
    global src_filename, wmget_filename
    canDownload = False
    if request.method == 'POST':
        f = request.files['src']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        if f.filename == '':
            flash('Please select your image!')
            canDownload = False
        else:
            src_filename = f.filename
            src_upload_path = os.path.join(basepath, 'static/img/upload', src_filename)
            f.save(src_upload_path)
            read_watermark(src_upload_path)
            canDownload = True

    return render_template('extractor.html', src='img/upload/'+src_filename, wm='img/res/'+src_filename[:-4]+'_extract.png', canDownload = canDownload)

if __name__ == '__main__':
    app.run(debug=True)