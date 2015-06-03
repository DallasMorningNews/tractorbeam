#!/usr/bin/env python
from flask import Flask, request, send_from_directory, send_file, make_response, abort
from werkzeug.exceptions import HTTPException
from PIL import Image
from selenium import webdriver
import os, io, base64, six

try:
    # The typical way to import flask-cors
    from flask.ext.cors import cross_origin
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import cross_origin


app = Flask(__name__)
app.debug = False
dir = os.getcwd()


class BadURL(HTTPException):
    code = 403
    description = '<p>The submitted URL is not valid. Only http:// and https:// allowed.</p>'

class BadSelector(HTTPException):
    code = 403
    description = '<p>The submitted selector had no matches in the page in question.</p>'



@app.route("/")
def index():
    return send_file('static/index.html')

@app.route("/image/")
@cross_origin()
def generate_image():
    url = request.args['url']
    selector = request.args['selector']
    # try to open it
    driver = webdriver.PhantomJS()
    try:
    	driver.get(url)
    except:
    	raise BadURL()
    # try to find the element
    try:
    	el = driver.find_element_by_css_selector(selector)
    except:
    	raise BadSelector()
    # find the element's bounds
    loc = el.location
    size = el.size
    x1 = loc['x']
    x2 = loc['x'] + size['width']
    y1 = loc['y']
    y2 = loc['y'] + size['height']
    # generate and crop the screenshot
    imageb64 = driver.get_screenshot_as_base64()
    pngraw = base64.decodestring(imageb64)
    im = Image.open(six.BytesIO(pngraw))
    im_cropped = im.crop((x1,y1,x2,y2))
    driver.quit()
    i = six.StringIO()
    im_cropped.save(i,"png")
    i.seek(0)
    return send_file(i, attachment_filename='response.png', as_attachment=True)



if __name__ == "__main__":
	dir = os.path.dirname(__file__)
	app.debug = True
	app.run()
