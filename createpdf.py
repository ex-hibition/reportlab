from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

class CreatePDF:
    """
    PDFを出力するクラス
    ベースは公式ページのサンプルプログラム
    https://www.reportlab.com/docs/platypus-example.py
    """
    # -- 日本語フォント
    font = 'HeiseiMin-W3'
    pdfmetrics.registerFont(UnicodeCIDFont(font))

    # -- ページサイズ
    pagesize = 'A4'

    # -- 段落スタイル
    styles = getSampleStyleSheet()
    p_style = styles["Normal"]
    p_style.fontName = font

    # -- ヘッダスタイル
    h_style = styles["Heading1"]
    h_style.fontName = font
    h_style.alignment = TA_CENTER

    # -- フッタ文字列
    pageinfo = "申込内容通知"

    # -- 1ページ目
    def first_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font, 9)
        canvas.drawString(17.0 * cm, 28.5 * cm, "発行日 : yyyy年mm月dd日")
        canvas.drawString(0.5 * cm, 0.75 * cm, "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    # -- 2ページ目以降
    def later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font, 9)
        canvas.drawString(0.5 * cm, 0.75 * cm,"Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def go(self, order):
        doc = SimpleDocTemplate(f"skit_sample_{order['id']}.pdf", pagesize = A4)

        story = []

        # -- 住所情報
        address = [['', f"〒 {order['address_1']}"]
                  ,['', order['address_2']]
                  ,['', order['address_3']]
                  ,['', '']
                  ,['', f"{order['address_name']}  様"]
        ]
        t1 = Table(address, colWidths=(0.1*cm, 20*cm))
        t1.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), self.font, 9)
                               ,
        ]))
        story.append(t1)
        story.append(Spacer(1,2.0*cm))

        # -- pngロゴ
        img = Image('logo.png', hAlign='CENTER')
        story.append(img)
        story.append(Spacer(1,0.5*cm))

        # -- 資料タイトル
        h = Paragraph("ご契約内容", self.h_style)
        story.append(h)
        story.append(Spacer(1,0.5*cm))

        # -- 資料説明文
        title = 'お申込み頂いたブロードバンドサービスのプラン変更についてご案内しております。\n大切なご案内となりますので必ずご確認ください。'
        p = Paragraph(title, self.p_style)
        story.append(p)
        story.append(Spacer(1,0.5*cm))

        # -- テーブルタイトル
        p = Paragraph("■申込情報", self.p_style)
        story.append(p)
        # -- 申込情報
        details = [['ユーザID', order['id']]
                  ,['氏名', order['address_name']]
                  ,['申込日', order['order_date']]
                  ,['申込No', order['order_no']]
                  ,['申込サービス', order['order_plan']]
        ]
        t2 = Table(details, colWidths=(5*cm, 10*cm))
        t2.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), self.font, 9)
                               ,('GRID', (0, 0), (-1, -1), 0.25, colors.black)
                               ,('BACKGROUND', (0, 0), (0, -1), colors.aliceblue)
                               ,
        ]))
        story.append(t2)
        story.append(Spacer(1,0.5*cm))

        # -- グラフ
        Graph.draw_graph()
        img_graph = Image('graph.png', hAlign='CENTER')
        story.append(img_graph)
        story.append(Spacer(1,0.5*cm))

        for i in range(5):
            caution = order['quality'] * 20
            p = Paragraph(caution, self.p_style)
            story.append(p)
            story.append(Spacer(1,0.5*cm))

        doc.build(story, onFirstPage=self.first_page, onLaterPages=self.later_pages)



import pandas as pd

class Order:
    """
    申込情報クラス
    現段階では出力項目をすべて含むCSVファイルを取り込むだけ
    """
    def __init__(self, csvfile):
        self.df = pd.read_csv(csvfile)



import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

class Graph:
    """グラフを作成するクラス"""

    def draw_graph():
        fig = plt.figure()
        left = np.array(['fast month',2,3,4,5,6,7,'8-'])
        height1 = np.array([0, 1000, 1100, 1200, 1300, 1400, 1500, 2980])
        height2 = np.array([2980, 1980, 1880, 1780, 1680, 1580, 1480, 0])
        p1 = plt.bar(left, height1, color="blue")
        p2 = plt.bar(left, height2, bottom=height1, color="pink")
        plt.legend((p1[0], p2[0]), ("Sales Price", "Discount"))
        plt.title("Service Amount")
        plt.xlabel("Since")
        plt.ylabel("Amount")

        fig.savefig('graph.png')



if __name__ == "__main__":
    pdf = CreatePDF()
    # -- csvインポート
    orders = Order('./order.csv')

    for index, order in orders.df.iterrows():
        pdf.go(order)