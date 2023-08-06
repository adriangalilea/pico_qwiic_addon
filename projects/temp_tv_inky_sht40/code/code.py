# to-do
# Add humidity and thermometer icons and remove % and C
# Add quotes mode

# bmps added from flaticon

import alarm
import time
import board
print("Waking up")
# Create an alarm for 60 seconds from now, and also a pin alarm.
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 20)
pin_alarm = alarm.pin.PinAlarm(pin=board.GP12, value=False)

from time import sleep, localtime
import busio
import adafruit_sht4x
i2c = busio.I2C(board.GP27, board.GP26)
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

def sensor_data():
    # calibrated sensor data
    # check for every sensor
    temperature, relative_humidity = sht.measurements
    temperature = temperature - 2
    return temperature, relative_humidity

import displayio
import terminalio
import adafruit_uc8151d
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
displayio.release_displays()

# inky
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
epd_cs = board.GP17
epd_dc = board.GP20
epd_reset = board.GP21
epd_busy = board.GP26

#buttons
from digitalio import DigitalInOut, Direction, Pull

button_a = DigitalInOut(board.GP12)
button_a.direction = Direction.INPUT
button_a.pull = Pull.UP

button_b = DigitalInOut(board.GP13)
button_b.direction = Direction.INPUT
button_b.pull = Pull.UP

button_c = DigitalInOut(board.GP14)
button_c.direction = Direction.INPUT
button_c.pull = Pull.UP

WIDTH = 296
HEIGHT = 128
chart_width = WIDTH - int(WIDTH /4) - 1
half_width = WIDTH // 2

# Create the displayio connection to the display pins
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
sleep(1)  # Wait a bit

display = adafruit_uc8151d.UC8151D(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    rotation=270,
    black_bits_inverted=False,
    color_bits_inverted=False,
    grayscale=True,
    refresh_time=1,
)

font = bitmap_font.load_font("/Roboto-Regular-50-55.bdf")
font_small = bitmap_font.load_font("/Roboto-Regular-25-25.bdf")

BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0xFF00FF
dark_gray = 0x555555
light_gray = 0xAAAAAA
FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE
# Set a background
background_bitmap = displayio.Bitmap(296, 128, 1)

#methods for storing and retrieving data
# to-do OSError: [Errno 30] Read-only filesystem
# not using any of the following until fixed
import json
def store_data_to_file():
    global temperatures, humidities
    data = {"temperatures": temperatures, "humidities": humidities}
    
    with open("data.json", "w") as f:
        json.dump(data, f)

def retrieve_data_from_file():
    global temperatures, humidities
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            temperatures = data["temperatures"]
            humidities = data["humidities"]
    except Exception as e:
        temperature, relative_humidity = sensor_data()
        temperatures.append(temperature)
        humidities.append(relative_humidity)
        store_data_to_file()
    return temperatures, humidities

temperatures = []
humidities = []

# temperatures, humidities = retrieve_data_from_file()

temperature, relative_humidity = sensor_data()
temperatures.append(temperature)
humidities.append(relative_humidity)
# I add them twice because it gives a point of reference in the chart so you know if temp is higher or lower than when the device was powered on
temperatures.append(temperature)
humidities.append(relative_humidity)

def check_sensor(temperature, relative_humidity):
    global temperatures, humidities, start_time
    # if more than one hour has passed we add the data to the list
    elapsed_time = time.monotonic() - start_time
    if elapsed_time >= 3600:
        start_time = time.monotonic()
        print("an hour has elapsed, adding a record")
        temperatures.append(temperature)
        humidities.append(relative_humidity)
        # if there's more than 24 items we pop the oldest one
        if len(temperatures)>24:
            temperatures.pop(0)
        if len(humidities)>24:
            humidities.pop(0)
    else: # else we update this hour record
        temperatures[-1] = temperature
        humidities[-1] = relative_humidity

margin = 10
chart_height = HEIGHT - (margin * 2)
chart_width = chart_width - 16

