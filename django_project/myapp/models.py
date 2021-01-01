from django.db import models
from django.contrib.auth.models import User #추가

# Create your models here.
"""
class Post(models.Model):
  # 모델 클래스 명은 단수로
    user = models.ForeignKey(User, on_delete=models.CASCADE)
      # 왜래키 (장고에서 기본 제공하는 User 모델과 M:1 관계)
    title = models.CharField(max_length=144)
      # 길이제한 144자
    subtitle = models.CharField(blank=True, null=True)
      # Application단 null OK, DB단 null OK
    content = models.TextField()
      # 기본 TextField
    created_at = models.DateTimeField(auto_now_add=True)
      # 해당 레코드 생성시 현재 시간 자동 저장
    def __str__(self):
      # 해당 모델 인스턴스를 str형으로 캐스팅 시의 리턴을 정의
        return '[{}] {}'.format(self.user.username, self.title)
          # ex) "[] 제목입니다."
"""


class AuthGroup(models.Model):
  name = models.CharField(unique=True, max_length=80)

  class Meta:
    managed = False
    db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
  group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
  permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_group_permissions'
    unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
  name = models.CharField(max_length=255)
  content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
  codename = models.CharField(max_length=100)

  class Meta:
    managed = False
    db_table = 'auth_permission'
    unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
  password = models.CharField(max_length=128)
  last_login = models.DateTimeField(blank=True, null=True)
  is_superuser = models.IntegerField()
  username = models.CharField(unique=True, max_length=150)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=150)
  email = models.CharField(max_length=254)
  is_staff = models.IntegerField()
  is_active = models.IntegerField()
  date_joined = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'auth_user'


class AuthUserGroups(models.Model):
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)
  group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_user_groups'
    unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)
  permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_user_user_permissions'
    unique_together = (('user', 'permission'),)


class Benefits(models.Model):
  id = models.IntegerField(primary_key=True)
  conv_type = models.CharField(max_length=10)
  b_type = models.CharField(max_length=15)
  b_name = models.CharField(max_length=30)
  b_ex = models.CharField(max_length=150, blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'benefits'


class DjangoAdminLog(models.Model):
  action_time = models.DateTimeField()
  object_id = models.TextField(blank=True, null=True)
  object_repr = models.CharField(max_length=200)
  action_flag = models.PositiveSmallIntegerField()
  change_message = models.TextField()
  content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'django_admin_log'


class DjangoContentType(models.Model):
  app_label = models.CharField(max_length=100)
  model = models.CharField(max_length=100)

  class Meta:
    managed = False
    db_table = 'django_content_type'
    unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
  app = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  applied = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'django_migrations'


class DjangoSession(models.Model):
  session_key = models.CharField(primary_key=True, max_length=40)
  session_data = models.TextField()
  expire_date = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'django_session'


class Post(models.Model):
  title = models.CharField(max_length=200)
  date = models.DateTimeField('date published')
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  image = models.ImageField(upload_to='media/',blank=True)
  def __str__(self):
    return self.title

#upload_to="%Y/%m/%d"
"""
class Photo(models.Model):
  #post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
  post = models.CharField(max_length=200)
  image = models.ImageField(upload_to='media/',blank=True, null=True)
"""
class Photo(models.Model):
  title = models.CharField(max_length=255, blank=True)
  image = models.ImageField(upload_to='media/')
  uploaded = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = False
    db_table = 'Photo'

class Qrcode(models.Model):
  title = models.CharField(max_length=255, blank=True)
  prod_name = models.CharField(max_length=100, blank=True)

  class Meta:
    managed = False
    db_table = 'Qrcode'

 # class Meta:
  #  managed = False
  # db_table = 'media_photos'



app_label = 'membership'