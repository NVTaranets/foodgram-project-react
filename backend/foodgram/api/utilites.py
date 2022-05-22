import os

from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import Recipes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import status
from rest_framework.response import Response
from wsgiref.util import FileWrapper

from .serializers import RecipesUser
from foodgram.settings import FONT_ROOT

# Импортируем библиотеки для формирования отчета в формате PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import ParagraphStyle as PS  # noqa: N817
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
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
            [Frame(1.5 * cm, 0.5 * cm, 18 * cm, 28 * cm, id='F1')])
        self.addPageTemplates(template)


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
    pdfmetrics.registerFont(
        TTFont(
            'Times',
            os.path.join(FONT_ROOT, 'times.ttf'),
            'UTF-8'
        )
    )

    addMapping('Times', 0, 0, 'Times')    # normal

    h1 = PS(
        name='Heading1',
        fontName='Times',
        fontSize=24,
        leading=34,

    )

    body = PS('body')

    body.fontName = 'Times'

    newfile = NamedTemporaryFile(suffix='.pdf')

    doc = MyDocTemplate(
        newfile.name,
        pagesize=A4,
        title="Корзина продуктов",
        autor="",
        subject=""
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
    t_data = [
        ['№ п.п.',
         'Наименование продукта',
         'Количество',
         'Ед.изм.'
         ],
    ] + t_data
    tabl = Table(t_data)
    tabl.setStyle(
        TableStyle(
            [('FONTNAME', (0, 0), (-1, -1), 'Times'),
             ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.8, colors.black),
             ('BOX', (0, 0), (-1, 0), 0.8, colors.black),
             ]
        )
    )
    tabl._argW[0] = 2 * cm
    tabl._argW[1] = 10 * cm
    tabl._argW[2] = 3 * cm
    tabl._argW[3] = 3 * cm
    stor.append(tabl)
    stor.append(Paragraph('', body))
    stor.append(Paragraph('Спасибо за использование сервиса :)!!!', body))
    doc.multiBuild(stor)

    response = HttpResponse(
        FileWrapper(newfile),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )

    return response
