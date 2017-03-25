# coding=utf-8

"""
DCRM - Darwin Cydia Repository Manager
Copyright (C) 2017  WU Zheng <i.82@me.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Notice: You have used class-based views, that's awesome.
        If not necessary, you can try function-based views.
        You may add lines above as license.
"""

from django.views.generic import ListView
from WEIPDCRM.models.package import Package
from WEIPDCRM.models.section import Section

from preferences import preferences
from django.utils.translation import ugettext_lazy as _

class SectionView(ListView):
    allow_empty = True
    paginate_by = 24
    ordering = '-id'
    model = Package
    context_object_name = 'package_list'
    pk_url_kwarg = 'section_id'
    template_name = 'frontend/section.html'

    def get(self, request, *args, **kwargs):
        if request.META['HTTP_USER_AGENT'].lower().find('mobile') > 0:
            self.template_name = 'mobile/section.html'
        return super(SectionView, self).get(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Get Package from specific section.

        :return: QuerySet
        """
        section_id = self.kwargs.get('section_id')
        queryset = super(SectionView, self).get_queryset().filter(c_section__id=section_id)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Merge global settings to current context
        """
        section_id = self.kwargs.get('section_id')
        packages_num = Package.objects.filter(c_section_id=section_id).count()
        context = super(SectionView, self).get_context_data(**kwargs)
        context['settings'] = preferences.Setting
        context['section_list'] = Section.objects.all().order_by('name')[:16]
        context['c_section'] = Section.objects.get(id=section_id)
        context['packages_num'] = _("%d packages in this section." % packages_num)
        return context
