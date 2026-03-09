{
    "name": "Awesome owl",
    "version": '1.0',
    "category": "other/",
    "license": "AGPL-3",
    "summary": "Awesome owl",
    "author": "Manoj Parmar",
    "maintainers": ["Manoj Parmar"],
    "website": "www.abc.com",
    "depends": [],
    'external_dependencies': {
        # 'python': ['']
    },
    "data": [
        # "security/ir.model.access.csv",
        # "views/.xml",
        # "report/.xml",
        # "data/multiple_cron.xml",
    ],
    'demo': [],
    'post_init_hook': '',
    'assets': {
        'web.assets_backend': [
            # 'awesome_owl/static/src/components',
        ],
        'web.assets_frontend': [
            'awesome_owl/static/src/js/*',
        ],
    },
    "installable": True,
    'auto_install': False,
    "application": True,
}
