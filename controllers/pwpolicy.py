import web
import json
import session
from sim.simulation import simulation
from datetime import timedelta, datetime
from environment import render_private as render
from environment import db
from models.pw_policy import pw_policy_model
from environment import get_start_time
from models.incident import incident


class pwpolicy:
    # the default policy should be specified in a central place and reusable
    default = {"plen": 8, "psets": 2, "pdict": 0,
               "phist": 1, "prenew": 1, "pattempts": 0,
               "precovery": 1}

    def GET(self):
        """
        Renders the form to input password policies.
        """
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id
            check = db.select('pw_policy', where="userid=$id_user", order="date DESC", vars=locals())
            if len(check) > 0:
                result_get = check[0]
                print "policies found in db " + str(result_get.pattempts)
                session.mysession.session.date = result_get.date
                return render.pwpolicy_form(session.mysession.session.user,result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.precovery, 0, session.mysession.session.turn)
            else:
#                dt = datetime.now()
#                dtt = dt - timedelta(days=dt.weekday()) #goes back to last monday
                # The default policy (i.e. when not specified by user)
                dtt = get_start_time()
                print "no policies found in db"
                db.insert('pw_policy', userid=id_user, date=dtt.strftime("%Y/%m/%d %H:%M:%S"),
                          plen=pwpolicy.default["plen"],
                          psets=pwpolicy.default["psets"],
                          pdict=pwpolicy.default["pdict"],
                          phist=pwpolicy.default["phist"],
                          prenew=pwpolicy.default["prenew"],
                          pattempts=pwpolicy.default["pattempts"],
                          precovery=pwpolicy.default["precovery"])
                result_get = db.select('pw_policy', where="userid=$id_user", vars=locals())[0]
                session.mysession.session.date = result_get.date
                return render.pwpolicy_form(session.mysession.session.user, result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.precovery, 1, result_get.date)
        else:
            raise web.seeother('/home')

    def POST(self):
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()
        data = json.loads(web.data())
        dat = eval(data["data"])
        print "form has " + str(dat)
        if "pdict" in dat:
            dict1=1
        else:
            dat["pdict"]=0
        if "precovery" in dat:
            precovery1=1
        else:
            dat["precovery"]=0
        if "pattempts" in dat:
            pattempts1=1
        else:
            dat["pattempts"]=0
        pw_policy_model().update({'userid':str(usrid), 'date':data["date"]}, dat)

#        return json.dumps(data)
        return json.dumps([{"name": "risk", "value": sim.get_risk(dat)},
                           {"name": "cost", "value": sim.calc_prod_cost(dat)}])
