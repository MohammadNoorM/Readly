from django.contrib import admin
from reports.models import OrderReport
from store.models import Order
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
import json



@admin.register(OrderReport)
class OrderAdmin(admin.ModelAdmin):

    change_list_template = 'admin/reports/orders.html'
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, request, extra_context=None):

        yearly_stastics = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'))
            .values('year')
            .annotate(sum=Sum('transaction__amount'))
        )

        monthly_stastics = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at'))
            .values('year', 'month')
            .annotate(sum=Sum('transaction__amount'))[:30]
        )

        weekly_stastics = (
            Order.objects.select_related('transaction')
            .annotate(year=ExtractYear('created_at'), week=ExtractWeek('created_at'))
            .values('year', 'week')
            .annotate(sum=Sum('transaction__amount'))[:30]
        )

        context = {
            **self.admin_site.each_context(request),
            'yearly_stastics': json.dumps(list(yearly_stastics)),
            'monthly_stastics': json.dumps(list(monthly_stastics)),
            'weekly_stastics': json.dumps(list(weekly_stastics)),
            'title': _('Order Reports'),
        }
        

        return TemplateResponse(request, self.change_list_template, context)