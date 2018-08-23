# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: liheng
# @time: 18-8-21 上午11:40

# broker 可以选择 Redis 对redis比较熟悉
broker_url = "redis://127.0.0.1/14"

# 执行的结果 保存在 redis的 15号库中
result_backend = "redis://127.0.0.1/15"