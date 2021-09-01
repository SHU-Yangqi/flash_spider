# flash_spider

与网页flash进行数据交互的爬虫

最近在玩保卫羊村，游戏是用flash做的，花了两天时间尝试做一个爬虫自动进行一些操作，网上很少有flash爬虫的教程，在这里总结一下遇到的坑

## 抓取数据包
flash使用的是amf数据格式进行的数据交换，这是一种二进制文件，传输效率高，用抓包软件抓取数据包得到如下结果

![image](https://user-images.githubusercontent.com/72846399/131700342-02312242-5a31-4001-a3c2-09c4a0700b80.png)

分析可知，我们只需要模拟浏览器发送对应格式的amf数据给服务器就可以了

数据包中的method就是我们要进行的操作，如图中的umap.pk_wolfs就是在前线打狼，这是游戏开发者命的名，我们只需要调用就好了

## 按AMF协议编码数据

python3使用的amf工具包为pyamf
安装时执行指令

    pip install Py3AMF

在GitHub中的pyamf项目中看到实例使用的时messaging.remoting类，我照例使用了一下，抓取到python发出的数据请求与浏览器发送的相去甚远，于是查看remoting和massaging的源码，发现发送的数据包只需要将一个类传进remoting.Request函数中转换成amf3格式就可以发送了。
遂编写一个MyMessage类用来组织羊村服务器所需的数据格式

## 获取gateway_key

分析数据包得知，我们发送的数据包需要一个gateway_key,这让我苦思冥想半天，最终在网页对应flash位置源码处找到了

![image](https://user-images.githubusercontent.com/72846399/131704169-4c258df4-7c3b-4af5-941a-7f5fd5f718ad.png)


## 模拟抓取苦工

在抓取苦工前打开抓包软件，再抓取苦工，分析数据包中method为user.catch_slave
于是只要将MyMessage类的数据成员method改为'user.catch_slave'就可以了

## 最终效果

可以通过苦工力量来筛选优质苦工，也可以设置定时抓苦工
完美！！

![image](https://user-images.githubusercontent.com/72846399/131704534-766075e5-bfa3-40bc-b494-cbde7ff4991b.png)

![image](https://user-images.githubusercontent.com/72846399/131704617-10a65b38-3385-4f42-a62f-ba7c7eb0ae92.png)

![image](https://user-images.githubusercontent.com/72846399/131704843-3a1dd731-dd84-43ae-b8ce-fac79523f527.png)

附上[游戏网址](http://tdsheep.tdsheepvillage.com/?)
