# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request


class fac_web(http.Controller):
    # _name = "fac.web"

    @http.route('/factory/factory/', auth='public', website=True)
    def index(self, **kw):
        Workers = http.request.env['fac.worker']

        return http.request.render('factory.index', {
            'workers': Workers.search([])
        })

    @http.route('/factory/<model("fac.worker"):worker>/', auth='public', website=True)
    def worker(self, worker):
        return http.request.render('factory.worker', {
            'person': worker
        })

    @http.route(['/factory/inputer/'], type='http', auth='public', website=True)
    def inputer(self, **kw):
        return http.request.render('factory.inputer', {})

    @http.route(['/factory/check/'], type='http', auth='public', website=True)
    def check(self, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        mod_get = pool.get('fac.worker')
        ids_get = mod_get.search(cr, uid, [('name', '=', request.params.get('fullname'))])

        if ids_get:
            return http.local_redirect('/factory/factory/')
        else:
            return """<script type='text/javascript'>
                    alert("人员无法查询");
                    </script>"""

    @http.route('/factory/add', type='http', auth='public', website=True)
    def add(self, **post):
        return http.request.render('factory.add', {})

    @http.route('/factory/adds', auth='public', type='json', method=['POST'], website=True)
    def adds(self, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        i = pool.get('fac.worker')
        i.create(cr, uid, kw, context)


