from ipwhois import IPWhois
import geoip2.database
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import sys

GEOLOCATOR = Nominatim()

def getlatlongIP(ip):
    result = IPWhois(ip)
    try:
        ret = result.lookup_rdap(depth=1)
        # print(ret)
        try:
            # Get the MaxMind geo data for the query.
            # I do not redistribute the GeoLite2 database, download
            # GeoLite2-City.mmdb from:
            # https://dev.maxmind.com/geoip/geoip2/geolite2/
            mm_reader = geoip2.database.Reader('GeoLite2-City.mmdb')

            # Query the database.
            mm_response = mm_reader.city(ret['query'])
            lat = mm_response.location.latitude
            lng = mm_response.location.longitude
            return lat, lng

        # Generic exception. Need to determine all raised and update handling.
        # geoip2.errors.AddressNotFoundError, TypeError, etc.
        except Exception as e:
            print(e)
            pass
    except:
        pass

def getlatlngReg(ip):
    result = IPWhois(ip)
    try:
        ret = result.lookup_rdap(depth=1)
        tmp_objects = ret['objects'].items()
        for ent_k, ent_v in tmp_objects:

            if sys.version_info >= (2, 7):
                for addr_k, addr_v in enumerate(ent_v['contact']['address']):

                    try:
                        addr = addr_v['value'].replace('\n', ' ')
                        location = GEOLOCATOR.geocode(addr)
                        print(location)
                        lat = location.latitude
                        lng = location.longitude
                        return lat, lng
                    except Exception as e:
                        print(e)
                        pass
    except Exception as e:
        print(e)
        pass

def measuredistance(ip1, ip2):
    ip1geo = getlatlongIP(ip1)
    ip2geo = getlatlongIP(ip2)
    distance = vincenty(ip1geo, ip2geo).meters
    return distance

# This is temporary. We are testing the script by feeding the IP Addresses by prompting the user
# AUTOMATION:
# Need to make the IP Addresses read from a file so we can
# start performing total distance travelled for a given prime user in a given stipulated time
# provided we have the IP Addresses

ip1 = raw_input('Enter First IP Address:')
ip2 = raw_input('Enter Second IP Address:')
distance = measuredistance(ip1, ip2)
print 'Distance in meters is {}'.format(distance)