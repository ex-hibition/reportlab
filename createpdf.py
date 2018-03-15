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
    this_styles = styles["Normal"]
    this_styles.fontName = "HeiseiMin-W3"

    Title = u"申込内容通知サンプル:title"
    pageinfo = u"申込内容通知サンプル:platypus example"
    
    # -- 1ページ目専用 
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('HeiseiMin-W3', 16)
        canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-30, self.Title)

        canvas.setFont('HeiseiMin-W3', 9)
        canvas.drawString(cm, 0.75 * cm,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()
    
    # -- 2ページ目以降
    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('HeiseiMin-W3', 9)
        canvas.drawString(cm, 0.75 * cm,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()
    
    def go(self, order):
        doc = SimpleDocTemplate(f"skit_sample_{order['id']}.pdf")

        story = [Spacer(1,2*cm)]
        style = self.this_styles

        p = Paragraph(order['id'], style)
        story.append(p)
        story.append(Spacer(1,0.5*cm))

        address = order['address_1'] + order['address_2'] + order['address_3'] + order['address_name']
        p = Paragraph(address, style)
        story.append(p)
        story.append(Spacer(1,0.5*cm))

        details = order['order_date'] + order['order_no'] + order['order_plan']
        p = Paragraph(details, style)
        story.append(p)
        story.append(Spacer(1,0.5*cm))

        for i in range(5):
            caution = order['quality'] * 20
            p = Paragraph(caution, style)
            story.append(p)
            story.append(Spacer(1,0.5*cm))

        doc.build(story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
    

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