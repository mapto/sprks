"""
Goal Task Differentiation Model
This Model represents how different complexity of a policy set by a user during the game
affects the behaviour of employees. Location distribution for the employees is also considered
"""
__author__ = 'ZHANELYA'

import numpy
from scipy.sparse import vstack
from copy import copy, deepcopy
from models.policies import policies_model
from localsys.environment import context


class goal_task_differentiation: #needs to be called in the end of each term (month) after the policies set by a user have been updated in DB
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
    policy_complexity = ['complex', 'medium', 'easy']

    def __init__(self, p_user_id):
        self.user_id = p_user_id
        self.behaviours2employees = numpy.genfromtxt('static/data/gtd_model/behaviours2employees.csv', delimiter=',') # columns - behaviours, # rows - employees
        self.locations2employees = numpy.genfromtxt('static/data/gtd_model/locations2employees.csv', delimiter=',') # columns - locations, # rows - employees
        self.pc_modifier_complexity2behaviour = numpy.genfromtxt('static/data/gtd_model/pc_modifier_complexity2behaviour.csv', delimiter=',') #columns - complexity, #rows - behaviours
        self.r_modifier_complexity2behaviour = numpy.genfromtxt('static/data/gtd_model/r_modifier_complexity2behaviour.csv', delimiter=',') #columns - complexity, #rows - behaviours
        self.policy = policies_model.get_policies_list(self.user_id)

    def get_policy_complexity(self, policy):
        complexity = 'none'
        if int(policy['plen'])>10 or int(policy['psets'])>3 or int(policy['phist'])>2 or int(policy['prenew'])>1:        # see pw_policy.py model for the reference
            complexity = 'complex'
        elif int(policy['plen'])>6 or int(policy['psets'])>1 or int(policy['pdict'])==1 or int(policy['phist'])==2 or int(policy['prenew'])==1:
            complexity = 'medium'
        elif int(policy['plen'])>0:
            complexity = 'easy'
        #complexity = 'easy'#/'complex'/'medium' for testing of extreme cases
        return complexity

    def get_goal_task_differentiation(self, empl_num):
        total_possible_empl_num = 9
        total_pc_modifier = 0
        total_r_modifier = 0
        if empl_num == 1:
            empl_tps = ['executives']
            empls = [ 'som']
        elif empl_num == 3:
            empl_tps = ['executives','desk','road']
            empls = [ 'padh', 'cam', 'ft']
        elif empl_num == 9:
            empl_tps = ['executives','executives','executives',
                      'desk','desk','desk',
                      'road','road','road']
            empls = [ 'padh', 'som', 'bdd',
                  'cam', 'rm', 'pm',
                  'ft', 'sc', 'sm']
        output = numpy.array(["employee","location","pswd_complexity",0,0])
        report = {"employees":[], "total":{}}
        report['employees'] = []

        for employee in empls:                 #for each possible employee (9 positions)
            employee_type = empl_tps[empls.index(employee)]
            for p in self.policy:                       #for each policy applied by a player (9 for each employee type out of 27)
                p_employee = p['employee']
                p_location = p['location']
                p_complexity = self.get_policy_complexity(p)
                if employee_type == p_employee:
                    possible_behaviours2locations = self.get_possible_behaviours2locations(employee, p_location)

                    pc_modifiers = deepcopy(self.pc_modifier_complexity2behaviour)
                    r_modifiers = deepcopy(self.r_modifier_complexity2behaviour)
                    if p_complexity=='none':
                        pc_modifier = [0,0,0]
                        r_modifier = [0,0,0]
                    else:
                        i = self.policy_complexity.index(p_complexity)
                        pc_modifier = [float(pc_modifiers[0][i]), float(pc_modifiers[1][i]), float(pc_modifiers[2][i])] #modifiers over behaviours
                        r_modifier = [float(r_modifiers[0][i]), float(r_modifiers[1][i]), float(r_modifiers[2][i])] #modifiers over behaviours

                    r_modifier = sum(possible_behaviours2locations.dot(r_modifier))    #dot product provides r_modifiers over different locations, which are then summed up
                    pc_modifier = sum(possible_behaviours2locations.dot(pc_modifier))  #dot product provides pc_modifiers over different locations, which are then summed up

                    output = numpy.vstack([output, [employee,p_location,p_complexity,r_modifier,pc_modifier]])

                    total_r_modifier = total_r_modifier + r_modifier
                    total_pc_modifier = total_pc_modifier + pc_modifier

                    flag=0
                    for rep in report['employees']:
                        if employee == rep['employee']:
                            flag=1
                            rep['risk'] = rep['risk']+r_modifier
                            rep['p_cost'] = rep['p_cost']+pc_modifier
                            break
                    if flag==0:
                        report['employees'].append({"employee":employee, "risk":r_modifier, "p_cost":pc_modifier})
        report['total']['risk'] = total_r_modifier*total_possible_empl_num/empl_num
        report['total']['p_cost'] = total_pc_modifier
        output = numpy.vstack([output, ["total","total","total",total_r_modifier,total_pc_modifier]])
        numpy.savetxt('static/data/gtd_model/tests/test'+str(self.user_id)+'.csv', output, fmt='%s')

        return report

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
    gtd = goal_task_differentiation(1)
    print str("behaviours\n" + str(gtd.behaviours2employees) + "\n")
    print str("locations\n" + str(gtd.locations2employees) + "\n")
    print( gtd.get_goal_task_differentiation(3))