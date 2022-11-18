from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from PyPDF2 import PdfReader, PdfWriter
# Create your views here.


@api_view(['GET','POST'])
def rotatePDF(req):
    if req.method == 'GET':
        return render(req,'upload.html')

    file = req.FILES['file']

    if file.name[-4:] != '.pdf':
        return HttpResponse("please upload pdf files")
    
    file_bytes = file.read()

    with open(f'/tmp/{file.name}','wb') as pdf:
        pdf.write(file_bytes)
    
    degrees = int(req.POST['degrees'])
    page_num = int(req.POST['page']) - 1
    pdf = open(f'/tmp/{file.name}','rb')

    reader = PdfReader(pdf)
    if page_num >= reader.numPages:
        return HttpResponse("page out of bounds")

    if degrees % 90 != 0:
        return HttpResponse("degrees must be multiples of 90")

    writer = PdfWriter()

    if degrees is None:
        degrees = 0

    for pagenum in range(reader.numPages):
        page = reader.getPage(pagenum)
        if pagenum == page_num:
            page.rotateClockwise(degrees)
        writer.addPage(page)

    out_pdf = open(f'/tmp/{file.name}_rotated','wb')
    writer.write(out_pdf)
    out_pdf.close()
    pdf.close()
    
    file_content = open(f'/tmp/{file.name}_rotated','rb')
    
    return HttpResponse(file_content.read(),content_type='application/pdf')