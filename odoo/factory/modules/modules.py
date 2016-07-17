# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import datetime

class fac_worker(osv.osv):      #工人模型
    _name = 'fac.worker'

    _columns = {
        'name': fields.char(u'姓名', size=64, translate=True),
        'person_id': fields.char(u'身份证', size=64),
        'gender': fields.selection([('male', u'男'), ('female', u'女')], u'性别'),
        'phone': fields.char(u'手机号码', size=64),
        'entry_date': fields.date(u'入职时间', readonly=True),
        # 'skills': fields.many2many('fac.skills', 'fac_worker_skills_rel', 'language', 'language_id', u'技能'),
        'skills': fields.many2many('fac.skills', string=u'技能', domain="[('state', '=', 'True')]"),
        'product_id': fields.many2many('fac.product', string=u'产品'),
    }

    _defaults = {
        'person_id': 510108199511069878,
        'phone': 15908128562,
        'entry_date': fields.datetime.now(),
     }

    def check_person_id(self, cr, uid, ids, context=None):      #身份证号码位数的验证方法
        for i in self.browse(cr, uid, ids, context=context):
            if len(i.person_id) == 18:
                return True
            return False

    def check_phone(self, cr, uid, ids, context=None):      #手机号码位数的验证方法
        for i in self.browse(cr, uid, ids, context=context):
            if len(i.phone) == 11:
                return True
            return False

    # _constraints = [
	# 	(check_person_id, u'身份证号码必须18位', ['person_id']),
	# 	(check_phone, u'手机号码必须11位', ['phone']),
	# ]
    #
    # _sql_constraints = [
	# 	('uniq_person_id', 'unique(person_id)', u'身份证号码必须唯一'),
	# 	('uniq_phone', 'unique(phone)', u'手机号码必须唯一'),
	# ]


class fac_leader(osv.osv):      #组长模型
    _name = 'fac.leader'

    _inherit = 'fac.worker'

    _columns = {
        'entry_date': fields.date(u'管理起始时间', required=True, readonly=True),
        'number': fields.integer(u'组长号'),
        'degree': fields.selection([('1', u'初级'), ('2', u'中级'), ('3', u'高级')], u'组长等级'),
    }


class fac_skills(osv.osv):      #技能模型
    _name = 'fac.skills'

    _columns = {
        'name': fields.char(u'语言', required=True),
        'category': fields.many2one('fac.ski.group', u'所属技能组'),
        'degree': fields.selection([('heigh', u'重要'), ('medium', u'一般'),
            ('low', u'较低')], u'需求程度'),
        'state': fields.boolean(u'激活状态'),
        # 'user_num': fields.many2one('fac.worker', u'掌握该技能人数'),
    }

    _defaults = {
        'degree': 'heigh',
        'state': False,
    }

    _sql_constraints = [
		('uniq_name', 'unique(name)', u'语言必须唯一'),
	]

# class fac_worker_skills_rel(osv.osv):       #工人与技能联系的中间表
#     _name = 'fac.worker.skills.rel'
#
#     _columns = {
#         'language_id': fields.many2one('fac.skills'),
#         'skills_id': fields.many2one('fac.worker'),
#     }


class fac_ski_group(osv.osv):        #技能组模型
    _name = 'fac.ski.group'

    _columns = {
        'name': fields.char(u'技能组合名', required=True),
        'child_skills': fields.one2many('fac.skills', 'category', u'子技能', required=True),
    }

    _sql_constraints = [
		('uniq_name', 'unique(name)', u'技能组合名必须唯一'),
	]

    def name_get(self, cr, uid, ids, context=None):
        #在技能组合名后显示具体该技能组合包含多少种语言
        res = super(fac_ski_group, self).name_get(cr, uid, ids, context=context)

        for index, name in enumerate(res):
            group = self.browse(cr, uid, name[0], context=context)
            if group.child_skills:
                length = len([line for line in group.child_skills])
                res[index] = (group.id, group.name + u'（' + str(length) + u'种语言' + u'）')

        return res


