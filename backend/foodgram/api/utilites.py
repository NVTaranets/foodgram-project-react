from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import Recipes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import status
from rest_framework.response import Response

from .serializers import RecipesUser

# Импортируем библиотеки для формирования отчета в формате PDF
# from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle as Par_style
from reportlab.platypus import Table, TableStyle
# from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
# from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# вспомогательные объекты для формирования отчета в PDF
class MyDocTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate(
            'normal',
            [Frame(1.5 * cm, 0.5 * cm, 18 * cm, 28 * cm, id='F1')]
        )
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):  # noqa: N802
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                key = 'h1-%s' % self.seq.nextf('heading1')
                self.canv.bookmarkPage(key, fit='Fit')
                self.notify('TOCEntry', (0, text, self.page, key))
            if style == 'Heading2':
                key = 'h2-%s' % self.seq.nextf('heading2')
                self.canv.bookmarkPage(key, fit='Fit')
                self.notify('TOCEntry', (1, text, self.page, key))
        if flowable.__class__.__name__ == 'TableOfContents':
            key = 'TableOfContents'
            self.canv.bookmarkPage(key, fit='Fit')
            self.canv.addOutlineEntry("Содержание", key, 0, 0)


def add_or_delete(request, model, obj_id):
    user = request.user
    if request.method == 'DELETE':
        obj = model.objects.filter(
            user=user,
            recipes__id=obj_id
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    if model.objects.filter(
        user=user,
        recipes__id=obj_id
    ).exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(
        Recipes,
        id=obj_id
    )
    model.objects.create(
        user=user,
        recipes=recipe
    )
    serializer = RecipesUser(recipe)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


def download_page(cart_list):
    pdfmetrics.registerFont(TTFont('Times', 'times.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-Italic', 'timesi.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-BoldItalic', 'timesbi.ttf', 'UTF-8'))
    addMapping('Times', 0, 0, 'Times')    # normal
    addMapping('Times', 0, 1, 'Times-Italic')    # italic
    addMapping('Times', 1, 0, 'Times-Bold')    # bold
    addMapping('Times', 1, 1, 'Times-BoldItalic')    # italic and bold

    h1 = Par_style(
        name='Heading1',
        fontName='Times-Bold',
        fontSize=14,
        leading=16
    )

    body = Par_style('body')

    body.fontName = 'Times'

    doc = MyDocTemplate(
        'shopping_list.pdf',
        pagesize=A4,
        title="Корзина продуктов",
        autor="",
        subject=""
    )
    response = HttpResponse(doc, content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )

    stor = []
    stor.append(Paragraph('Список покупок', h1))
    t_data = [
        [f'{i}',
         ingredient['ingredients__name'],
         ingredient['amount'],
         ingredient["ingredients__measurement_unit"]
         ] for i, ingredient in enumerate(cart_list, 1)
    ]

    tabl = Table(t_data)
    tabl.setStyle(
        TableStyle(
            [('FONTNAME', (0, 0), (-1, -1), 'Times-Italic'),
             ('ALIGN', (0, 0), (0, -1),
             'RIGHT')
             ]
        )
    )
    tabl._argW[0] = 2 * cm
    tabl._argW[1] = 12 * cm
    tabl._argW[2] = 4 * cm
    tabl._argW[3] = 4 * cm
    stor.append(tabl)

    return response
