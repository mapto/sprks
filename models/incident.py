__author__ = 'zcabh_000'

from environment import db

class incident:
    classes = [range(1, 8)]

    def get_incident(self, cls):
        list = db.select('incidents', where="idincident=$id", vars=locals())
        if len(list) == 0:
            raise KeyError("Incident ID not found.")
        return list[0]

    def get_incident_description(self, cls):
        #        return self.get_incident(cls).description
        return 1

    def get_incident_risk(self, cls):
        #        return self.get_incident(cls).risk
        return 1

    def get_incident_cost(self, cls):
        #        return self.get_incident(cls).cost
        return 1
