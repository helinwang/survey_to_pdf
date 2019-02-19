import csv
from fpdf import FPDF
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.font_manager as mfm
prop = mfm.FontProperties(fname="kai.ttf")

import matplotlib.pyplot as plt

email_field = 'Email to be evaluated (only enter your own Email if this is a self-evaluation)'
skip_fields = {'Timestamp', 'This quiz is intended for', 'Name to be evaluated (only enter your own Email if this is a self-evaluation)', email_field}

pdf = FPDF('P', 'mm', 'Letter')
pdf.add_font('kai', '', 'kai.ttf',True)
pdf.set_font('Kai', '', 9)

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100
HEADER_HEIGHT = 15
COLUMNS = 2

def plot(x, y, question, answers):
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
    file_name = question+'.png'
    plt.savefig(file_name)
    plt.clf()
    pdf.image(file_name,x,y,IMAGE_WIDTH,IMAGE_HEIGHT)

with open('quiz.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    results = {}
    questions = []
    for question in reader.fieldnames:
        if question in skip_fields:
            continue
        questions.append(question)
        results[question] = []

    for row in reader:
        for question in questions:
            results[question].append(row[question])

    pdf.add_page()
    pdf.cell(0, 0, txt=u'测试')
    i = 0
    for question in questions:
        x = (i % COLUMNS) * IMAGE_WIDTH
        y = int(i / COLUMNS) * IMAGE_HEIGHT + HEADER_HEIGHT
        print(x, y)
        plot(x, y, question, results[question])
        i+=1
    pdf.output("pages.pdf", "F")
