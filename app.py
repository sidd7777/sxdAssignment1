from flask import Flask, render_template, request
import csv
import pandas as pd
import os as os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def sxdindex():
    return render_template("sxdindex.html")


@app.route("/sxddata", methods=["GET", "POST"])
def sxddata():
    if request.method == "POST":
        reqFile = request.files["csvfile"]
        if reqFile.filename != "":
            reqFilename = secure_filename(reqFile.filename)
            reqFile.save(os.path.join("static", reqFilename))
            data = []
            with open(os.path.join("static", reqFilename)) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            return render_template("sxddata.html", data=data)
    return render_template("sxddata.html")


@app.route("/sxdsearchbyname", methods=["GET", "POST"])
def sxdsearchbyname():
    return render_template("sxdsearchbyname.html")


@app.route("/sxdsearch", methods=["GET", "POST"])
def sxdsearch():
    if request.method == "POST":
        row = request.form["name"]
        csv_reader = csv.DictReader(open("static/q1c.csv"))
        temp_path = ""
        seat = 0
        for r in csv_reader:
            if row == r["row"]:
                temp_path = "../newQuiz1/static/" + r["pic"]
                seat = r["seat"]
                name = r["name"]

        if temp_path != "":
            return render_template(
                "sxdsearchbyname.html",
                image_path=temp_path,
                name=name,
                seat=seat,
                message="found",
            )
        else:
            return render_template("sxdsearchbyname.html", error="Not found!")


@app.route("/sxdedit", methods=["GET", "POST"])
def sxdedit():
    return render_template("sxdedit.html")


@app.route("/sxdeditdetails", methods=["GET", "POST"])
def sxdeditdetails():
    if request.method == "POST":
        name = request.form["name"]
        csv_reader = csv.DictReader(open("static/q1c.csv"))
        temp_name = ""
        for r in csv_reader:
            if name == r["name"]:
                temp_name = name
        print(temp_name)
        if temp_name != "":
            return render_template("sxd_display.html", name=temp_name)
        else:
            return render_template("sxd_display.html", error="No Record Found!")


@app.route("/sxdadd", methods=["GET"])
def sxd_add():
    return render_template("sxd_add.html")


@app.route("/sxdadd", methods=["POST"])
def sxdadd():
    temp_name = request.form["name"]
    temp_picture = request.files["pic"]  # Access the file using request.files
    temp_seat = request.form["seat"]
    temp_row = request.form["row"]
    temp_notes = request.form["notes"]

    temp = [
        temp_name,
        temp_picture.filename,
        temp_seat,
        temp_row,
        temp_notes,
    ]  # Use picture.filename to get the filename

    with open("static/q1c.csv", "a") as csv_file:  # Use 'a' to append to the file
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(temp)

    return render_template("sxd_show.html", msg="User Added Successfully.")


@app.route("/sxd_update", methods=["GET", "POST"])
def sxd_update():
    if request.method == "POST":
        temp_name = request.form["name"]
        temp_picture = request.files["pic"]  # Access the file using request.files
        temp_seat = request.form["seat"]
        temp_row = request.form["row"]
        temp_notes = request.form["notes"]
        cnt = 0

        temp = [
            temp_name,
            temp_picture.filename,
            temp_notes,
            temp_row,
            temp_seat,
        ]  # Use picture.filename to get the filename
        lines = []

        with open("static/q1c.csv", "r") as f1:
            csv_read = csv.reader(f1)
            for r in csv_read:
                if len(r) > 0 and temp_name == r[0]:
                    lines.append(temp)
                else:
                    lines.append(r)
                cnt += 1
        print(cnt)

        with open(
            "static/q1c.csv", "w"
        ) as csv_written:  # Use with open() to write to the file
            csv_writer = csv.writer(csv_written)
            csv_writer.writerows(lines)

        if cnt != 0:
            return render_template(
                "sxd_display.html", update="One Record Updated Successfully."
            )
        else:
            return render_template("sxd_display.html", error="No Record Found!")


@app.route("/range", methods=["GET", "POST"])
def range_view():
    if request.method == "POST":
        r1 = request.form["r1"]
        r2 = request.form["r2"]
        csv_reader = csv.DictReader(open("static/q1c.csv"))
        temp_path = ""
        temp_name = ""
        temp_notes = ""
        temp_seat = ""
        temp_row = ""
        count = 0
        for r in csv_reader:
            if r1 <= r["row"] and r2 >= r["row"]:
                count += 1
                temp_notes = r["notes"]
                temp_path = "../newQuiz1/static/" + r["pic"]
                temp_name = r["name"]
                temp_seat = r["seat"]
                temp_row = r["row"]
        if count == 0:
            return render_template("grade.html", error="no data found")
        else:
            return render_template(
                "grade.html",
                image_path=temp_path,
                name=temp_name,
                seat=temp_seat,
                row=temp_row,
                count=count,
                notes=temp_notes,
                message="found",
            )
    else:
        # Handle the GET request
        return render_template("grade.html")


@app.route("/sxdremove", methods=["GET", "POST"])
def sxdremove():
    return render_template("sxdremove.html")


@app.route("/sxddelete", methods=["GET", "POST"])
def sxddelete():
    if request.method == "POST":
        reqName = request.form["name"]
        cnt = 0
        lines = list()
        with open("static/q1c.csv", "r") as f:
            csv_read = csv.reader(f)
            for r in csv_read:
                lines.append(r)
                if reqName == r[0]:
                    lines.remove(r)
                    cnt += 1

            csv_write = open("static/q1c.csv", "w")
            for i in lines:
                for k in i:
                    csv_write.write(k + ",")
                csv_write.write("\n")

        if cnt != 0:
            return render_template(
                "sxddelete.html", message="Record Remove Successfully."
            )
        else:
            return render_template("sxddelete.html", error="Record Not Found.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
