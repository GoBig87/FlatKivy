# Copyright (c) 2019 Artem S. Bulgakov
#
# This file is distributed under the terms of the same license,
# as the Kivy framework.

"""
Tool for updating Iconic font
=============================

Downloads archive from https://github.com/Templarian/MaterialDesign-Webfont and
updates font file with icon_definitions.
"""

import ast
import json

if __name__ == "__main__":
    with open('selection.json') as f:
        selection = json.load(f)

    icon_dict = {}
    for icon in selection['icons']:
        print(icon['properties']['name'])
        icon_dict[icon['properties']['name']] = []
        for index, attr in enumerate(icon['attrs']):
            # This skips empty and ones missing fill entries
            if attr and attr['fill'] != 'none':
                print(attr)
                rgb_color_255 = ast.literal_eval(attr['fill'].strip('rgb'))
                color_code = [i / 255 for i in rgb_color_255]
                if 'opacity' in attr.keys():
                    opacity = attr['opacity']
                else:
                    opacity = 1
                color_code.append(opacity)
                if 'codes' in icon['properties'].keys():
                    hex_num = hex(icon['properties']['codes'][index])[2:]

                else:
                    hex_num = str(hex(icon['properties']['code']))[2:]
                hex_code = f'\\u{hex_num.upper()}'
                icon_tuple = (color_code, hex_code)
                icon_dict[icon['properties']['name']].append(icon_tuple)
            pass
        pass
    pass

    with open('icon_definition2.py', "w") as f:
        icon_dict_string = json.dumps(icon_dict, indent=4, sort_keys=True)
        f.write(icon_dict_string)