class fac_product(osv.osv):         #产品模型
    _name = 'fac.product'

    def _get_continue_days(self, cr, uid, ids, field_name, args, context=None):
        #continue_days函数字段的第一计算函数
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            _start_date = datetime.datetime.strptime(product.start_date, '%Y-%m-%d')
            _end_date = datetime.datetime.strptime(product.end_date, '%Y-%m-%d')
            res[product.id] = (_end_date - _start_date).days
            # res.update({product.id: (_end_date - _start_date).days})
        return res

    def _set_continue_days(self, cr, uid, ids, field_name, changed_id, args, context=None):
        #continue_days函数字段的修改字段后的计算函数
        if not changed_id:
            return

        for product in self.browse(cr, uid, ids, context=context):
            if product.start_date:
                _start_date = datetime.datetime.strptime(product.start_date, '%Y-%m-%d')
                _end_date = datetime.timedelta(days=changed_id) + _start_date

                product.write({'end_date': _end_date})

    def finish_percent(self, cr, uid, ids, field_name, args, context=None):
        #everyday_percent函数字段的第一计算函数
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            _finish_percent = 1 / product.everyday_percent
            res.update({product.id: _finish_percent})
        return res

    def _has_worker(self, cr, uid, ids, context=None):
        #工作流最终审核的判断两个条件之一：产品指定了工人返回True，否则False
        for product in self.browse(cr, uid, ids, context=context):
            if product.pro_worker:
                return True
        print u'没有工人无法制造产品！'
        return False

    def _has_skills(self, cr, uid, ids, context=None):
        #工作流最终审核的判断两个条件之一：产品指定了技术组合返回True，否则False
        for product in self.browse(cr, uid, ids, context=context):
            if product.pro_ski_group:
                return True
        print u'没有相关技术无法制造产品！'
        return False

    def _get_state_from_product(self, cr, uid, context=None):
        #返回state字段的列表选项
        return [
            ('requirement', u'提出需求'),
            ('plan', u'制定方案'),
            ('1th_approved', u'初步审核'),
            ('2th_approved', u'最终审核'),
            ('start', u'开工制作'),
            ('finished', u'完成收工'),
        ]

    def write_pro_database(self, cr, uid, ids, context=None):
        #数据存入数据库
        return self.write(cr, uid, ids, {'name': 'data save database ok'})

    _columns = {
        'name': fields.char(u'产品名', size=64, required=True),
		'start_date': fields.date(u'开工时间', required=True),
		'end_date': fields.date(u'完工时间', required=True),
		'continue_days': fields.function(_get_continue_days, fnct_inv=_set_continue_days,
			string=u'生产天数', type='integer', store=False),
        'everyday_percent': fields.float(u'每天完成进度(填写范围在(0~1))', digits=(1,2), required=True),
        'plan_days': fields.function(finish_percent, string=u'预计天数', type='integer', store=False),
        'state': fields.selection(_get_state_from_product, u'产品状态'),
        'pro_worker': fields.many2many('fac.worker', string=u'产品制作者'),
        'pro_ski_group': fields.many2many('fac.ski.group', string=u'需要的技能组'),
        'child_ski': fields.related('pro_worker', 'skills', string=u'制作者具有的子技能', type='many2many',
            relation='fac.skills'),
    }

    _defaults = {
        'everyday_percent': '0.5',
    }

    def check_date(self, cr, uid, ids, context=None):
        #_结束时间大于开始时间的约束函数
        for product in self.browse(cr, uid, ids, context=context):
            if product.start_date and product.end_date and product.continue_days < 0:
                return False
        return True

    def check_plan_days(self, cr, uid, ids, context=None):
        #预计天数是否能完成产品的约束函数
        for product in self.browse(cr, uid, ids, context=context):
            if 1 / product.everyday_percent > product.continue_days:
                return False
        return True

    _constraints = [
        (check_date, u'结束时间必须大于开始时间', ['start_date', 'end_date']),
        (check_plan_days, u'预计天数无法完成产品', ['continue_days', 'everyday_percent']),
    ]

    _sql_constraints = [
        ('uniq_name', 'unique(name)', u'产品名必须唯一'),
        ('check_everyday_percent', 'check(everyday_percent>0 and everyday_percent<1)',
            u'每天完成进度的填写范围在(0~1)'),
    ]