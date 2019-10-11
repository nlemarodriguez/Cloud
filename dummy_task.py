from crontab import CronTab

my_cron = CronTab(user='ec2-user')
job = my_cron.new(command='/home/ec2-user/crones/cron.sh >> /home/ec2-user/crones/myscript.log 2>&1')
job.minute.every(1)

my_cron.write()
