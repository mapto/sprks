__author__ = 'Daniyar'

import numpy


class company:
    employee_types = ['executives', 'desk', 'road'] # 'desk' == 'white-collar', 'road' == 'blue-collar'
    location_types = ['office', 'public', 'home']
    device_types = ['desktop', 'laptop', 'phone']

    employees_count = 2 * pow(10, 5)
    max_incident_cost = employees_count * pow(10, 3)

    def __init__(self, distribution=[.1, .5, .4], support=5):
        self.distribution = distribution
        self.support = support # number of support staff per one staff unit (1000 employees)
        # 'desk' used for office worker, but changed in order to distinguish from office as location

        self.employees2locations = numpy.genfromtxt('static/data/locations.csv', delimiter=',') # rows - locations, columns - employees
        self.employees2devices = numpy.genfromtxt('static/data/devices.csv', delimiter=',') # rows - devices, columns - employees

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_user_distribution(self):
        return self.distribution

    def get_location_distribution(self, employee="any"):
        if employee == "any":
            return self.employees2locations.dot(self.distribution)
        else:
            index = self.employee_types.index(employee)
            return self.employees2locations[:,index]

    def get_device_distribution(self, employee="any"):
        if employee == "any":
            return self.employees2devices.dot(self.distribution)
        else:
            index = self.employee_types.index(employee)
            return self.employees2devices[:,index]

    def set_support(self, support):
        pass

    def get_support(self):
        return self.support

if __name__ == "__main__":
    co = company()
    print str(co.employee_types) + " " + str(co.get_user_distribution())
    print str(co.location_types) + " " + str(co.get_location_distribution())
    print str(co.device_types) + " " + str(co.get_device_distribution())
    print co.get_location_distribution("executives")
    print co.get_location_distribution("desk")
