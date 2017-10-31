# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.models import model_to_dict
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.shortcuts import render

from .forms import DepositTransactionModelForm
from .models import Page


class IndexView(TemplateView):
    """
    Index page view
    """
    template_name = 'base.html'


class GetPageDetailsView(View):
    """
    View returns given by url serialized page instance
    """
    def get(self, request, slug):
        if request.is_ajax():
            ctx = {'page': [], 'success': True}
            page = Page.objects.filter(slug=slug)

            if not page.exists():
                ctx['success'] = False
                ctx['message'] = 'Page does not exists'
            else:
                ctx['page'] = model_to_dict(page[0])

            return JsonResponse(ctx, safe=False)
        return render(request, 'base.html')


class DepositSubmitApiView(View, FormMixin):
    form_class = DepositTransactionModelForm

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        transaction = form.save()
        return JsonResponse(
            {
                'success': True,
                'dash_wallet': transaction.dash_address,
                'status_url': '/status/{}/'.format(transaction.id),
            },
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'success': False,
                'ripple_address_error': form.errors['ripple_address'][0],
            },
        )
