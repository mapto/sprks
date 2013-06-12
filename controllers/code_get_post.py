import web
import string
import json
import session
from sim.simulation import simulation
import math
from settings import settings



class index:
    def populate(self):
        ''' presumes that database is already connected
            OBSOLETE
        '''
#       use this if table needs to be created
        self.db.query('CREATE TABLE pw_policy(id INT NOT NULL PRIMARY KEY, plen INT, psets INT, pdict BOOL, phist INT, prenew INT, pattempts BOOL, pautorecover BOOL);')

#       use this if table needs to be filled with values
        self.db.query("INSERT INTO pw_policy VALUES (1, 8, 3, 0, 1, 1, 0, 1);")
        self.db.query("INSERT INTO pw_policy VALUES (2, 8, 3, 0, 1, 1, 0, 1);")
        self.db.query("INSERT INTO pw_policy VALUES (3, 8, 3, 0, 1, 1, 0, 1);")
        self.db.query("INSERT INTO pw_policy VALUES (4, 5, 3, 0, 1, 1, 0, 1);")

    def GET(self):
        db = settings().db
        render = settings().render
        if session.mysession.session.loggedin:
            #use this variable to request any ID number
            id_user = session.mysession.session.id
            check = db.select('pw_policy', where="userid=$id_user", order="date DESC", vars=locals())

            if check > 0:
                notfound=0
              #  result_get = db.select('pw_policy', where="idpolicy=$id_tmp", vars=locals())[0]
                result_get = check[0]
                return render.index(result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound)
            else:
                notfound=1
                result_get = db.select('pw_policy', where="userid=8", vars=locals())[0]
                return render.index(result_get.userid, result_get.plen, result_get.psets,
                                result_get.pdict, result_get.phist, result_get.prenew,
                                result_get.pattempts, result_get.pautorecover, notfound)
        else:
            raise web.seeother('/login')

    def POST(self):
        db = settings().db
        render = settings().render
		# TODO do we need to check session here?
        web.header('Content-Type', 'application/json')
        sim = simulation()
        i = web.input()
        #data = json.loads(web.data())
#        print "data is " + json.dumps(data)

        #for policy in data:
            # currently separate query for each attribute. In production needs to collect them
           # if policy["name"] != "idpolicy":
                #result = db.query("UPDATE `pw_policy` SET `" + policy["name"] + "` =  '" + policy["value"] + "' WHERE  `pw_policy`.`idpolicy` =1;")
        usrid = i.userid
        plen = i.plen
        psets = i.psets
        pdict = i.pdict
        phist = i.phist
        prenew = i.prenew
        pattempts = i.pattempts
        pautorecover = i.pautorecover
        result = db.update('pw_policy', where='userid = $usrid', plen=plen, psets=psets, pdict=pdict, phist=phist,
                           prenew=prenew, pattempts=pattempts, pautorecover=pautorecover, vars=locals())
        sim.set_policy("plen", int(plen))
        sim.set_policy("psets", int(psets))
        sim.set_policy("pdict", int(pdict))
        sim.set_policy("phist", int(phist))
        sim.set_policy("prenew", int(prenew))
        sim.set_policy("pattempts", int(pattempts))
        sim.set_policy("pautocover", int(pautorecover))
#        return json.dumps(data)
        return json.dumps([{"name": "prob", "value": math.ceil(sim.calc_risk_prob()*10000)/100},
                           {"name": "impact", "value": math.ceil(sim.calc_risk_impact()*100)/100},
                           {"name": "cost", "value": math.ceil(sim.calc_prod_cost()*100)/100}])


class add:
    def POST(self):
        # make sure that the following line stays as per your local installation
        db = settings().db
        render = settings().render

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
        return render.index(form.id, form.plen, form.psets, form.pdict, form.phist,
                            form.prenew, form.pattempts, form.pautorecover, notfound)
