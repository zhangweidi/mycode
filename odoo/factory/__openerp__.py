# -*- coding: utf-8 -*-
{
	'name': 'factory',
	'version': '1.0',
	'author': 'zhangweidi',
	'description':
		'''
		Odoo模块开发工厂练习篇
		''',
		'depends': ['base','website'],
		'data': [
			'security/ir.model.access.csv',
			# 'security/ir_ui_view.xml',
            'views/templates_input.xml',
            'views/templates.xml',
			'views/factory_view.xml',
			'views/factory_workflow.xml',
            # 'views/factory_demo.xml',
			# 'sincere_training_report.xml',
			],
        'js': ['static/src/js/*.js'],
		'auto_install': False,
}