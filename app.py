from flask import Flask, render_template, request
import csv
import pandas as pd
import os as os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def sxdindex():
    return render_template('sxdindex.html')

@app.route("/sxdupload", methods=['GET', 'POST'])
def sxdupload():
    if request.method == 'POST':
        reqFile = request.files['csvfile']
        if reqFile.filename != '':
            filename = secure_filename(reqFile.filename)
            reqFile.save(os.path.join('static', filename))
            return render_template('sxdupload.html', message="CSV file uploaded successfully.")
    return render_template('sxdupload.html')


@app.route("/sxddata", methods=['GET', 'POST'])
def sxddata():
    if request.method == 'POST':
        reqFile = request.files['csvfile']
        if reqFile.filename != '':
            reqFilename = secure_filename(reqFile.filename)
            reqFile.save(os.path.join('static', reqFilename))
            data = []
            with open(os.path.join('static', reqFilename)) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            return render_template('sxddata.html', data=data)
    return render_template('sxddata.html')



@app.route("/sxdsearchbyname", methods=['GET', 'POST'])
def sxdsearchbyname():
    return render_template('sxdsearchbyname.html')


@app.route("/sxdsearch", methods=['GET', 'POST'])
def sxdsearch():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_path = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_path = '../static/' + r['Picture']
        if temp_path != '':
            return render_template('sxdsearchbyname.html', image_path=temp_path, message="found")
        else:
            return render_template('sxdsearchbyname.html', error="Not found!")


@app.route("/sxdsal", methods=['GET', 'POST'])
def sxdsal():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for r in csv_reader:
        if r['Salary'] == '' or r['Salary'] == ' ':
            r['Salary'] = 99000;
        if int(float(r['Salary'])) < 99000:
            if r['Picture'] != ' ':
                temp_path.append('static/' + r['Picture'])
                print(temp_path)
                print(int(float(r['Salary'])))

    print(len(temp_path))
    if temp_path != '':
        return render_template('sxdsal.html', image_path=temp_path,  message="found")
    else:
        return render_template('sxdsal.html', error="Picture did not find!")


@app.route("/sxdedit", methods=['GET', 'POST'])
def sxdedit():
    return render_template('sxdedit.html')


@app.route("/sxdeditdetails", methods=['GET', 'POST'])
def sxdeditdetails():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('sxd_display.html', name=temp_name)
        else:
            return render_template('sxd_display.html', error="No Record Found!")


@app.route("/sxd_update", methods=['GET', 'POST'])
def sxd_update():
    if request.method == 'POST':
        temp_name = request.form['name']
        temp_state = request.form['state']
        temp_salary = request.form['salary']
        temp_grade = request.form['grade']
        temp_room = request.form['room']
        temp_picture = request.files['picture']  # Access the file using request.files
        temp_keyword = request.form['keyword']
        cnt = 0

        temp = [temp_name, temp_state, temp_salary, temp_grade, temp_room, temp_picture.filename, temp_keyword]  # Use picture.filename to get the filename
        lines = []

        with open('static/people.csv', 'r') as f1:
            csv_read = csv.reader(f1)
            for r in csv_read:
                if name == r[0]:
                    lines.append(temp)
                else:
                    lines.append(r)
                cnt += 1

        with open('static/people.csv', 'w') as csv_written:  # Use with open() to write to the file
            csv_writer = csv.writer(csv_written)
            csv_writer.writerows(line)

        if cnt != 0:
            return render_template('sxd_display.html', update="One Record Updated Successfully.")
        else:
            return render_template('sxd_display.html', error="No Record Found!")



@app.route("/sxdremove", methods=['GET', 'POST'])
def sxdremove():
    return render_template('sxdremove.html')

@app.route("/sxddelete", methods=['GET', 'POST'])
def sxddelete():
    if request.method == 'POST':
        reqName = request.form['name']
        cnt = 0
        lines = list()
        with open('static/people.csv', 'r') as f:
            csv_read = csv.reader(f)
            for r in csv_read:
                lines.append(r)
                if reqName == r[0]:
                    lines.remove(r)
                    cnt+=1


            csv_write = open('static/people.csv', 'w')
            for i in lines:
                for k in i:
                    csv_write.write(k + ',')
                csv_write.write('\n')

        if cnt != 0:
            return render_template('sxddelete.html', message="Record Remove Successfully.")
        else:
            return render_template('sxddelete.html', error="Record Not Found.")

@app.route("/sxdupload_pic", methods=['GET', 'POST'])
def sxdpic():
    return render_template('sxdupload_pic.html')

@app.route("/sxd_newpic", methods=['GET', 'POST'])
def sxd_newpic():
    if request.method == 'POST':
        reqFile = request.files['img']
        reqFile.save('static/'+reqFile.filename)
        return render_template('sxd_show.html', msg="Image Upload Successfully.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
