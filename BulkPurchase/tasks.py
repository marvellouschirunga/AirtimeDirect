# tasks.py
from celery import shared_task
import csv
from django.core.mail import EmailMessage
from .models import AirtimeRequest

@shared_task
def generate_csv_and_send_email():
    requests = AirtimeRequest.objects.filter(status='Pending')
    with open('airtime_requests.csv', 'w', newline='') as csvfile:
        fieldnames = ['phone_number', 'owner_name', 'data_bundle', 'scheduled_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for request in requests:
            writer.writerow({
                'phone_number': request.phone_number,
                'owner_name': request.owner_name,
                'data_bundle': request.data_bundle,
                'scheduled_time': request.scheduled_time,
            })
    email = EmailMessage(
        'Airtime Requests',
        'Please find the attached CSV file for the airtime requests.',
        'your_email@example.com',
        ['admin@example.com'],
    )
    email.attach_file('airtime_requests.csv')
    email.send()
    requests.update(status='Processed')