import uuid
import helpers
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()

class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email required"

class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming soon"
    DRAFT = "draft", "Draft"

def handle_upload(instance, filename):
    return f"{filename}"

def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"

def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"

# get_thumbnail_display_name = lambda instance: get_display_name(
#     instance, 
#     is_thumbnail=True)
    
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"]
        )
    access = models.CharField(
        max_length=14,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED
        )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # before save
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        # after save
    
    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title} - Course"
    
    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        image_options = {
            "width": 200
        }
        url = self.image.build_url(**image_options)
        return url
    
    def get_image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            # CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.image(**image_options)
        # CloudinaryImage(str(self.image)).image(**image_options)
        url = self.image.build_url(**image_options)
        return url
    
    def get_image_detail(self, as_html=False, width=750):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            # CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.image(**image_options)
        # CloudinaryImage(str(self.image)).image(**image_options)
        url = self.image.build_url(**image_options)
        return url
    
# Lesson.objects.all() # lesson queryset -> all rows
# Lesson.objects.first()
# course_obj = Course.objects.first()
# Lesson.objects.filter(course_id=course_obj.id)
# course_obj.lesson_set.all()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags = ['thumbnail', 'lesson'],
        blank=True, null=True)
    video = CloudinaryField(
        "video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        blank=True, 
        null=True, 
        tags = ['video', 'lesson'],
        resource_type="video"
        )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(
        default=False,
        help_text="If user does not have access to course, can they see this?"
        )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-updated']
        
    def save(self, *args, **kwargs):
        # before save
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        
    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
        