import io

import xlsxwriter
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from business import models
from business import forms


# Create your views here.
def lk(request):
    return render(template_name='lk.html', request=request)


def business_company_info(request):
    forms_counts = ['Первый', 'Второй', 'Третий']
    forms_render = [forms.CompanyWorkerForm() for _ in range(len(forms_counts))]

    form_region = forms.CompanyRegionForm()

    if request.method == 'POST':
        forms_render = [
            forms.CompanyWorkerForm({'position': position}) for position in request.POST.getlist('position')]
        form_region = forms.CompanyRegionForm(request.POST)
        if all(form.is_valid() for form in forms_render) and form_region.is_valid():
            company = request.user.company
            company.companyworker_set.all().delete()

            for company_worker_form in forms_render:
                worker = company_worker_form.instance
                worker.company = company

                worker.save()

            return redirect(f'/find_business_center/?region={form_region.data["region"]}')

    company_worker_forms = zip(forms_counts, forms_render)
    return render(template_name='business_company_info.html', request=request,
                  context={'company_worker_class': models.CompanyWorker,
                           'business_center_class': models.BusinessCenter,
                           'company_worker_forms': company_worker_forms,
                           'form_region': form_region})


def find_business_center(request):
    region = int(request.GET['region'])
    business_centers = models.BusinessCenter.objects.filter(region=region).all()

    return render(template_name='find_business_center.html', request=request,
                  context={'business_centers': business_centers})


def set_office_in_bs(request):
    business_center_id = int(request.GET['business_center_id'])
    offices = models.BusinessCenterOffice.objects.filter(business_center_id=business_center_id).all()

    if request.method == 'POST':
        office_id = request.POST['office_id']

        company = request.user.company

        models.BusinessCenterOfficeToCompany.objects.filter(company=company).all().delete()

        company_to_office = models.BusinessCenterOfficeToCompany()
        company_to_office.company = company
        company_to_office.offices_id = office_id
        company_to_office.save()

        return redirect('/select_pc')

    return render(template_name='set_office_in_bs.html', request=request, context={'offices': offices})


def select_pc(request):
    company = request.user.company
    positions = models.CompanyWorker.objects.filter(company=company).values_list('position').distinct().all()
    things = models.Things.objects.filter(type=models.Things.PC, for_position__in=positions).all()

    if request.method == 'POST':
        thing_id = request.POST['thing_id']

        thing_to_company = models.ThingToCompany()
        thing_to_company.company = company
        thing_to_company.thing_id = thing_id

        thing_to_company.save()

    return render(template_name='select_pc.html', request=request,
                  context={'things': things, 'positions_types': dict(models.Things.POSITION_CHOICES)})


@transaction.atomic
def cart_show(request):
    company = request.user.company
    offices = [_.offices for _ in company.businesscenterofficetocompany_set.select_related('offices').all()]
    things = [_.thing for _ in company.thingtocompany_set.select_related('thing').all()]

    check = {
        'sum': sum(map(lambda _: _.price, offices)) + sum(map(lambda _: _.price, things)),
        'count': len(offices) + len(things)
    }

    if request.method == 'POST' and not company.is_init:
        order = models.Order()
        order.company = company

        order.save()

        for office in offices:
            order_to_office = models.OfficesToOrder()
            order_to_office.order = order
            order_to_office.office = office

            order_to_office.save()

        for thing in things:
            order_to_things = models.ThingsToOrder()
            order_to_things.order = order
            order_to_things.things = thing

            order_to_things.save()

        company.is_init = True
        company.save()

    order = models.Order.objects.filter(company=company).first()

    if not order:
        order = models.Order()
        order.status = models.Order.NOT_READY

    return render(template_name='cart_show.html', request=request,
                  context={'offices': offices, 'things': things, 'check': check,
                           'order_status': dict(models.Order.STATUS_CHOICES)[order.status]}, )


def excel_dump(request):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # data = get_simple_table_data()
    #
    # # Write some test data.
    # for row_num, columns in enumerate(data):
    #     for col_num, cell_data in enumerate(columns):
    #         worksheet.write(row_num, col_num, cell_data)

    workbook.close()

    output.seek(0)

    filename = 'Order.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
