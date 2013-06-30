__author__ = 'Daniyar'


class company:
    def __init__(self, size=None, distribution=None, systems={}, support=None):
        self.size = size
        self.distribution = distribution
        self.systems = systems
        self.support = support

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def set_distribution(self, distribution):
        pass

    def get_distribution(self):
        pass

    def add_policy(self,policy_name, policy):
        self.systems[policy_name] = policy

    def get_systems(self):
        return self.systems

    def set_support(self, support):
        pass

    def get_support(self):
        return self.support


