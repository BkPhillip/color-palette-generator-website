import os
from app import app
import urllib.request
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
import colorgram


ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}


def allowed_file(filename):\
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        colors = colorgram.extract('static/uploads/' + filename, 10)
        colors_rgb_tuple = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
        colors_hex = ['%2x%02x%02x' % rgb for rgb in colors_rgb_tuple]
        rounded_color_proportions = [round(color.proportion, 6) for color in colors]
        return render_template('index.html',
                               filename=filename,
                               colors=colors,
                               colors_hex=colors_hex,
                               rounded_color_proportions=rounded_color_proportions,
                               number_of_colors=len(colors))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
