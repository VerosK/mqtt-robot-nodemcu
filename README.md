# μPython code for small robot
 
## Upload to the board

 * Upload this to NodeMCU board with `ampy`

 * Change `config.py` to the right MQTT server.

 * Connect to WiFi  
   ```python
   import network
   wifi = network.WLAN()
   wifi.active(True)       
   # wifi.scan()           # scan WiFi networks when needed
   wifi.connect('robot', '12345678')
   # wifi.isconnected()    # check WiFi connection       
   ```
       

 * Reboot the board
 
## Diagnostics
 
 * robot moves both wheels after successfull connection to WiFi
 
 * otherwise open terminal and connect to the board


## hardware needed

 * NodeMCU board with ESP8266
 
 * DOIT Motor shield for NodeMCE [(guide)](https://cdn.hackaday.io/files/8856378895104/user-mannual-for-esp-12e-motor-shield.pdf)
 
 * Two DC motors with wheels
 
 * lunch box
 
## HOW TO: change WiFi

 * Open terminal (Putty, Picocom, Minicom or whatever). speed: 115200
 
 * Press `Ctrl+C` to stop running Python code. Prompt `>>>` should appear.
 
 * Run code from the first section
 
## Links
 
 Web joystick is available at https://github.com/VerosK/mqtt-robot-webdriver/
