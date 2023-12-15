## Домашнее задание к занятию  «Очереди RabbitMQ»

### Задание 1. Установка RabbitMQ

Используя Vagrant или VirtualBox, создайте виртуальную машину и установите RabbitMQ.
Добавьте management plug-in и зайдите в веб-интерфейс.

*Итогом выполнения домашнего задания будет приложенный скриншот веб-интерфейса RabbitMQ.*


### Решение 1


#### Установка RabbitMQ и Managment plug-in

1. Команда установки RabbitMQ

	`sudo apt install rabbitmq-server`

2. Проверка сервиса RabbitMQ

	`sudo systemctl is-enabled rabbitmq-server`

	`sudo systemctl status rabbitmq-server`

4. Включение plug-in Managment

	`sudo rabbitmq-plugins enable rabbitmq_management`

	`sudo systemctl restart rabbitmq-server`
  
#### Скриншоты к Заданию 1

*Проверка установленных плагинов*

![Commit Task1](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task1p1.png)


*Включение плагина Managment*

![Commit Task1](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task1p2.png)


*Web-интерфейс приложения RabbitMQ*

![Commit Task1](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task1p3.png)



---

### Задание 2. Отправка и получение сообщений

Используя приложенные скрипты, проведите тестовую отправку и получение сообщения.
Для отправки сообщений необходимо запустить скрипт producer.py.

Для работы скриптов вам необходимо установить Python версии 3 и библиотеку Pika.
Также в скриптах нужно указать IP-адрес машины, на которой запущен RabbitMQ, заменив localhost на нужный IP.

```shell script
$ pip install pika
```

Зайдите в веб-интерфейс, найдите очередь под названием hello и сделайте скриншот.
После чего запустите второй скрипт consumer.py и сделайте скриншот результата выполнения скрипта

*В качестве решения домашнего задания приложите оба скриншота, сделанных на этапе выполнения.*

Для закрепления материала можете попробовать модифицировать скрипты, чтобы поменять название очереди и отправляемое сообщение.


### Решение 2


#### Поготовка к выполнению

1. Команда установки pip

        sudo apt install python3-pip

2. Установка pika

        pip install pika

*Для проверки очередей в RabbitMQ использовались два скрипта Python имитирующих работу датчиков*
*давления и температуры. Текст скриптов приложен в git c именами producer2.py и consumer2.py.*

#### Скриншоты к Заданию 2

*Очередь Pressure*

![Commit Task2](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task2p1.png)


*Очередь Temparature*

![Commit Task2](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task2p2.png)


*Очереди привязаны к exchange (sensor_exchange) и получают данные от producer2.py*

![Commit Task2](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task2p3.png)


*Очередь опустошена после запуска consumer2.py*

![Commit Task2](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task2p4.png)



---

### Задание 3. Подготовка HA кластера

Используя Vagrant или VirtualBox, создайте вторую виртуальную машину и установите RabbitMQ.
Добавьте в файл hosts название и IP-адрес каждой машины, чтобы машины могли видеть друг друга по имени.

Пример содержимого hosts файла:
```shell script
$ cat /etc/hosts
192.168.0.10 rmq01
192.168.0.11 rmq02
```
После этого ваши машины могут пинговаться по имени.

Затем объедините две машины в кластер и создайте политику ha-all на все очереди.

*В качестве решения домашнего задания приложите скриншоты из веб-интерфейса с информацией о доступных нодах в кластере и включённой политикой.*

Также приложите вывод команды с двух нод:

```shell script
$ rabbitmqctl cluster_status
```

Для закрепления материала снова запустите скрипт producer.py и приложите скриншот выполнения команды на каждой из нод:

```shell script
$ rabbitmqadmin get queue='hello'
```

После чего попробуйте отключить одну из нод, желательно ту, к которой подключались из скрипта, затем поправьте параметры подключения в скрипте consumer.py на вторую ноду и запустите его.

*Приложите скриншот результата работы второго скрипта.*


### Решение 3


#### Подготовка к объединению в кластер

1. Для сборки кластера, все ноды должны иметь одинаковый файл .erlang.cookie

        scp /var/lib/rabbitmq/.erlang.cookie andy@192.168.101.61:/var/lib/rabbitmq/

2. На втором ноде выполним
```
	sudo systemctl restart rabbitmq-server
	
	sudo rabbitmqctl stop_app

	sudo rabbitmqctl join_cluster rabbit@rmq1

	sudo rabbitmqctl start_app
```
3. На первой ноде выполним
```
	sudo rabbitmqctl cluster_status
```
4. Выполняем следующую команду для создания новой политики ha-all, которая позволит всем очередям быть зеркалированными на всех узлах кластера RabbitMQ.
```
	sudo rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all","ha-sync-mode":"automatic"}'
```
5. Проверка политик
```
	sudo rabbitmqctl list_policies
```

#### Скриншоты к Заданию 3

*Две очереди для кластера из двух нод*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p1.png)


*Запуск producer2.py на первой ноде (localhost)*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p2.png)


*Видим наличие сообщений в очередях первой и второй ноды*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p3.png)


*Запускаем consumer2.py на второй ноде и видим, что очереди обнулились*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p4.png)


*Запускаем теперь producer2.py (localhost) на второй ноде*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p5.png)


*Запускаем consumer2.py на первой ноде и очередь опусташается, данные выведены на экран*

![Commit Task3](https://github.com/AndrewZnamenskiy/RabbitMQ/blob/main/img/task3p6.png)


----

