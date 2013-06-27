__author__ = 'zcabh_000'

class incident:
    # index reference:
    # 0 - name (temporarily also serves as description)
    # 1 - plen, 2 - psets, 3 - pdict, 4 - phist, 5 - prenew, 6 - pattempts, 7 - pautorecover,
    # 8 - risk, 9 - cost
    list = (('void',         0, 0, 0, 0, 0, 0, 0,  0,   0),
            ('default',      8, 2, 0, 1, 1, 0, 1,  0.3, 0.3),
            ('very_easy',    0, 1, 0, 0, 1, 0, 1,  1,   0),
            ('eternal',      8, 1, 0, 0, 0, 0, 1,  0.5, 0),
            ('too_hard',    12,4,1,3,1,0,1,        0.7, 1),
            ('easy_recovery',8,1,0,0,3,0,1,        0.5, 0.1),
            ('too_demanding',8,1,1,3,3,0,0,        1,   0),
            ('easy_secure',  8,2,0,0,1,1,1,        0.1, 0.2),
            ('hard_secure', 10,3,0,0,1,1,0,        0.1, 0.3),
            ('too_often',    8,3,0,0,3,0,0,        0.8, 0.7))

    def __init__(self, cls):
        self.my_class = incident.list[cls]
        print 'incident class name is ' + self.my_class[0]

    def get_incident(self, cls):
        if len(list) < cls:
            raise KeyError("Incident ID not found.")
        return list[cls]

    def get_description(self):
        return self.my_class[0]

    def get_id(self):
        return self.my_class[0]

    def get_cost(self):
        return self.my_class[9]

    def get_risk(self):
        return self.my_class[8]