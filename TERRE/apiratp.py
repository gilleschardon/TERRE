#!/usr/bin/python3
# -*- coding: utf-8 -*-

from zeep import Client
import datetime
import pytz

# fuseau horaire
tz = pytz.timezone('Europe/Paris')

# retourne le temps actuel en utilisant le format de l'API
def now_ratp():
    d = datetime.datetime.now(tz=tz)
    return '%u%02u%02u%02u%02u' % (d.year, d.month, d.day, d.hour, d.minute)

# vérifie si un train peu être pris
def check_margin(time, margin):
    now = now_ratp()

    now_minute = 60 * int(now[-4:-2]) + int(now[-2:])
    time_minute = 60 * int(time[-4:-2]) + int(time[-2:])

    if now[1:-4] == time[1:-4]:
        return now_minute + margin <= time_minute
    else:
        # autour de minuit
        return now_minute + margin <= time_minute + 24*60

def strdate(date):
    return date[8:10] + ':' + date[10:]

class apiratp:

    def __init__(self, wsiv):
        self.ratp_client = Client(wsiv)

        self.line_t = self.ratp_client.get_type('ns0:Line')
        self.station_t = self.ratp_client.get_type('ns0:Station')
        self.direction_t = self.ratp_client.get_type('ns0:Direction')
        self.mission_t = self.ratp_client.get_type('ns0:Mission')

    # retourne les missions RER
    def missions_rer(self, line, station, sens, margin=0, otherstops = [], maxlines = 0):

        oline = self.line_t(id=line)
        ostation = self.station_t(line = oline, name=station)
        odirection = self.direction_t(sens = sens)

        missions = self.ratp_client.service.getMissionsNext(station=ostation, direction=odirection)

        missionlist = []

        if maxlines > 0:
            missions.missions = missions.missions[:maxlines]

        for m in missions.missions:
            mission = {}

            mission['code'] = m['code']
            if not m.stationsStops[0]:
                mission['stops'] = "nostop"
            elif check_margin(m.stationsDates[0], margin):
                mission['stops'] = "catchable"
            else:
                mission['stops'] = "noncatchable"
            mission['id'] = m.id
            mission['terminus'] = m.stations[1].name
            mission['message'] = m.stationsMessages[0]
            if len(m.stationsDates) > 0:
                mission['date'] = strdate(m.stationsDates[0])
            else:
                mission['date'] = ''

            oline = self.line_t(id=line)
            omission = self.mission_t(line = oline, id=m.id)
            M = self.ratp_client.service.getMission(omission)

            L = len(otherstops)
            train_stops = [False] * L;
            for s in M.mission.stations:
                for j  in range(L):
                    if s.name == otherstops[j]:
                        train_stops[j] = True
            mission['otherstops'] = train_stops


            missionlist.append(mission)

        return missionlist

    # retourne les missions bus et metro
    def missions_busmetro(self, line, station, sens, maxlines = 0):

        oline = self.line_t(id=line)
        ostation = self.station_t(line = oline, name=station)
        odirection = self.direction_t(sens = sens)

        missions = self.ratp_client.service.getMissionsNext(station=ostation, direction=odirection)

        missionlist = []

        if maxlines > 0:
            missions.missions = missions.missions[:maxlines]

        for m in missions.missions:
            if len(m.stations) > 1:
                mission = {}

                mission['terminus'] = m.stations[1].name
                mission['message'] = m.stationsMessages[0]
                if len(m.stationsDates) > 0:
                    mission['date'] = strdate(m.stationsDates[0])
                else:
                    mission['date'] = ''

                missionlist.append(mission)
        return missionlist
