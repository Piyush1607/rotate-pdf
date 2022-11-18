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

    #checking .pdf extension
    if file.name[-4:] != '.pdf':
        return HttpResponse("please upload pdf files")
    
    file_bytes = file.read()
    # saving the uploaded file
    with open(f'/tmp/{file.name}','wb') as pdf:
        pdf.write(file_bytes)
    
    # degrees to rotate and page number
    degrees = int(req.POST['degrees'])
    page_num = int(req.POST['page']) - 1
    pdf = open(f'/tmp/{file.name}','rb')

    # pdf reader
    reader = PdfReader(pdf)

    # if page number exceeds total pages then return this response
    if page_num >= reader.numPages:
        return HttpResponse("page out of bounds")

     # if degrees is not specified then we take it 0
    if degrees is None:
        degrees = 0
    # degrees should be multiples of 90
    if degrees % 90 != 0:
        return HttpResponse("degrees must be multiples of 90")

    # pdf writer
    writer = PdfWriter()

    # looping through all pages in the pdf
    for pagenum in range(reader.numPages):
        page = reader.getPage(pagenum)
        # rotating the specified page
        if pagenum == page_num:
            page.rotateClockwise(degrees)
        # adding pages to the writer
        writer.addPage(page)

    # writing the output to a new file
    out_pdf = open(f'/tmp/{file.name}_rotated','wb')
    writer.write(out_pdf)

    # closing the opened files
    out_pdf.close()
    pdf.close()
    
    file_content = open(f'/tmp/{file.name}_rotated','rb')
    
    # displaying the rotated pages as response
    return HttpResponse(file_content.read(),content_type='application/pdf')
