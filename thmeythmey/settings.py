
BOT_NAME = 'thmeythmey'

SPIDER_MODULES = ['thmeythmey.spiders']
NEWSPIDER_MODULE = 'thmeythmey.spiders'

ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'thmeythmey.pipelines.MySQLPipeline': 2
}

DOWNLOADER_MIDDLEWARES = {
	'thmeythmey.middlewares.SeleniumMiddleware': None
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'helloworld'
DB_DB = 'khmergoo_sequelize'
