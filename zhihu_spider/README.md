# 简介

这是一个知乎爬虫，并不成熟，许多功能并不完善。

存在的意义是方便学习

# 目录结构及说明

```
|---- .idea  # PyCharm 集成开发环境配置目录
|---- ZhihuSpider  # Scrapy 自动生成目录
    |---- cookies  # 保存登录 cookies
    |---- spiders  # 保存各个爬虫主程序
        |---- __init__.py
        |---- zhihu.py  # 知乎爬虫主程序
    |---- utils
        |---- browsezhihu.py  # 用于登录知乎的辅助性程序
        |---- chromedriver.exe  # Chrome 驱动
        |---- Mofiki's Coordinate Finder.exe  # 坐标提取工具
    |---- __init__.py
    |---- items.py  # 所有的 items 都会去 pipelines
    |---- middlewares.py
    |---- pipelines.py  # 负责保存数据、内容
    |---- privacy.py  # 保存一些隐私数据字段
    |---- settings.py  # 项目级别的设置字段
|---- .gitignore
|---- LICENSE
|---- main.py  # 项目入口程序
|---- README.md
|---- scrapy.cfg  # Scrapy 生成的配置文件
|---- zhihu_answer.sql  # zhihu_answer 的表结构 sql 脚本，由 Navicat 自动生成，下同
|---- zhihu_question.sql
```

# 待做项

- [ ] 检查是否登录成功目前要手动判断，滑动验证也是手动的
- [ ] question 表里的 create_time 和 update_time 项并没有实现爬取