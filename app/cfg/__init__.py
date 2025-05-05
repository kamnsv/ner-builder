import json
import logging
import os


docs      = '/docs'
api       = '/api'
tabby_url = os.getenv('tabby_url', 'http://ner_llm:8080')
tabby_key = os.getenv('tabby_key')
kg_url  = os.getenv('kg_url')
kg_user = os.getenv('kg_user','neo4j')   
kg_pswd = os.getenv('kg_password','password')
title     = os.getenv('title','Graph knowledge creator')
desc      = os.getenv('desc','Builder graph knowledge')
debug     = bool(os.getenv('debug', '1'))
path_ner  = os.getenv("ner_path")
with open('/app/cfg/logger.json', 'r') as f:
    config = json.load(f)
    if debug:
        config['handlers']['console']['level'] = 'DEBUG'
    logging.config.dictConfig(config)
    logging.captureWarnings(True)
