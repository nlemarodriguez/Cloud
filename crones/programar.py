from crontab import CronTab
my_cron = CronTab(user='ec2-user')
print('prueba')
job = my_cron.new(command='/home/ec2-user/Grupo01/crones/cron.sh >> /home/ec2-user/Grupo01/crones/myscript.log 2>&1', comment='1')
job.minute.every(1)
 
my_cron.write()