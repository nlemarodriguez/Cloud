from crontab import CronTab
my_cron = CronTab(user='dn.lecca')
print('prueba')
job = my_cron.new(command='/home/SIS/dn.lecca/crones/cron.sh >> /home/SIS/dn.lecca/crones/myscript.log 2>&1', comment='1')
job.minute.every(1)
 
my_cron.write()