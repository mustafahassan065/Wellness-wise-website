from django.core.management.base import BaseCommand
from .models import Resource

class Command(BaseCommand):
    help = 'Populates the database with sample resources'

    def handle(self, *args, **options):
        resources = [
            Resource(
                title="Healthy Eating for Beginners",
                category="nutrition",
                topic="general",
                content="This resource provides tips on how to start eating healthier...",
                image_url="https://your-image-url.com/healthy_eating.jpg",  # Replace with actual image URL
                external_url="https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/nutrition-basics/healthy-eating-for-a-healthy-weight/healthy-eating-for-beginners_285628"  # Replace with actual external resource URL
            ),
            Resource(
                # ... similar structure for other resources
            ),
            # ... data for 8 more resources
        ]
        Resource.objects.bulk_create(resources)  # Efficiently create multiple resources

   