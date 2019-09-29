#!/usr/bin/python3

import solaredge

class SolarData:
    def __init__(self, api_key, site_id):
        self.__solarEdge = solaredge.Solaredge(api_key)
        self.__data = self.__solarEdge.get_overview(site_id)

    def lifetime_energy(self):
        return round(self.__data["overview"]["lifeTimeData"]["energy"]/1000, 2)
    
    def last_year_energy(self):
        return round(self.__data["overview"]["lastYearData"]["energy"]/1000, 2)
    
    def last_day_energy(self):
        return round(self.__data["overview"]["lastDayData"]["energy"]/1000, 2)
    
    def current_power(self):
        return round(self.__data["overview"]["currentPower"]["power"]/1000, 2)
    
    
    



