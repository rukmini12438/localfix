import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localfix.settings')
django.setup()
from django.contrib.auth.models import User
from accounts.models import Profile
from listings.models import ServiceCategory, ServiceListing

cats = [
    ("Tutoring", "fa-graduation-cap", "#2563EB"),
    ("Electrical", "fa-bolt", "#D97706"),
    ("Plumbing", "fa-droplet", "#059669"),
    ("Carpentry", "fa-hammer", "#EA580C"),
    ("Cleaning", "fa-sparkles", "#DB2777"),
    ("Painting", "fa-paintbrush", "#7C3AED"),
]
for name, icon, color in cats:
    ServiceCategory.objects.get_or_create(name=name, defaults={"icon": icon, "color": color})

if not User.objects.filter(username="aarav").exists():
    u = User.objects.create_user("aarav", password="testpass123", first_name="Aarav", last_name="Sharma")
    Profile.objects.create(user=u, role="provider", location="Connaught Place, Delhi")
    ServiceListing.objects.create(
        provider=u, category=ServiceCategory.objects.get(name="Tutoring"),
        title="Maths & Science Tutoring", description="Experienced tutor for grades 6-12.",
        price_range="Rs 400-600/hr", location="Connaught Place, Delhi", availability="Mon-Sat, 9am-7pm"
    )

if not User.objects.filter(username="priya").exists():
    u = User.objects.create_user("priya", password="testpass123")
    Profile.objects.create(user=u, role="customer", location="Delhi")

print("seed complete")
