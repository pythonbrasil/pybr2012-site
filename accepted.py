#!/usr/bin/env python
# coding: utf-8

from pythonbrasil8.schedule.models import Session


approved_talks = [83, 92, 68, 102, 18, 62, 39, 99, 112, 2, 12, 81, 35, 42, 17, 97,
                  103, 126, 57, 58, 69, 71, 95, 24, 63, 108, 80, 38, 107, 9, 1,
                  123, 5, 31, 22, 73, 91, 124, 8, 34, 48, 120, 128, 113, 3, 79,
                  51, 19, 21, 26, 50, 114]

approved_tutorials = [78, 93, 59, 6, 86, 32, 105, 89, 60, 131, 132, 133]

for session in Session.objects.all():
    if session.id in approved_talks or session.id in approved_tutorials:
        session.status = u'accepted' # WTF?
    else:
        session.status = u'proposed'
    session.save()
    print session.type, session.status, session.id, session.title.encode('utf-8')
