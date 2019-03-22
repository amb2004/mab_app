import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import time
from proccess import home_page,upload_convert_pdf,get_first_info,crop,get,check_file,display
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_restful import Resource, Api ,reqparse, abort
from os import walk
from jinja2 import Environment, FileSystemLoader
import json
import cv2

def get_rect(data_):
#    print(data_)
    print("jjjjjjjjjjjjjjjjjjjj================",str(data_))
    try:
        data_=json.loads(data_)
    except:
        pass
    x_start=int(data_['x'])
    y_start=int(data_['y'])
    x_end=x_start+int(data_['width'])
    y_end=y_start+int(data_['height'])
    rotate=int(data_['rotate'])
    return x_start,y_start,x_end,y_end,rotate

def get_data(path_main, name0):

    name0 = name0 + '.jpg'



    profile_ocr = {}
    profile_ocr['text'] = []
    profile_ocr['text'].append({})
    #        name="1409-004-Key-Elevation-Bank-.json"
    # path_json="./static/img/rlogo/"
    path_json = os.path.join(path_main, "rlogo/")
    # path_logo="./static/img/croped_img_300/"
    path_logo = os.path.join(path_main, "croped_img_300/")
    # path_img="./static/img/croped_img_300/"
    path_img = os.path.join(path_main, "croped_img_300/")
    path_rect = os.path.join(path_main, "croped_rect/")
#    if name0 in str(os.listdir(path_main)):
#        return path_rect + name0

    file_json = name0.replace('jpg', 'json')
    file_json = path_json + file_json
    file_logo = file_json.replace('json', 'jpg').replace('rlogo', 'croped_img')
    image = cv2.imread(file_logo)

    print(file_json)
    with open(file_json) as datafile:
        
        data = json.load(datafile)
        print("wwwwwwwwwwwwddddddddddddddddddddd=======",datafile)

    title = data['title']
    print('title   :', title)
    x_start, y_start, x_end, y_end, rotate = get_rect(title)
    img = cv2.rectangle(image, (int(x_start), int(y_start)), (int(x_end), int(y_end)), (0, 255, 0), 7)
    drawingN = data['project_number']
    x_start, y_start, x_end, y_end, rotate = get_rect(drawingN)
    img = cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 0, 255), 7)

    revsion = data['revsion']
    x_start, y_start, x_end, y_end, rotate = get_rect(revsion)
    img = cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (255, 0, 0), 7)

    cv2.imwrite(path_rect + name0, img)

    return path_rect + name0

import logging
logging.basicConfig(level=logging.DEBUG)

json_info={
    "filename":"",
    "coo_img":"",
    "title":"",
    "revsion":"",
    "price":"",
    "project_number":""
}

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/img/')


UPLOAD_FOLDER = '/tmp/flask-upload-test/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

def delet_from_drc(filename):
    try:
        os.remove("./static/img/rlogo/{}.json".format(filename))
    except FileNotFoundError:
        pass
    try:
        os.remove("./static/img/croped_img/{}.jpg".format(filename))
    except FileNotFoundError:
        pass
    try:
        os.remove("./static/img/croped_img_200/{}.jpg".format(filename))
    except:
        pass
    try:
        os.remove("./static/img/croped_rect/{}.jpg".format(filename))
    except:
        pass







class HelloWorld(Resource):
    def get(self):
        mypath = "./static/img/croped_img"
        f = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            f.extend(filenames)
            break
        template = env.get_template("img_container.html")
        output = template.render(images=f)
        if len(f) == 0:
            output = "<h1>No Images To Load</h1>"

        return {'html': output}

    def post(self):
        json_data = request.get_json(force=True)
        json_data= (json_data['src'].split('\\')[-1]).split('.')[0:-1]
        json_data=".".join(json_data)
        delet_from_drc(json_data)
        return str({"status":True})

class post(Resource):
    def post(self):
        json_data = request.get_json(force=True)



        json_data = (json_data['src'].split('/')[-1]).split('.')[0:-1]
        json_data = ".".join(json_data)

        aa = get_data(app.config['UPLOAD_FOLDER'], json_data.replace("%20"," "))




        #aa=get_data("./static/", json_data['filename'])

        return json_data


class edit_save(Resource):
    def post (self):
        json_data = request.get_json(force=True)
        
        path_json = os.path.join(app.config['UPLOAD_FOLDER'], "rlogo/",json_data["filename"].replace('.jpg','.json'))
        print("]]]]]]]]]]]]]",path_json)
        

        json_info={
            "filename":"",
            "coo_img":"",
            "title":"",
            "revsion":"",
            "price":"",
            "project_number":""
        }
        json_info["filename"]=str(json_data["filename"])
        json_info["coo_img"]=str(json_data["coo_img"])
        json_info["title"]=str(json_data["title"])
        json_info["project_number"]=str(json_data["project_number"])
        json_info["revsion"]=str(json_data["revsion"])


        
        with open(path_json, 'w') as outfile:
            json.dump(json_info, outfile)


        return json_info

api.add_resource(HelloWorld, '/hello')

api.add_resource(post, '/posts')

api.add_resource(edit_save, '/save_edit')




filename=None
@app.route('/check', methods=['GET', 'POST'])
def check():
    return check_file(app, request)

@app.route('/display')
def display_img():
    return render_template('index.html')



@app.route('/')
def first():
    return home_page()

@app.route('/second', methods=['GET', 'POST'])
def second():

    filename=upload_convert_pdf(app,request)
    json_info["filename"] = filename
    return render_template('crop_first_img.html', msg= filename)

@app.route('/third', methods=['GET', 'POST'])
def third():
    print(json_info["filename"])
    return get_first_info(app,request,json_info["filename"])


@app.route('/finish', methods=['GET', 'POST'])
def finish():
    print(get())
    json_info["coo_img"]=get()
    print(json_info["filename"])
    return crop(app,request,json_info)
img=None
infos=None
@app.route('/edit', methods = ['POST','GET'])

def edit():

    # if request.method == 'GET':
    print(request.method)

    if request.method=='GET':
        
        print("====================+++",json_data)
        return render_template('edit.html',msg=img,info=infos)


    if request.method == 'POST':
        json_data=request.form["firstname"]
        # print("====================+++",json_data)
        # return render_template('edit.html',msg=img,info=infos)
        # json_data = request.get_json(force=True)
        json_data = (json_data.split('/')[-1]).split('.')[0:-1]
        json_data = ".".join(json_data)
        img=json_data+'.jpg'
        json_data=json_data+".json"
        print("===========------------",json_data)

        path_json = os.path.join(app.config['UPLOAD_FOLDER'], "rlogo/",json_data)

        print("=====",path_json)
        import io
        file = io.open(path_json, mode="r", encoding="utf-8").read()
        file=json.loads(file)
        infos=file
        #file=json.loads(file)

        return render_template('edit.html',msg=img,info=file)









if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80,debug=True)
