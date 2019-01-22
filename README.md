# 汽车之家口碑频道爬虫(A型,B型,SUV车型)

## 调度器
使用scrapy_redis进行url的去重及完成断点续爬功能.

## 存储器
使用sqlalchemy连接mysql数据库进行数据去重存储.

## 配置重爬
在爬虫完成后，进入redis数据库，删除db0数据库里的koubei:dupefilter，再重新运行爬虫，则爬虫将进行重爬.
