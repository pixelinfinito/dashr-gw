# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.forms.models import model_to_dict
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import DepositTransactionModelForm
from .models import Page, DepositTransaction, RippleWalletCredentials
from .tasks import monitor_dash_to_ripple_transaction


class IndexView(TemplateView):
    """
    Index page view
    """
    template_name = 'base.html'


class GetPageDetailsView(View):
    """
    View returns given by url serialized page instance
    """
    def get(self, request, slug, **kwargs):
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

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(GetPageDetailsView, self).dispatch(*args, **kwargs)


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
        monitor_dash_to_ripple_transaction.apply_async(
            (transaction.id,),
            countdown=30,
        )
        return JsonResponse(
            {
                'success': True,
                'dash_wallet': transaction.dash_address,
                'status_url': reverse(
                    'deposit-status',
                    args=(transaction.id,),
                ),
            },
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                'success': False,
                'ripple_address_error': form.errors['ripple_address'][0],
            },
        )


class DepositStatusApiView(View):
    @staticmethod
    def get(request, transaction_id):
        transaction = get_object_or_404(DepositTransaction, id=transaction_id)
        ripple_address = RippleWalletCredentials.objects.only(
            'address',
        ).get().address
        return JsonResponse(
            {
                'transactionId': transaction.id,
                'rippleAddress': transaction.ripple_address,
                'dashAddress': transaction.dash_address,
                'state': transaction.get_state_display().format(
                    confirmations_number=settings.DASHD_MINIMAL_CONFIRMATIONS,
                    gateway_ripple_address=ripple_address,
                    **transaction.__dict__
                ),
                'stateHistory': transaction.get_state_history(),
            }
        )
