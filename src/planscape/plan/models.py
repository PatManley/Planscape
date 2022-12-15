from django.contrib.auth.models import User
from django.contrib.gis.db import models

import math 

class Plan(models.Model):
    """
    A Plan is associated with one User, the owner, and one Region.  It has a name,
    status (locked/public), and a geometry representing the planning area.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # type: ignore

    # The name of the plan.
    name: models.CharField = models.CharField(max_length=120)

    # The region_name for the plan; should be one of the valid region names in base.region_names.
    region_name: models.CharField = models.CharField(max_length=120)

    # Whether the plan has been made "public".
    public: models.BooleanField = models.BooleanField(null=True, default=False)

    # Whether the plan has been "locked".
    locked: models.BooleanField = models.BooleanField(null=True, default=False)

    # The planning area of the plan.
    geometry = models.MultiPolygonField(srid=4269, null=True)

class Project(models.Model): 
    """
    A Project is associated with one User, the owner, and one Plan. It has optional user-specified
    project parameters, e.g. constraints.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE) 

    # Project Parameters:

    # The maximum cost constraint. Default set to no max cost.
    max_cost = models.IntegerField(null=True, default=math.inf) 

    #min_acres_treated 

    #permitted_ownership = (1=federal, 2=state, 4=private) 

class GeneratedProjectAreas(models.Model): 
    """
    GeneratedProjectAreas are associated with one Project. It has geometries representing 
    the project area, and an estimate of the area treated.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 

    # The project area geometries. May be one or more polygons that represent the project area.
    project_area = models.MultiPolygonField(srid=4269, null=True) 

    # The sum total of the project area areas.
    estimated_area_treated = models.IntegerField(null=True) 

class Scenario(models.Model):
    """
    A Scenario is associated with one User, the owner, and one Project. It has optional user-specified
    prioritization parameters.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
