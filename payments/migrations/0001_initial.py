from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from payments.models import Subscription

def create_subscriptions(apps, schema_editor):
    Subscription = apps.get_model('payments', 'Subscription')
    subscriptions = [
        {'title': '1개월 무료', 'price': 0,},
        {'title': '1개월', 'price': 1000,},
        {'title': '3개월', 'price': 2500,},
        {'title': '6개월', 'price': 4500,},
        {'title': '1년', 'price': 8000,}
    ]
    for sub in subscriptions:
        Subscription.objects.create(title=sub['title'], price=sub['price'])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('1MF', '1 개월 무료'), ('1M', '1 개월'), ('3M', '3 개월'), ('6M', '6 개월'), ('1Y', '1 년')], max_length=50)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.RunPython(create_subscriptions),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]