def refresh_display():
    if display.time_to_refresh == 0:
        display.refresh()
        print('refreshed')
    else:
        print(f'Waiting for {display.time_to_refresh}')

def display_data(mode):
    global temperatures, humidities
    # Create a display group for our screen objects
    g = displayio.Group()
    records = ""
    if mode == "temperature":
        records = temperatures
    if mode == "humidity":
        records = humidities
    # to-do add quotes mode
    if mode == "both":
        records = temperatures
    
    if mode == "temperature" or mode == "humidity":
        #draw screen elements
        g.append(RoundRect(0, 0, WIDTH, HEIGHT, 4, fill=0xFFFFFF, outline=0x000000))
        g.append(RoundRect(WIDTH - int(WIDTH /4), 0, int(WIDTH /4), int(HEIGHT / 2)+1, 3, fill=WHITE, outline=BLACK))
        g.append(RoundRect(WIDTH - int(WIDTH /4), int(HEIGHT / 2), int(WIDTH /4), int(HEIGHT / 2), 3, fill=WHITE, outline=BLACK))


        # Draw simple text using the built-in font into a displayio group
        temperature_label = label.Label(font_small, text="", color=FOREGROUND_COLOR)
        temperature_label.anchor_point = (0.5, 0.5)
        temperature_label.anchored_position = (WIDTH /8 * 7, HEIGHT // 4)
        g.append(temperature_label)

        humidity_label = label.Label(font_small, text="", color=FOREGROUND_COLOR)
        humidity_label.anchor_point = (0.5, 0.5)
        humidity_label.anchored_position = (WIDTH /8 * 7, HEIGHT // 4 * 3)
        g.append(humidity_label)
    
        print(records)
        max_record = int(max(records)) + 1
        min_record = int(min(records)) - 1
        
        data_group = displayio.Group()
        # we check if there isn't much spread on temps so we increase for the chart grid lines range
        if max_record - min_record < 6:
            max_record = int(max_record + 3)
            min_record = int(min_record - 3)

        # Calculate the increment for the y-axis grid
        increment = 2
        while max_record - min_record > increment * 10:
            increment += 2

        # Draw the y-axis grid
        for i in range(min_record, max_record, increment):
            temp_line = Line(0, int(HEIGHT - (i - min_record) * HEIGHT / (max_record - min_record)), int(chart_width) + 2, int(HEIGHT - (i - min_record) * HEIGHT / (max_record - min_record)), GREY)
            data_group.append(temp_line)
            temp_label = label.Label(terminalio.FONT, text=str(i), color=BLACK)
            temp_label.x = chart_width + 4
            temp_label.y = int(HEIGHT - (i - min_record) * HEIGHT / (max_record - min_record))
            data_group.append(temp_label)

        # Draw the lines connecting the temperature values
        for i in range(len(records) - 1):
            temp_line = Line(int((i + 1) * chart_width / len(records)), int(HEIGHT - (records[i] - min_record) * HEIGHT / (max_record - min_record)), int((i + 2) * chart_width / len(records)), int(HEIGHT - (records[i + 1] - min_record) * HEIGHT / (max_record - min_record)), GREY)
            data_group.append(temp_line)

        # Draw the circles for the temperature values
        for i in range(len(records)):
            temp_circle = Circle(int((i + 1) * chart_width / len(records)), int(HEIGHT - (records[i] - min_record) * HEIGHT / (max_record - min_record)), 1, fill=BLACK, outline=BLACK)
            data_group.append(temp_circle)
        
        temperature_label.text = f"{temperature:0.1f}˚"
        humidity_label.text = f"{relative_humidity:0.0f}%"
        g.append(data_group)
        display.show(g)
        refresh_display()
    else:
        # Define the values for the temperature and humidity data
        min_temp = min(temperatures)
        current_temp = temperatures[-1]
        max_temp = max(temperatures)

        min_humidity = min(temperatures)
        current_humidity = temperatures[-1]
        max_humidity = max(temperatures)
        
        g.append(RoundRect(0, 0, WIDTH, HEIGHT, 4, fill=0xFFFFFF, outline=0x000000))
        g.append(RoundRect(0, 0, half_width, HEIGHT, 3, fill=WHITE, outline=BLACK))
        g.append(RoundRect(half_width, 0, WIDTH, HEIGHT, 3, fill=WHITE, outline=BLACK))

        # Create a Label for the minimum temperature data
        min_temp_label = label.Label(font_small, text=f"{min_temp:.1f}˚", color=GREY)
        min_temp_label.anchor_point = (0.5, 1)
        min_temp_label.anchored_position = (WIDTH // 4, HEIGHT // 4)
        g.append(min_temp_label)

        # Create a Label for the current temperature data
        current_temp_label = label.Label(font, text=f"{current_temp:.1f}˚", color=BLACK)
        current_temp_label.anchor_point = (0.5, 0.5)
        current_temp_label.anchored_position = (WIDTH // 4, HEIGHT // 2)
        g.append(current_temp_label)

        # Create a Label for the maximum temperature data
        max_temp_label = label.Label(font_small, text=f"{max_temp:.1f}˚", color=GREY)
        max_temp_label.anchor_point = (0.5, 0)
        max_temp_label.anchored_position = (WIDTH // 4, HEIGHT // 4 * 3)
        g.append(max_temp_label)

        # Create a Label for the minimum humidity data
        min_humidity_label = label.Label(font_small, text=f"{min_humidity:.0f}%", color=GREY)
        min_humidity_label.anchor_point = (0.5, 1)
        min_humidity_label.anchored_position = (WIDTH // 4 * 3, HEIGHT // 4 )
        g.append(min_humidity_label)

        # Create a Label for the current humidity data
        current_humidity_label = label.Label(font, text=f"{current_humidity:.0f}%", color=BLACK)
        current_humidity_label.anchor_point = (0.5, 0.5)
        current_humidity_label.anchored_position = (WIDTH // 4 * 3, HEIGHT // 2)
        g.append(current_humidity_label)

        # Create a Label for the maximum humidity data
        max_humidity_label = label.Label(font_small, text=f"{max_humidity:.0f}%", color=GREY)
        max_humidity_label.anchor_point = (0.5, 0)
        max_humidity_label.anchored_position = (WIDTH // 4 * 3, HEIGHT // 4 * 3)
        g.append(max_humidity_label)
        display.show(g)
        refresh_display()
        print(len(g))
    for i in range(len(g)):
        g.pop(-1)


#Hour labels are too crammed, disabling them until better way of showing or number of hours is reduced
#     hour_label = label.Label(terminalio.FONT, text=str(i), color=BLACK)
#     hour_label.x = int((i + 1) * chart_width / len(temperatures) - hour_label.width // 2)
#     hour_label.y = int(HEIGHT -10)
#     g.append(hour_label)

sleep_time = 31
last_time = time.monotonic() #for checking if we can update display
start_time = time.monotonic() #for checking if an hour elapsed

mode = "both"
prev_mode = "both"

display_data(mode)

while True:
    if not button_a.value:
        print("button a press, mode set to temperature")
        mode = "temperature"
        sleep(0.1)
    if not button_b.value:
        print("button b press, mode set to quotes")
        mode = "both"
        sleep(0.1)
    if not button_c.value:
        print("button c press, mode set to rh")
        mode = "humidity"
        sleep(0.1)
#     print(g.index)
    #actualizamos si el tiempo ha pasado o hemos pedido un modo nuevo
    if time.monotonic() - last_time > sleep_time or not mode == prev_mode:
        prev_mode = mode
        last_time = time.monotonic()
        temperature, relative_humidity = sensor_data()
        #we update the data every 30 minutes
        check_sensor(temperature, relative_humidity)
        display_data(mode)