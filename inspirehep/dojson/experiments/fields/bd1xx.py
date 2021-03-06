# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""MARC 21 model definition."""

from dojson import utils

from ..model import experiments


@experiments.over('experiment_name', '^119..')
def experiment_name(self, key, value):
    """Name of experiment."""
    value = utils.force_list(value)
    self.setdefault('affiliation', [v.get("u") for v in value if v.get('u')])
    return {
        'experiment': [v.get("a") for v in value if v.get('a')],
        'wwwlab': [v.get("u") for v in value if v.get('u')]
    }


@experiments.over('contact_email', '^270..')
@utils.for_each_value
def contact_email(self, key, value):
    """Contact email of experiment."""
    return value.get("m")


@experiments.over('title', '^245[10_][0_]')
@utils.for_each_value
@utils.filter_values
def title(self, key, value):
    """Title Statement."""
    self.setdefault('breadcrumb_title', value.get('a'))
    return {
        'title': value.get('a'),
        'subtitle': value.get('b'),
        'source': value.get('9'),
    }


@experiments.over('name_variants', '^419..')
@utils.for_each_value
def name_variants(self, key, value):
    """Variants of the name."""
    return value.get('a')


@experiments.over('description', '^520..')
@utils.for_each_value
def description(self, key, value):
    """Description of experiment."""
    return value.get("a")


@experiments.over('spokesperson', '^702..')
@utils.for_each_value
def spokesperson(self, key, value):
    """Spokesperson of experiment."""
    return value.get("a")


@experiments.over('collaboration', '^710..')
def collaboration(self, key, value):
    """Collaboration of experiment."""
    value = utils.force_list(value)
    collaborations = sorted((elem["g"] for elem in value if 'g' in elem), key=lambda x: len(x))
    if len(collaborations) > 1:
        self['collaboration_alternative_names'] = collaborations[1:]
    if collaborations:
        return collaborations[0]


@experiments.over('urls', '^856.[10_28]')
@utils.for_each_value
def urls(self, key, value):
    """URLs."""
    return value.get('u')


@experiments.over('related_experiments', '^510')
@utils.for_each_value
def related_experiments(self, key, value):
    """Related experiments."""
    try:
        recid = int(value.get('0'))
    except (TypeError, ValueError):
        recid = None
    return {
        'name': value.get('a'),
        'recid': recid
    }


@experiments.over('date_started', '^046..')
def date_started(self, key, value):
    """Date started and completed."""
    value = utils.force_list(value)
    date_started = None
    for val in value:
        if val.get('t'):
            self.setdefault('date_completed', val.get('t'))
        if val.get('s'):
            date_started = val.get('s')
    return date_started


@experiments.over('field_code', '^65017')
@utils.for_each_value
def field_code(self, key, value):
    """Field code."""
    return value.get('a')


@experiments.over('accelerator', '^693')
@utils.for_each_value
def accelerator(self, key, value):
    """Field code."""
    return value.get('a')
