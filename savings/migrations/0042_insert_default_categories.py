from django.db import migrations
from django.contrib.auth import get_user_model
from savings.models import Category

def insert_default_categories(apps, schema_editor):
    User = get_user_model()

    # Asegúrate de que el primer usuario exista, o crea uno si no lo hay
    try:
        user = User.objects.first()  # Usa el manager de objetos de User
    except User.DoesNotExist:
        user = None

    if not user:
        # Si no hay un usuario, crea uno
        user = User.objects.create_user(
            email="admin@zenkoo.com",
            password="adminpassword",  # O cualquier password predeterminado
            first_name="Admin",
            last_name="User"
        )

    # Categorías predeterminadas
    categories = ["Supervivencia", "Ocio y vicio", "Cultura", "Extras"]

    # Crear categorías si no existen
    for category_name in categories:
        Category.objects.get_or_create(name=category_name, type="expense", user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0041_alter_monthlyplan_reflection'),  # Si esta dependencia no existe, puedes eliminarla
    ]

    operations = [
        migrations.RunPython(insert_default_categories),
    ]