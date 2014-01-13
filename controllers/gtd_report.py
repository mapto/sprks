__author__ = 'ZHANELYA'
from models.gtd import goal_task_differentiation as gtd
from localsys.environment import context


class report:
    def GET(self):
        #gtd.get_goal_task_differentiation(context.user_id())
        return "hi"