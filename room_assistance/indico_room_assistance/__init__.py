# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2019 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from indico.core import signals
from indico.util.i18n import make_bound_gettext


_ = make_bound_gettext('room_assistance')


@signals.import_tasks.connect
def _import_tasks(sender, **kwargs):
    import indico_room_assistance.tasks
