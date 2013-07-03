__author__ = 'Daniyar'

import numpy

class company:
    def __init__(self, size=200, distribution=[.1, .5, .4], support=5):
        self.size = size # in thousand of employees
        self.distribution = distribution
        self.support = support # number of support staff per one staff unit (1000 employees)
        # 'desk' used for office worker, but changed in order to distinguish from office as location
        self.employee_types = {'executives', 'desk', 'road'}
        self.location_types = {'office', 'public', 'home'}
        self.device_types = {'desktop', 'laptop', 'phone'}

        self.employees2locations = numpy.genfromtxt('static/data/locations.csv', delimiter=',') # rows - locations, columns - employees
        self.employees2devices = numpy.genfromtxt('static/data/devices.csv', delimiter=',') # rows - devices, columns - employees

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_user_distribution(self):
        return self.distribution

    def get_location_distribution(self):
        return self.employees2locations.dot(self.distribution)

    def get_device_distribution(self):
        return self.employees2devices.dot(self.distribution)

    def add_policy(self,policy_name, policy):
        self.systems[policy_name] = policy

    def get_systems(self):
        return self.systems

    def set_support(self, support):
        pass

    def get_support(self):
        return self.support

if __name__ == "__main__":
    co = company()
    print str(co.employee_types) + " " + str(co.get_user_distribution())
    print str(co.location_types) + " " + str(co.get_location_distribution())
    print str(co.device_types) + " " + str(co.get_device_distribution())


