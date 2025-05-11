
# Большая языковая модель

В проекте используется квантованная модель Gemma2 на базе LLama, которая переобучена на русскоязычном датасете Saiga.

Модель загружается из репозитория [HuggingFace](https://huggingface.co/Kamnsv/SaigaGemma2-9B-GGUF).

По умолчанию модель загружается на CPU в память, и в зависимости контекстного окна в настройках занимает от 6Gb.

Проект имеет интеграцию с open source проектом [Tabby](https://github.com/TabbyML/tabby) и если указать в переменных окружения токен и url к API Tabby, то приложение будет обращаться к стороннему API. 

```
tabby_url=http...
tabby_key=auth_...
```

Tabby позволяет локально или удаленно развернуть квантованную модель на устройствах cuda, metal, rock или vulkan. По умолчанию нет зарегистрированной модели `SaigaGemma2` но её можно добавить, создав models.json:
```
[    
    {
      "name": "Nomic-Embed-Text",
      "provider_url": "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF",
      "license_name": "Apache 2.0",
      "license_url": "https://choosealicense.com/licenses/apache-2.0/",
      "urls": [
        "https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q8_0.gguf"
      ],
      "sha256": "3e24342164b3d94991ba9692fdc0dd08e3fd7362e0aacc396a9a5c54a544c3b7"
    },
    {
      "license_name": "Gemma License",
      "license_url": "https://ai.google.dev/gemma/terms",
      "chat_template": "{% for message in messages %}{% if (message['role'] == 'assistant') %}{% set role = 'model' %}{% else %}{% set role = message['role'] %}{% endif %}{{ '<start_of_turn>' + role + '/n' + message['content'] | trim + '<end_of_turn>\n' }}{% endfor %}",
      "name": "SaigaGemma2-9B",
      "provider_url": "https://huggingface.co/Kamnsv/SaigaGemma2-9B-GGUF",
      "urls": [
        "https://huggingface.co/Kamnsv/SaigaGemma2-9B-GGUF/resolve/main/model-00001-of-00001.gguf"
      ],
      "sha256": "07dca63c396ed58060e75ad3f9409e89b30a9f7771989aefacfa03bb17d8eed9"
    }
  ]
```

и запустить контейнер, например для CUDA:

```
  tabbyml:
    image: tabbyml/tabby
    command: > 
     serve 
     --device cuda 
     --chat-model ${tabby_model:-SaigaGemma2-9B}
    ports:
      - "8080:8080"
    volumes:
      - ./models.json/:/data/models/TabbyML/models.json:ro
      - ${models:-./data/models/}:/data/models/TabbyML:rw
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              capabilities: ["gpu"]
```

После запуска Tabby необходимо зарегистрироваться в web-интерфейсе (по умолчанию http://localhost:8080/) и потом взять Token. Создайте .env и поместить туда переменную окружения `tabby_key`.


## Особенность тестирования

Генеративные модели обладают свойством стохастичности, то есть их ответы не являются детерминированными и могут варьироваться при повторных запросах. Это связано с использованием параметра seed, который задаёт начальное состояние генератора случайных чисел и влияет на воспроизводимость результата. Вследствие этого тесты, проверяющие точное совпадение ответов, могут периодически давать сбои.

> Параметр `seed` в проекте напрямую не влияет на сервис Tabby, однако параметр temperature передаётся со значением 0. Это означает, что генерация в Tabby фактически детерминирована по параметру температуры.