# -*- coding: utf-8 -*-

import logging
from io import StringIO

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.core.management import call_command

from intranet.db.ldap_db import LDAPConnection

from cacheops import invalidate_obj

from ....auth.decorators import eighth_admin_required
from ....users.models import User

logger = logging.getLogger(__name__)


@eighth_admin_required
def index_view(request):
    context = {
        "admin_page_title": "Maintenance Tools"
    }
    return render(request, "eighth/admin/maintenance.html", context)


@eighth_admin_required
def teacher_management(request):
    context = {
        "admin_page_title": "Teacher Management",
        "fields": ["iodineUid", "iodineUidNumber", "cn", "sn", "givenName", "mail"],
        "advanced_fields": ["dn", "objectClass", "header", "style", "mailentries", "chrome", "startpage"]
    }
    return render(request, "eighth/admin/teacher_management.html", context)


@eighth_admin_required
def teacher_modify(request):
    # TODO: implement teacher create/modify
    return JsonResponse({"success": False})


@eighth_admin_required
def teacher_delete(request):
    dn = request.POST.get("dn", None)
    if request.method == "POST" and dn and settings.USER_DN in dn:
        c = LDAPConnection()
        c.conn.delete(dn)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@eighth_admin_required
def teacher_list(request):
    c = LDAPConnection()
    usrid = request.GET.get("id", None)
    if usrid:
        data = c.search(settings.USER_DN, "iodineUid={}".format(usrid), ["*"])
        if len(data) == 0:
            return JsonResponse({"teacher": None})
        teacher = {x: y[0] for x, y in data[0]["attributes"].items()}
        teacher["dn"] = data[0]["dn"]
        return JsonResponse({"teacher": teacher})
    else:
        data = c.search(settings.USER_DN, "objectClass=tjhsstTeacher", ["iodineUid", "cn"])
        teachers = [{"id": x["attributes"]["iodineUid"][0], "name": x["attributes"]["cn"][0]} for x in data]
        return JsonResponse({"teachers": teachers})


@eighth_admin_required
def sis_import(request):
    context = {
        "admin_page_title": "SIS Import"
    }
    # TODO: implement sis import
    return render(request, "eighth/admin/sis_import.html", context)


@eighth_admin_required
def start_of_year_view(request):
    context = {
        "admin_page_title": "Start of Year Operations",
        "completed": False
    }
    if request.method == "POST" and request.POST.get("confirm"):
        content = StringIO()
        call_command("year_cleanup", run=True, confirm=True, stdout=content)
        content.seek(0)
        context["output"] = content.read()
        context["completed"] = True
    return render(request, "eighth/admin/start_of_year.html", context)


@eighth_admin_required
def clear_comments_view(request):
    context = {
        "admin_page_title": "Clear Admin Comments",
        "completed": False
    }
    if request.method == "POST" and request.POST.get("confirm"):
        deleted_comments = ""
        count = 0

        c = LDAPConnection()
        comments = c.search(settings.USER_DN, "objectClass=tjhsstStudent", ["eighthoffice-comments", "dn"])
        for row in comments:
            if "eighthoffice-comments" in row:
                c.del_attribute(row["dn"], "eighthoffice-comments")
                u = User.objects.get(dn=row["dn"])
                invalidate_obj(u)
                u.clear_cache()
                deleted_comments += "=== {} ({})\n{}\n".format(u.full_name, u.username, row["eighthoffice-comments"])
                count += 1

        context["deleted_comments"] = deleted_comments or "No comments were deleted."
        context["deleted_comments_count"] = count
        context["completed"] = True
    return render(request, "eighth/admin/clear_comments.html", context)
