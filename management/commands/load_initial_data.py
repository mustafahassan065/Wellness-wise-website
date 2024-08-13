# wellness/management/commands/load_initial_data.py
from django.core.management.base import BaseCommand
from my_app.models import Category, Topic, Resource

class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **kwargs):
        # Add categories
        mental_health = Category.objects.create(name="Mental Health")
        physical_health = Category.objects.create(name="Physical Health")
        nutrition = Category.objects.create(name="Nutrition")

        # Add topics
        stress_management = Topic.objects.create(name="Stress Management")
        exercise = Topic.objects.create(name="Exercise")
        diet = Topic.objects.create(name="Diet")
        mindfulness = Topic.objects.create(name="Mindfulness")
        sleep = Topic.objects.create(name="Sleep")
        weight_loss = Topic.objects.create(name="Weight Loss")
        mental_resilience = Topic.objects.create(name="Mental Resilience")
        hydration = Topic.objects.create(name="Hydration")

        # Add resources
        Resource.objects.create(
            title="Understanding Stress",
            description="A comprehensive guide to managing stress.",
            category=mental_health,
            topic=stress_management,
            url="https://example.com/stress"
        )

        Resource.objects.create(
            title="Effective Exercise Routines",
            description="A guide to creating effective exercise routines.",
            category=physical_health,
            topic=exercise,
            url="https://example.com/exercise"
        )

        Resource.objects.create(
            title="Healthy Eating Habits",
            description="Tips for maintaining a healthy diet.",
            category=nutrition,
            topic=diet,
            url="https://example.com/diet"
        )

        Resource.objects.create(
            title="The Importance of Mindfulness",
            description="Learn how mindfulness can improve your mental well-being.",
            category=mental_health,
            topic=mindfulness,
            url="https://example.com/mindfulness"
        )

        Resource.objects.create(
            title="Improving Your Sleep Quality",
            description="Strategies to enhance your sleep quality for better health.",
            category=physical_health,
            topic=sleep,
            url="https://example.com/sleep"
        )

        Resource.objects.create(
            title="Weight Loss Tips",
            description="Effective methods to help you achieve your weight loss goals.",
            category=nutrition,
            topic=weight_loss,
            url="https://example.com/weight_loss"
        )

        Resource.objects.create(
            title="Building Mental Resilience",
            description="Develop techniques to build mental resilience.",
            category=mental_health,
            topic=mental_resilience,
            url="https://example.com/mental_resilience"
        )

        Resource.objects.create(
            title="Staying Hydrated",
            description="The importance of hydration and tips to ensure you're drinking enough water.",
            category=physical_health,
            topic=hydration,
            url="https://example.com/hydration"
        )

        Resource.objects.create(
            title="Meditation Techniques for Stress Relief",
            description="Guided meditation techniques to help relieve stress.",
            category=mental_health,
            topic=stress_management,
            url="https://example.com/meditation"
        )

        Resource.objects.create(
            title="Nutritional Supplements",
            description="An overview of essential nutritional supplements.",
            category=nutrition,
            topic=diet,
            url="https://example.com/supplements"
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
