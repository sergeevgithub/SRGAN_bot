# SRGAN_bot
## Итоговый проект для первой части Deep Learning School


Короткое описание бота: 
Нужно отправить боту изображение, в ответ (примерно через 1,5 минуты) бот пришлет увеличенное в 4 раза изображение.
Бот начинает работу при отправке команды /start.


Что получилось сделать:
1) Собрана и обучена(плохо) модель на основе статьи https://arxiv.org/pdf/1609.04802.pdf
2) Собран чат-бот с помощью фреймворка aiogram, реализован интерфейс бота.
3) Все это хоть и локально, но собрано вместе.

Что не получилось сделать:
1) Деплой бота.
2) Асинхроность. По факту бот виснет во время обработки изображения.
3) Качество итогового изображения оставляет желать лучшего, генератор обучился слабо.

Для обучения использовался датасет DIV2K (https://data.vision.ee.ethz.ch/cvl/DIV2K/)
Использовались изображения Train Data Track 1 bicubic x8 (LR images) как входные и Train Data Track 1 bicubic downscaling x2 (LR images) как желаемый результат.
