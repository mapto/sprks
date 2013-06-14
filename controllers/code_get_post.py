import web
from time import strftime
import json
import session
from sim.simulation import simulation
from datetime import time, timedelta, datetime, date
from environment import render_private as render
from environment import db
from models.pw_policy import pw_policy_model

class pwpolicy_form:
    def GET(self):
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id
            check = db.select('pw_policy', where="userid=$id_user", vars=locals())
            if len(check) > 0:
                notfound=0
              #  result_get = db.select('pw_policy', where="idpolicy=$id_tmp", vars=locals())[0]
                result_get = check[0]
                return render.pwpolicy_form(result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound)
            else:
                notfound=1
                dt = datetime.now()
                dtt = dt - timedelta(days=dt.weekday())
                db.insert('pw_policy', plen=8, psets=2, pdict=0,
                          phist=1, prenew=1, pattempts=0,
                          pautorecover=1, userid=id_user, date=dtt.strftime("%Y/%m/%d %H:%M:%S"))
                result_get = db.select('pw_policy', where="userid=$id_user", vars=locals())[0]
                return render.pwpolicy_form(result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound)
        else:
            raise web.seeother('/login')

    def POST(self):
        web.header('Content-Type', 'application/json')
        usrid = session.mysession.session.id
        sim = simulation()
        data = json.loads(web.data())
#       print "data is " + json.dumps(data)
       # print str(data["data"])
        """for policy in data:
            # currently separate query for each attribute. In production needs to collect them
            if policy["name"] != "userid":
                result = db.query("UPDATE `pw_policy` SET `" + policy["name"] + "` =  '" + policy["value"] + "' WHERE  `pw_policy`.`userid` ="+"$usrid;", vars=locals())
                if policy["name"] != "date":
                    sim.set_policy(policy["name"], int(policy["value"]))"""
        pw_policy_model().update({'userid':str(usrid)}, eval(data["data"]))
        tmp = eval(data["data"])
        for k, value in tmp.iteritems():
            print k, value
            sim.set_policy(k, value)
        #db.update('pw_policy', where="userid=$usrid", date=data["date"], vars=locals())
#        return json.dumps(data)
        return json.dumps([{"name": "prob", "value": sim.calc_risk_prob()},
                           {"name": "impact", "value": sim.calc_risk_impact()},
                           {"name": "cost", "value": sim.calc_prod_cost()}])


class add:
    def POST(self):
        # make sure that the following line stays as per your local installation


        form = web.input()
        id_tmp = form.id
        check = db.select('pw_policy', where="id=$id_tmp", vars=locals())
        if check:
            result = db.update('pw_policy', where='id = $form.id', plen=form.plen, psets=form.psets,
                                   pdict=form.pdict, phist=form.phist, prenew=form.prenew,
                                   pattempts=form.pattempts, pautorecover=form.pautorecover, vars=locals())
            print 'found id'+id_tmp
        else:
            result = db.insert('pw_policy', id=form.id, plen=form.plen,
                                   psets=form.psets, pdict=form.pdict,
                                   phist=form.phist, prenew=form.prenew,
                                   pattempts=form.pattempts, pautorecover=form.pautorecover)
            print 'id'+id_tmp+' does not exist'

        notfound=0
        return render.pwpolicy_form(form.id, form.plen, form.psets, form.pdict, form.phist,
                            form.prenew, form.pattempts, form.pautorecover, notfound)
