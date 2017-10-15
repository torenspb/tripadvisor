Скрипт парсит отзывы с сайта tripadvisor.ru, агрегируя результаты в CSV-файл.
В выборку попадают - дата отзыва, имя пользователя, возраст и пол пользователя(если указаны), оценка месту, заголовок и текст отзыва.
Скрипт делался под конкретную задачу в рамках проводимого лабораторией экономики культуры НИУ ВШЭ исследования.
Используемые модули - requests, BeautifulSoup, csv.

На вход скрипт принимает csv файл с параметрами в формате:
name,http-url,list_count
где name - будущее имя файла для хранения результатов парсинга, http-url - ссылка на первую страницу места, list_count - кол-во страниц, с которых будет собираться информация.
Парсинг ведется по мобильной версии сайта, т.к. для получения возраста и пола пользователя необходимо дополнительно получать информацию из профиля, что удобнее и проще реализовать в версии для смартфонов.

Проект сопровожден наглядным примером.
