import RPi.GPIO as GPIO
import time, sys

# opening a file in apend mode to write output
f = open('flowmeteroutput.txt', 'a')

# constants start
inpt = 13
minutes = 0
constant = 0.006
time_new = 0.0
rpt_int = 10
global rate_cnt, tot_cnt
rate_cnt = 0
tot_cnt = 0
# constants end

# GPIO settings
GPIO.setup(inpt, GPIO.IN)
GPIO.setmode(GPIO.BOARD)

# adding pulse count
def pulse_cnt(inpt_pin):
   global rate_cnt, tot_cnt
   rate_cnt += 1
   tot_cnt += 1

# adding event detection for GPIO falling
GPIO.add_event_detect(inpt,GPIO.FALLING,
                       callback=pulse_cnt,bouncetime=10)

# output for waterflow detection
print('Water Flow - Approximate', str(time.asctime(time.localtime(time.time()))))
rpt_int=int(input('input desired report interval in second'))
print('Reports every','rpt_int','seconds')
print('Control C to exit')
f.write('\n water flow - Approximate - Reports every' + str(rpt_int)+' \tSeconds '+ time.asctime(time.localtime(time.time())))

# infinite loop
while True:
    time_new = time.time()+rpt_int
    rate_cnt = 0
    
    # loop for 60 seconds and break when there is an keyboard interrupt
    while time.time() <= time_new:
        if GPIO.input(inpt)!= 0:
            rate_cnt += 1
            tot_cnt += 1
        try:
            # print pulse detection 1-defines there is no flow
            # 0-defines there is pulse detected
            print(GPIO.input(inpt),end='')
        except KeyboardInterrupt:
            
            # closing activity
            print('\n CTRL C-existing nicely')
            GPIO.cleanup()
            f.close()
            print('Done')
            sys.exit()

    minutes += 1
    
    # calculating litres per minute flow through water measurement
    LperM = round(((rate_cnt*constant)/(rpt_int/60)),2)
    Totlit = round(tot_cnt*constant,1)
    print('\n liters/min',LperM,'c',rpt_int,'second sample')
    print('total liters',Totlit)
    print('time (min&clock) ', minutes ,'\t',
           time.asctime(time.localtime(time.time())),'\n')
    
    # writing all information to file
    f.write('\n liters/min:'+str(LperM))
    f.write('\t total liters:'+str(Totlit))
    f.write('\t time(min&clock):'+str(minutes)+'\t'+
             str(time.asctime(time.localtime(time.time()))))
    
# closing activity    
f.flush
GPIO.cleanup()
f.close()
print('Done')










