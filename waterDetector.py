import RPi.GPIO as GPIO
import time
import smtplib
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
# photoresistor connected to adc #0
photo_ch = 0
#port init
def init():
       GPIO.setwarnings(False)  
       GPIO.cleanup()  #clean up at the end of your script
       GPIO.setmode(GPIO.BCM) #to specify which pin numbering system

         # set up the SPI interface pins
       GPIO.setup(SPIMOSI,  GPIO.OUT)
       GPIO.setup(SPIMISO, GPIO.IN)
       GPIO.setup(SPICLK, GPIO.OUT)
       GPIO.setup(SPICS, GPIO.OUT)
          #read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
       if ((adcnum > 7) or (adcnum < 0)):
                     return -1
       GPIO.output(cspin, True)
       GPIO.output(clockpin, False) # start clock low
       GPIO.output(cspin, False) # bring CS lo
       commandout = adcnum
       commandout |= 0x18 # start bit + single-ended bit
       commandout <<= 3 # we only need to send 5 bits here
       for i in range(5):
               if (commandout & 0x80):
                     GPIO.output(mosipin, True)
               else:
                     GPIO.output(mosipin, False)
               commandout <<= 1
               GPIO.output(clockpin, True)
               GPIO.output(clockpin, False)
       adcout = 0
       # read in one empty bit, one null bit and 10 ADC bits
       for i in range(12):
                 GPIO.output(clockpin, True)
                 GPIO.output(clockpin, False)
                 adcout <<= 1
                 if (GPIO.input(misopin)):
                         adcout |= 0x1
       GPIO.output(cspin, True)
       adcout >>= 1 # first bit is 'null' so drop it
       return adcout
def main():
         init()
         time.sleep(2)
         print ("will start detec water level\n")
         loop_counter = 0
         while True:
              adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
              if adc_value < 10:
                  print ("no water\n")
                  time.sleep(1)
              elif adc_value>10 and adc_value<200:
                  print("water level:"+str("%.1f"%(adc_value/200.*100))+"%\n")
                  loop_counter += 1
                  print(loop_counter)
                   #print "adc_value= " +str(adc_value)+"\n"
                  time.sleep(1)
                  if loop_counter == 1:
                       server = smtplib.SMTP('smtp.gmail.com', 587)
                       server.starttls()
                       server.login("sender email", "sender password")
                       msg = "it sure is wet down here!"
                       server.sendmail("sender email", "receiver email", msg)
                       server.quit()
if __name__ == '__main__':
        try:
                   main()
        except KeyboardInterrupt:
               pass
GPIO.cleanup()
