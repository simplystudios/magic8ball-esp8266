import machine
import urequests
from machine import Pin, I2C
import ssd1306
import utime
import framebuf
import network

ssid = "wifi name" # your wifi name
password = "wifi password"# your wifi password 

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    pass

print("Connected to network:", ssid)
print("IP address:", sta_if.ifconfig()[0])

# Initialize the OLED display
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Initialize the button pin
button_pin = Pin(0, Pin.IN, Pin.PULL_UP)


def generate_response():
    # Make a request to the API
    response = urequests.get("https://nekos.life/api/v2/8ball")

    # Extract the response text from the JSON response
    text = response.json()['fact']

    return text


while True:
    if not button_pin.value():
        # Button is pressed, generate a new response
        text = generate_response()

        # Display the text on the OLED display
        buffer = bytearray(
            b"\x00\x00\x00\x00\x00\x03\x80\x00\x00<\xf8B\x01\xff\xfe\x84\x00\x7f\xe7\x80\x02\xff\xff\xc0\x03\xfe{T\x0f\x7f}\xf0\r\xdf\xfd\xf0\x1f\xb7\xefz?\xf0?X'\xf0\x0e\xbc7\xc2\xa6}\x1f\xc1\xc3\xf8v\xc2A\xf4}\xc3\xc3\xfc?\xc4\xc3\\i\xc6B\xdc?\xc6\xc3\xfc\x7f\xe3\x87|?\xa0\x03|?\xf8\x17\xfc\x1e\xff\xf7\xf0\nu\xff\xd9\x0f\xdf\xff\xb0\x07?\xff\xe1\x03\xfa\xff\xd0A\x97_\x83\x00\x7f\xfa \x00\x1f\xe8\x02\x00\x00\x02@\x00\x00\x00\x00")
        fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

    # Clear the OLED display
        oled.fill(0)
        oled.text(text, 0, 0)
        oled.blit(fb, 48, 10)
        oled.show()

        # Wait for a short period to debounce the button
        utime.sleep(0.5)
