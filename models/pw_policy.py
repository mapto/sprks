__author__ = 'Horace'

from settings import settings


class pw_policy_model:

    def update(self, i):
        db = settings().db
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