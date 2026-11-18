import django.db.models.deletion
from django.db import migrations, models


def copy_event_from_seat(apps, schema_editor):
    Ticket = apps.get_model('pages', 'Ticket')
    for ticket in Ticket.objects.select_related('seat'):
        ticket.event_id = ticket.seat.event_id
        ticket.save(update_fields=['event'])


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0047_event_max_spots'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='NZD per ticket. Required if ticketed.', max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_spots',
            field=models.PositiveIntegerField(blank=True, help_text='Real cap on RSVPs (or tickets, if ticketed). Blank = unlimited.', null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='pages.event'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.RunPython(copy_event_from_seat, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='ticket',
            name='seat',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='pages.event'),
        ),
        migrations.DeleteModel(
            name='Seat',
        ),
    ]
