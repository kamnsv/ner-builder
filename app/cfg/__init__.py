import json
import logging
import os
import torch
import random
import numpy as np

docs      = '/'
api       = '/api'
tabby_url = os.getenv('tabby_url', 'http://ner_llm:8080')
tabby_key = os.getenv('tabby_key')
model_url = os.getenv('model_url')
model_path = os.getenv('model_path')
model_context = int(os.getenv('model_context', '1024'))
kg_url  = os.getenv('kg_url')
kg_user = os.getenv('kg_user','neo4j')   
kg_pswd = os.getenv('kg_password','password')
title     = os.getenv('title','Graph knowledge creator')
desc      = os.getenv('desc','Builder graph knowledge')
debug     = bool(os.getenv('debug', 'DEBUG'))
path_ner  = os.getenv("ner_path")
device  = os.getenv("device", 'cuda')
stanza_local  = [True, None][bool(os.getenv("stanza_local", ''))] 
seed = int(os.getenv("seed", '0'))

random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)
np.random.seed(seed)
torch.manual_seed(seed)

with open('/app/cfg/logger.json', 'r') as f:
    config = json.load(f)
    config['handlers']['console']['level'] = debug
    logging.config.dictConfig(config)
    logging.captureWarnings(True)
