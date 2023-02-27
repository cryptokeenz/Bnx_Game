# Bnx_Game

修改 login 函数中的 private_key 即可导入私钥

<img width="746" alt="1677538906470" src="https://user-images.githubusercontent.com/108882370/221708958-15194c5e-3603-4824-859d-3ad3c118ce31.png">

根据自己地址情况修改 (0,5) 中的数字

![image](https://user-images.githubusercontent.com/108882370/221710806-f0939364-5964-49bb-88ac-4798f5a9e055.png)


默认关闭随机延迟函数，如果出现连接被服务器强行关闭情况，可以开启

![image](https://user-images.githubusercontent.com/108882370/221709105-cfd7baad-2204-4c21-a809-8072a03b03fa.png)

可以自行设置 start_date 时间，需要按、年、月、日、时、秒格式设置

![image](https://user-images.githubusercontent.com/108882370/221709611-67480a39-75c8-4cc4-9d4e-93dcdc8accae.png)

其他时间参数：

```
interval 间隔调度，参数如下：
    weeks (int) – 间隔几周
    days (int) – 间隔几天
    hours (int) – 间隔几小时
    minutes (int) – 间隔几分钟
    seconds (int) – 间隔多少秒
    start_date (datetime|str) – 开始日期
    end_date (datetime|str) – 结束日期
    timezone (datetime.tzinfo|str) – 时区
```
```
cron参数如下：
    year (int|str) – 年，4位数字
    month (int|str) – 月 (范围1-12)
    day (int|str) – 日 (范围1-31)
    week (int|str) – 周 (范围1-53)
    day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – 时 (范围0-23)
    minute (int|str) – 分 (范围0-59)
    second (int|str) – 秒 (范围0-59)
    start_date (datetime|str) – 最早开始日期(包含)
    end_date (datetime|str) – 最晚结束时间(包含)
    timezone (datetime.tzinfo|str) – 指定时区
```
