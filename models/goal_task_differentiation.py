__author__ = 'ZHANELYA'

import numpy
from copy import copy, deepcopy
from models.policies import policies_model
from localsys.environment import context


class goal_task_differentiation: #needs to be called in the end of each term (month) after the policies set by a user have been updated in DB
    #if (context.user_id()):
    #    user_id = context.user_id()
    #else:
    user_id = 1  # set to 0 for real game

    policy = policies_model.get_policies_list(user_id)

    employee_types = ['executives','executives','executives',
                      'desk','desk','desk',
                      'road','road','road']
    employees = [ 'padh', 'som', 'bdd',
                  'cam', 'rm', 'pm',
                  'ft', 'sc', 'sm']

    #Susie Queue, PA to Department Head (Executive)
    #Andrew Smith, Senior Operations Manager (Executive)
    #Karine Bordeaux, Business Development Director (Executive)
    #Iza Henata, Client Account Manager (Desk)
    #Helen Stark, Recruitment Manager (Desk)
    #Hue Matt, Project Manager (Desk)
    #Kevin Clark, Facilities Technician (Road)
    #Richard Holmes, Sales Consultant (Road)
    #Drake Green, Suppliers Manager (Road)

    behaviour_types = ['secure', 'productive', 'social']
    location_types = ['office', 'public', 'home']

    def __init__(self):
        self.behaviours2employees = numpy.genfromtxt('static/data/gtd_model/behaviours2employees.csv', delimiter=',') # columns - behaviours, # rows - employees
        self.locations2employees = numpy.genfromtxt('static/data/gtd_model/locations2employees.csv', delimiter=',') # columns - locations, # rows - employees

    def get_policy_complexity(self, policy):
        complexity = 'easy'
        if int(policy['plen'])>10 or int(policy['psets'])>3 or int(policy['phist'])>2 or int(policy['prenew'])>1:        # see pw_policy.py model for the reference
            complexity = 'complex'
        elif int(policy['plen'])>6 or int(policy['psets'])>1 or int(policy['pdict'])==1 or int(policy['phist'])==2 or int(policy['prenew'])==1:
            complexity = 'medium'
        return complexity

    def get_goal_task_differentiation(self):
        for p in self.policy:
            policy_employee = p['employee']
            policy_location = p['location']
            policy_complexity = self.get_policy_complexity(p)
            for employee in self.employees:
                employee_type = self.employee_types[self.employees.index(employee)]
                if employee_type == policy_employee:
                    print employee
                    print policy_location
                    print policy_complexity
                    print self.get_possible_behaviours2locations(employee,policy_location)
        return 0

    def get_locations_from_policy(self, employee, location, locations2employee): # if the policy is defined, say for office only, then assign the rest to 0
        if 'office' not in location:
            locations2employee[0]=0
        if 'public' not in location:
            locations2employee[1]=0
        if 'home' not in location:
            locations2employee[2]=0
        return locations2employee

    def get_behaviours2locations(self, employee="any", location="any"):                     #locations to behaviours distribution for any employee
        if employee == "any":                                               #if employee is not found in the list of employees
            return 0
        else:
            i = self.employees.index(employee)
            locations2employee = deepcopy(self.locations2employees[i])
            locations2employee = self.get_locations_from_policy(employee, location, locations2employee)
            behaviours2employees = deepcopy(self.behaviours2employees[i])
            behaviours2locations = numpy.outer(locations2employee, behaviours2employees)   #multiplication of 2 vectors
            return behaviours2locations                                # columns - behaviours, # rows - locations for employee

    def get_possible_behaviours2locations(self,employee="any", location="any"):
        if employee == "any":                                               #if employee is not found in the list of employees
            return 0
        else:
            possible_behaviours2locations = self.get_behaviours2locations(employee, location)
            self.behaviours2locations_possibility = numpy.genfromtxt('static/data/gtd_model/'+employee+'_behaviours2locations_possibility.csv', delimiter=',') # columns - locations, # rows - employees
            for index, x in numpy.ndenumerate(possible_behaviours2locations):
                if(self.behaviours2locations_possibility[index] == 0):
                    possible_behaviours2locations[index]=0
            return possible_behaviours2locations                       # columns - possible behaviours, # rows - locations for employee

if __name__ == "__main__":
    gtd = goal_task_differentiation()
    print str("behaviours\n" + str(gtd.behaviours2employees) + "\n")
    print str("locations\n" + str(gtd.locations2employees) + "\n")
    print( gtd.get_goal_task_differentiation())