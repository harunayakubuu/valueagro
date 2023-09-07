from django.shortcuts import render
from django.http import HttpResponse
from contacts.models import Contact

import xlwt

# Import for PDF redering
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.db.models import Sum
# import tempfile
import datetime


# def invoice_pdf(request):
    
#     response = HttpResponse(content_type = "application/pdf")
#     response['Content-Disposition'] = 'inline; attachment; filename=Contact_Messages'+str(datetime.datetime.now())+".pdf"
#     response['Content-Transfer-Encoding'] = "binary"

#     contact_messages = Contact.objects.all()

#     html_string = render_to_string(
#         "invoices/contact_messages.html",
#         {
#             'msgs': contact_messages,
#             'total': 0
#         }
#     )

#     html = HTML(string = html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete = True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb') # r for reading, b - binary
#         response.write(output.read())
#     return response


def export_excel(request):
    
    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Contact Messages '+str(datetime.date.today())+".xls"

    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet("Contacts Messages")

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Email', 'Phone Number', 'Subject', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Contact.objects.all().values_list('name', 'email', 'phone', 'subject', 'status', 'created_at')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)
    return response