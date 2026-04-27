from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_usedcode'),
    ]

    operations = [
        # add parent field to Category for subcategories
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='subcategories',
                to='store.category',
            ),
        ),
        # create the RecentlyViewed table
        # no unique_together because we delete then re-create to refresh viewed_at
        migrations.CreateModel(
            name='RecentlyViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recently_viewed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
            },
        ),
    ]
