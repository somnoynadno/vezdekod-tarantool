# vezdekod-tarantool

```
  / _ \
\_\(_)/_/
 _//o\\_
  /   \
```

## Инсталляция

Сервис (UI) доступен по адресу http://somnoynadno.ru:8000

Можно самостоятельно поднять в Docker командой:

```bash
 $ docker-compose up --build -d
 ```

И применить настройки индексов в Tarantool:
```commandline
> image_space = box.schema.space.create('image_space')
> image_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
> caption_space = box.schema.space.create('caption_space')
> caption_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
> fulltext_search_space = box.schema.space.create('fulltext_search_space')
> fulltext_search_space:create_index('primary', {parts = {1, 'unsigned', is_nullable=false}})
> fulltext_search_space:create_index('secondary', {unique = false, parts = {2, 'string', is_nullable=false}})
```

## Документация API

Для удобства тестирования предоставляю 
[коллекцию Postman](https://www.getpostman.com/collections/46a3f6baa0a7fbd9a2af).

Нужно только поменять URL на http://somnoynadno.ru:8000

### Создание мема

**Важно:** не надо отправлять большие изображения, их не может 
переварить хранилка (я её для этого не тюнил) 

```bash
 $ curl -X POST -F 'image=@your_image.png' -F 'upper_text=Hello' -F 'lower_text=Woooorld' -F 'vk_style=true' http://localhost:8000/set
```

P.S. Выставленное поле "vk_style" позволяет изменить монотонный цвет изображения
на случайный из палитры ВК.

### Создание мема (JSON)

Мне так чуть больше нравится:

```bash
 $ curl -X POST \
   -H 'Content-Type: application/json' \
   -d '{"upper_text":"Hey!!!","lower_text":"Create meme","vk_style":true,"image":"b64_image_string=="}' \
   http://localhost:8000/set/json
```

### Получение мема по ID

Лучше сразу в браузере открывать

```bash
 $ wget http://localhost:8000/get/<meme_id>
```

## Контакты

Если возникнут вопросы: [@somnoynadno](https://t.me/somnoynadno)

#### Небольшая обратная связь

Честно говоря, я так и не понял выигрышные стороны у Tarantool 
для решения этого задания. Первое время у меня создавалось впечатление,
что эта хранилка мне только мешается: не особо понятен в чём смысл туда
пихать картинки и как корректно строить поисковый индекс. Поэтому я 
спроектировал систему примерно так, как спроектировал бы её на базе
того же домороченного Redis, а в самом конце даже получил некий кайф от
автогенерации мемов))
