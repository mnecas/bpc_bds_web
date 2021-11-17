# Generated by Django 3.2.9 on 2021-11-17 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=45)),
                ('street', models.CharField(max_length=45)),
                ('street_number', models.IntegerField()),
                ('zip', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arival', models.DateTimeField(auto_now_add=True)),
                ('delivery_fee', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('passowrd', models.CharField(max_length=45)),
                ('username', models.CharField(max_length=45)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.address')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.dish')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('drivers', models.ManyToManyField(to='main.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField()),
                ('text', models.TextField(max_length=500)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_driver', to='main.person')),
                ('restaurant_dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.restaurantdish')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='dishes',
            field=models.ManyToManyField(through='main.RestaurantDish', to='main.Dish'),
        ),
        migrations.AddField(
            model_name='person',
            name='person_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.persontype'),
        ),
        migrations.CreateModel(
            name='DeliveryDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirements', models.TextField(max_length=200)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.delivery')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.restaurantdish')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='dishes',
            field=models.ManyToManyField(through='main.DeliveryDish', to='main.RestaurantDish'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='main.person'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=45)),
                ('value', models.CharField(max_length=45)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=45)),
                ('type', models.CharField(max_length=45)),
                ('brand', models.CharField(max_length=45)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='persons',
            field=models.ManyToManyField(to='main.Person'),
        ),
    ]
