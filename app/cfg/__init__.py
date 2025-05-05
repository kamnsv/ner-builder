import json
import logging
import os


docs      = '/docs'
api       = '/api'
#tabby_url = os.getenv('tabby_url')
#tabby_key = os.getenv('tabby_key')
tabby_url='http://ner_llm:8080'
tabby_key='auth_cdf9d031b12341139775b3c68fb1395f'
kg_url  = os.getenv('kg_url')
kg_user = os.getenv('kg_user','neo4j')   
kg_pswd = os.getenv('kg_password','password')
title     = os.getenv('title','Graph knowledge creator')
desc      = os.getenv('desc','Builder graph knowledge')
debug     = bool(os.getenv('debug', '1'))

with open('/app/cfg/logger.json', 'r') as f:
    config = json.load(f)
    if debug:
        config['handlers']['console']['level'] = 'DEBUG'
    logging.config.dictConfig(config)
    logging.captureWarnings(True)
