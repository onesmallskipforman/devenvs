#!/usr/bin/env python
# # coding=utf-8
# import sys
# from copy import deepcopy
# from time import sleep

from lifxlan import LifxLAN, TileChain, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE

OFF = [0, 0, 0, 0]

TEST_SCENE = [65491, 57671, 5898, 3500]

A1A = [0, 0, 11977, 1584]

ring_tilechain_colors = [[
    *[OFF]*63,
    A1A, # this last element is the top ring
]]

panel_tilechain_colors = [[
    *[A1A]*63,
    OFF, # this last element is the top ring
]]

def main():
    lifx = LifxLAN(3)
    lights = lifx.get_lights()
    lights_tilechain = [TileChain(i.get_mac_addr(), i.get_ip_addr()) for i in lights]

    for light in lights_tilechain:
        light.set_power(1)
        light.set_tilechain_colors(panel_tilechain_colors)
        # print(light.get_tilechain_colors())
        # print(light.get_tile_effect())

if __name__=="__main__":
    main()
