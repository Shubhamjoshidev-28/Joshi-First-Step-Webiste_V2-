from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatReplyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('session_key', models.CharField(blank=True, max_length=64)),
                ('user_message', models.TextField(blank=True)),
                ('bot_reply', models.TextField()),
                ('match_source', models.CharField(default='fallback', max_length=30)),
                ('confidence', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
