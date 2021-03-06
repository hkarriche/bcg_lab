# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

from datetime import datetime, timedelta

from order.models import Order

class Command(BaseCommand):
    can_import_settings = True
    help = 'Send alerts for order having a non changed status for 21 days and 31 days'
    
    def handle(self, *args, **options):
        verbose = options.get('verbosity', 0)
        
        n = datetime.now()
        
        for order in Order.objects.filter( last_change__lte = n - timedelta(21), last_change__gte = n - timedelta(22) ):
            subject = u"[BCG-Lab %s] Commande %s - statut inchangé depuis 21 jours" % (settings.SITE_NAME, order.provider.name)
            emails = []
            for username in order.orderitem_set.values_list('username', flat = True).distinct():
              user = User.objects.get(username = username)
              if user.email:
                emails.append(user.email)

            default_from = settings.DEFAULT_FROM_EMAIL
            template = loader.get_template('email_order_status.txt')
            message = template.render( Context({ 'order': order, 'days': 21 }) )
            send_mail( subject, message, default_from, emails )
        
        for order in Order.objects.filter( last_change__lte = n - timedelta(31), last_change__gte = n - timedelta(32) ):
            subject = u"[BCG-Lab %s] Commande %s - statut inchangé depuis 31 jours" % (settings.SITE_NAME, order.provider.name)
            emails = []
            for username in order.orderitem_set.values_list('username', flat = True).distinct():
              user = User.objects.get(username = username)
              if user.email:
                emails.append(user.email)

            default_from = settings.DEFAULT_FROM_EMAIL
            template = loader.get_template('email_order_status.txt')
            message = template.render( Context({ 'order': order, 'days': 31 }) )
            send_mail( subject, message, default_from, emails )


