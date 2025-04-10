from django.db import models

"""
- Courses:
	- Title
	- Description
	- Thumbnail/Image
	- Access:
		- Anyone
		- Email required
        - Purchase required
		- User required (n/a)
	- Status: 
		- Published
		- Coming Soon
		- Draft
"""

class AccessRequirements(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email required"
    
class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming soon"
    DRAFT = "draft", "Draft"

class Course(models.Model):
    pass
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # image
    access = models.CharField(
        max_length=10,
        choices=AccessRequirements.choices,
        default=AccessRequirements.DRAFT
        )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
        )
    
    @ property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

"""
    - Lessons
    - Title
    - Description
    - Video
    - Status: Published, Coming Soon, Draft
"""
