# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Games(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    post_season = models.TextField(blank=True, null=True)
    stadium = models.TextField(blank=True, null=True)
    team1 = models.TextField(blank=True, null=True)
    team2 = models.TextField(blank=True, null=True)
    team1_runs = models.TextField(blank=True, null=True)
    team2_runs = models.TextField(blank=True, null=True)
    team1_hits = models.TextField(blank=True, null=True)
    team2_hits = models.TextField(blank=True, null=True)
    team1_hr = models.TextField(blank=True, null=True)
    team2_hr = models.TextField(blank=True, null=True)
    winner = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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


class FindgamesGame(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    stadium = models.CharField(max_length=50)
    winner = models.CharField(max_length=50)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'findgames_game'


class FindgamesTeam1(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    team1_name = models.CharField(max_length=50)
    team1_runs = models.IntegerField()
    team1_hits = models.IntegerField()
    team1_hrs = models.IntegerField()
    home = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'findgames_team1'


class FindgamesTeam2(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    team2_name = models.CharField(max_length=50)
    team2_runs = models.IntegerField()
    team2_hits = models.IntegerField()
    team2_hrs = models.IntegerField()
    home = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'findgames_team2'

