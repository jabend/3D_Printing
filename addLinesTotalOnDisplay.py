# Cura PostProcessingPlugin
# Author:   Amanda de Castilho
# Date:     August 28, 2018
# Modified: Jon Abend
# Date:     March 18, 2019

# Description:  This plugin inserts a line at the start of each layer,
#               M117 - displays the filename and layer height to the LCD
#               Alternatively, user can override the filename to display alt text + layer height

from ..Script import Script
from UM.Application import Application
import re

class addLinesTotalOnDisplay(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Layer Info Display",
            "key": "LayerInfoLCD",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "name":
                {
                    "label": "text to display:",
                    "description": "By default the current filename will be displayed on the LCD. Enter text here to override the filename and display something else.",
                    "type": "str",
                    "default_value": ""
                }
            }
        }"""

    def execute(self, data):
        if self.getSettingValueByKey("name") != "":
            name = self.getSettingValueByKey("name")
        else:
            name = Application.getInstance().getPrintInformation().jobName
        lcd_text = "M117 "
        i = 1
        line_count = ""
        for layer in data:
            display_text = lcd_text + str(i)
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if "TIME:" in line.upper():
                    seconds = int(re.sub(r'^;TIME:','',line))
                    m, s = divmod(seconds, 60)
                    h, m = divmod(m, 60)
                    time = "%dh %02dm" % (h, m)
                if "COUNT:" in line.upper():
                    line_count = re.sub(r'^.*COUNT: *',r'',line)
                if line.startswith(";LAYER:"):
                    line_index = lines.index(line)
                    line_percent = "{0:.1%}".format(float(i)/float(line_count))
                    lines.insert(line_index + 1, display_text + '/' + line_count + ' ' + line_percent + ' ' + time)
                    i += 1
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines

        return data
