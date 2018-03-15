# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

class CreatePDF:
    """
    PDFを出力するクラス
    ベースは公式ページのサンプルプログラム
    https://www.reportlab.com/docs/platypus-example.py
    """
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()
    
    Title = u"申込内容通知サンプル:title"
    pageinfo = u"申込内容通知サンプル:platypus example"
    
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('HeiseiMin-W3', 16)
        canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-30, self.Title)

        canvas.setFont('HeiseiMin-W3', 9)



        canvas.setFont('HeiseiMin-W3', 9)
        canvas.drawString(cm, 0.75 * cm,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()
    
    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('HeiseiMin-W3', 9)
        canvas.drawString(cm, 0.75 * cm,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()
    
    def go(self, order):
        doc = SimpleDocTemplate(f"skit_sample_{order['id']}.pdf")
        Story = [Spacer(1,2*cm)]
        style = self.styles["Normal"]
        for i in range(100):
            p = Paragraph(order['id'], style)
            Story.append(p)
            Story.append(Spacer(1,0.2*cm))

            address = order['address_1'] + order['address_2'] + order['address_3']
            p = Paragraph(unicode(address, 'utf-8'), style)
            Story.append(p)
            Story.append(Spacer(1,0.2*cm))

            bogustext = ("Paragraph number %s. " % i) *5
            p = Paragraph(bogustext, style)
            Story.append(p)
            Story.append(Spacer(1,0.2*cm))

        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
    

import pandas as pd

class Order:
    """
    申込情報クラス
    現段階では出力項目をすべて含むCSVファイルを取り込むだけ
    """
    def __init__(self, csvfile):
        self.df = pd.read_csv(csvfile) 


if __name__ == "__main__":
    pdf = CreatePDF()
    orders = Order('./order.csv')

    for index, order in orders.df.iterrows():
        pdf.go(order)