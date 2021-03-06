## Формулировка задачи

Большинство веб-страниц сейчас перегружено всевозможной рекламой… Наша задача «вытащить»
из веб-страницы только полезную информацию, отбросив весь «мусор» (навигацию, рекламу и тд).
Полученный текст нужно отформатировать для максимально комфортного чтения в любом
текстовом редакторе. Правила форматирования: ширина строки не больше 80 символов (если
больше, переносим по словам), абзацы и заголовки отбиваются пустой строкой. Если в тексте
встречаются ссылки, то URL вставить в текст в квадратных скобках. Остальные правила на ваше
усмотрение. 

Программа оформляется в виде утилиты командной строки, которой в качестве параметра
указывается произвольный URL. Она извлекает по этому URL страницу, обрабатывает ее и
формирует текстовый файл с текстом статьи, представленной на данной странице.
В качестве примера можно взять любую статью на lenta.ru, gazeta.ru и тд
Алгоритм должен быть максимально универсальным, то есть работать на большинстве сайтов.

**Усложнение задачи 1**: Имя выходного файла должно формироваться автоматически по URL.
Примерно так:

http://lenta.ru/news/2013/03/dtp/index.html => [CUR_DIR]/lenta.ru/news/2013/03/dtp/index.txt

**Усложнение задачи 2**: Программа должна поддаваться настройке – в отдельном файле/файлах
задаются шаблоны обработки страниц

## Требования к выполнению задачи
1. Задача выполняется на С++|Python с использованием классов. Не должно использоваться
сторонних библиотек, впрямую решающих задачу.
2. Предпочтительная среда выполнения – MS Windows.
3. Решение должно состоять из документа, описывающего алгоритм, исходных кодов
программы, исполняемого модуля.
4. Приложите список URL, на которых вы проверяли свое решение. И результаты проверки.
5. Желательно указать направление дальнейшего улучшения/развития программы.

## Алгоритм
 - url принимается через параметр -u или --url
 - Создается, если отсутствует структура нужных папок
 - оригинальное содержимое страницы сохраняется в файл orig.txt
 - Содержимое страницы просматривается построчно в зависимости от параметров, указанных в conf.ini. Определяется заголовок новости и ее тело
 - уже отобранный текст заголовка и тела новости парсятся: удаляется html-маркировка, лишние теги, проставляются все переносы, текст разбивается по ширине.
 -результат записывается в файл res.txt
 
Пример запуска утилиты:
```Bash
D:\work\py>parse.py -u https://lenta.ru/news/2017/01/22/sobornost/
19:20:36.247053:        url is  https://lenta.ru/news/2017/01/22/sobornost/
19:20:36.841474:        original url content written to D:\work\py/lenta.ru/news/2017/01/22/sobornost/orig.txt
19:20:37.253765:        parsed url content written to D:\work\py/lenta.ru/news/2017/01/22/sobornost/res.txt
 ```
## Параметры
  - def_folder - папка, куда будем сохранять результаты,
  - usage_str - строка запуска утилиты,
  - string_size - Максимальная ширина строки,
  - header_tag - название тега заголовка новости,
  - header_tag_class - класс тега заголовка новости,
  - content_tag - тег тела новости,
  - content_tag_class - класс тега тела новости,
  - encoding - кодировка страницы.
## URL, на которых проверялось решение
 - https://lenta.ru/news/2017/01/22/sobornost/
 - https://lenta.ru/news/2017/01/22/prosecutors/
 - https://lenta.ru/news/2017/01/22/brennan_angered/
 - https://lenta.ru/news/2017/01/22/opec80percent/
 - https://lenta.ru/news/2017/01/22/pensionhelp/
## Направление дальнейшего улучшения
 - Передача скрипту списка url
 - Оптимизация алгоритма очистки контента от "мусора".
 - Использование утилиты как расширение в браузере (избавит от лишних действий, парсится будет открытая в данный момент страница)
