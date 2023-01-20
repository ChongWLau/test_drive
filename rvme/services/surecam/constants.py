from model_utils import Choices


ALARM_TYPES = Choices(
    ('low', 'The accelerometer triggered a “low” event'),
    ('medium', 'The accelerometer triggered a “medium” event'),
    ('high', 'The accelerometer triggered a “high” event'),
    ('button', 'Button on the device was pressed'),
    ('input1', 'External cable input triggered an event')
)

EVENT_TYPES = ALARM_TYPES + Choices(
    ('start', 'Device started up'),
    ('stop', 'Device shutdown'),
    ('kl15_off', 'Ignition was turned off'),
    ('kl15_on', 'Ignition was turned on'),
    ('kl30_low', 'Power supply dropped below'),
    ('card_not_found', 'No SD card inserted'),
    ('flash_error', 'Internal flash overflow'),
    ('card_full', 'SD card full'),
    ('travel_start', 'The vehicle has been travelling for >10mph for at least 10 seconds'),
    ('travel_stop', 'The vehicle stopped travelling: speed dropped below 10mph for 10 seconds'),
    ('overspeed_start', 'The vehicle\'s speed went above the overspeed threshold'),
)
