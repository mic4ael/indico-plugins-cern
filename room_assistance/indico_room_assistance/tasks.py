# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2019 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

import dateutil.parser
from celery.schedules import crontab

from indico.core.celery import celery
from indico.core.config import config
from indico.core.db import db
from indico.core.notifications import make_email, send_email
from indico.core.plugins import get_plugin_template_module
from indico.modules.events.models.events import Event
from indico.modules.events.requests.models.requests import Request, RequestState
from indico.util.date_time import now_utc

from indico_room_assistance.plugin import RoomAssistancePlugin


@celery.periodic_task(run_every=crontab(minute='0', hour='6'), plugin='room_assistance')
def room_assistance_emails():
    requests = (Request.query
                .filter(Request.type == 'room-assistance',
                        Request.state == RequestState.accepted,
                        Event.own_room_id.isnot(None),
                        db.cast(Request.data['start_dt'].astext, db.Date) == db.cast(now_utc(), db.Date))
                .join(Event))

    template = get_plugin_template_module('emails/room_assistance_emails.html', requests=requests,
                                          parse_dt=dateutil.parser.parse)
    recipients = RoomAssistancePlugin.settings.get('room_assistance_recipients')
    if recipients:
        email = make_email(from_address=config.NO_REPLY_EMAIL, to_list=recipients, template=template, html=True)
        send_email(email)
