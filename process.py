import csv
from fpdf import FPDF
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.font_manager as mfm
prop = mfm.FontProperties(fname="kai.ttf")

import matplotlib.pyplot as plt

email_field = 'Email to be evaluated (only enter your own Email if this is a self-evaluation)'
name_field = 'Name to be evaluated (only enter your own Email if this is a self-evaluation)'
intend_for_field = 'This quiz is intended for'
skip_fields = {'Timestamp', intend_for_field, email_field, name_field}

pdf = FPDF('P', 'mm', 'Letter')
pdf.add_font('kai', '', 'kai.ttf',True)
pdf.set_font('Kai', '', 9)

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100
HEADER_HEIGHT = 15
STR_HEIGHT = 10
STR_X = 10
COLUMNS = 2

def plot(x, y, question, answers, name):
    d = {}
    for ans in answers:
        if ans not in d:
            d[ans] = 0
        d[ans] += 1

    names = []
    counts = []
    for name, count in d.items():
        names.append(name)
        counts.append(count)

    _, texts, _ = plt.pie(counts,labels=names,autopct='%1.1f%%')
    plt.text(-0.8, 1.2, question, fontproperties=prop)
    plt.axis('equal')
    plt.setp(texts, fontproperties=prop)
    file_name = name+str(x)+'.'+str(y)+'.png'
    plt.savefig(file_name)
    plt.clf()
    pdf.image(file_name,x,y,IMAGE_WIDTH,IMAGE_HEIGHT)


def persons(rows):
    ps = {}
    for row in rows:
        email = row[email_field].lower()
        if email not in ps:
            ps[email] = []
        ps[email].append(row)
    ret = []

    for _, v in ps.items():
        ret.append(v)
    return ret

def print_person(questions, name, rows):
    results = {}
    feedbacks_from_other = 0
    for row in rows:
        if row[intend_for_field].lower() == "myself":
            continue

        feedbacks_from_other += 1
        for question in questions:
            if question not in results:
                results[question] = []
            results[question].append(row[question])

    pdf.add_page()
    pdf.cell(0, 0, txt=name+', '+str(feedbacks_from_other) + " feedbacks from others")
    i = 0

    last_y = 0
    for question in questions:
        x = (i % COLUMNS) * IMAGE_WIDTH
        y = int(i / COLUMNS) * IMAGE_HEIGHT + HEADER_HEIGHT
        plot(x, y, question, results[question], name)
        i+=1
        last_y = y

    y = last_y + IMAGE_HEIGHT
    for row in rows:
        line = row[intend_for_field] + ", "
        for question in questions:
            line += row[question] + ", "
        pdf.text(STR_X, y, txt=line)
        y += STR_HEIGHT


with open('quiz.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    questions = []
    for question in reader.fieldnames:
        if question in skip_fields:
            continue
        questions.append(question)

    rows = []
    for row in reader:
        rows.append(row)

    ps = persons(rows)
    for prs in ps:
        print_person(questions, prs[0][name_field], prs)

    pdf.output("pages.pdf", "F")
