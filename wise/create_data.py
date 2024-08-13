from my_app.models import Category, Resource
from django.db import models

class Category(models.Model):
    """Model for resource categories."""
    name = models.CharField(max_length=255, unique=True)

    def _str_(self):
        return self.name
# Define Category objects outside the resources list
mindfulness_category = Category.objects.create(name="Mindfulness")
nutrition_category = Category.objects.create(name="Nutrition")
sleep_hygiene_category = Category.objects.create(name="Sleep Hygiene")
yoga_category = Category.objects.create(name="Yoga")
meditation_category = Category.objects.create(name="Meditation")
positive_psychology_category = Category.objects.create(name="Positive Psychology")
stress_management_category = Category.objects.create(name="Stress Management")
relationships_category = Category.objects.create(name="Relationships")
exercise_category = Category.objects.create(name="Exercise")

class Topic(models.Model):
    """Model for resource topics."""
    name = models.CharField(max_length=255)

    def _str_(self):
        return self.name


class Resource(models.Model):
    """Model for wellness resources."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    image_url = models.URLField(blank=True)  # Optional image URL
    categories = models.ManyToManyField(Category)
    topics = models.ManyToManyField(Topic)

    def _str_(self):
        return self.title

resources = [
    Resource(
        title="5 Easy Mindfulness Exercises for Beginners",
        description="This article explores simple mindfulness practices to help reduce stress and improve focus.",
        url="https://www.mindful.org/5-easy-mindfulness-exercises-for-beginners",
        categories=[mindfulness_category],
        topics=[Topic.objects.get_or_create(name="Stress Management")[0]]
    ),
    Resource(
        title="Healthy Eating for a Balanced Life",
        description="This website provides guidance on creating a healthy and sustainable eating plan.",
        url="https://www.eatright.org/",
        categories=[nutrition_category],
        topics=[Topic.objects.get_or_create(name="General Wellness")[0]]
    ),
    Resource(
        title="7 Tips for Getting a Better Night's Sleep",
        description="Learn effective strategies to improve your sleep quality and wake up feeling refreshed.",
        url="https://www.sleepfoundation.org/articles/7-tips-get-better-nights-sleep",
        categories=[sleep_hygiene_category],
        topics=[Topic.objects.get_or_create(name="Physical Health")[0]]
    ),
    Resource(
        title="Yoga Poses for Beginners",
        description="A visual guide to basic yoga poses that can improve flexibility, strength, and relaxation.",
        url="https://www.yogajournal.com/poses/beginner-yoga-poses",
        categories=[yoga_category],
        topics=[Topic.objects.get_or_create(name="Exercise")[0]]
    ),
    Resource(
        title="Guided Meditation for Anxiety Relief",
        description="This audio meditation helps reduce anxiety symptoms and promotes inner peace.",
        url="https://www.headspace.com/meditation/guided-meditations/letting-go-of-anxiety",
        categories=[meditation_category],
        topics=[Topic.objects.get_or_create(name="Mental Health")[0]]
    ),
    Resource(
        title="The Power of Positive Thinking",
        description="Explore the benefits of cultivating a positive mindset and practical tips for achieving it.",
        url="https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/positive-thinking/art-20043337",
        categories=[positive_psychology_category],
        topics=[Topic.objects.get_or_create(name="Mental Wellbeing")[0]]
    ),
    Resource(
        title="10 Ways to Manage Stress at Work",
        description="Discover techniques to cope with workplace stress and maintain a healthy work-life balance.",
        url="https://www.helpguide.org/articles/mental-health/workplace-stress-management.htm",
        categories=[stress_management_category],
        topics=[Topic.objects.get_or_create(name="Work-Life Balance")[0]]
    ),
    Resource(
        title="Building Healthy Relationships",
        description="Learn how to cultivate strong and supportive relationships with friends, family, and partners.",
        url="https://www.apa.org/topics/relationships/healthy-relationships",
        categories=[relationships_category],
        topics=[Topic.objects.get_or_create(name="Emotional Wellbeing")[0]]
    ),
    Resource(
        title="The Importance of Physical Activity",
        description="Understand the benefits of regular exercise for both physical and mental health.",
        url="https://www.cdc.gov/physicalactivity/basics/adult_benefits.htm",
        categories=[exercise_category],
        topics=[Topic.objects.get_or_create(name="Physical Health")[0]]
    ),
]