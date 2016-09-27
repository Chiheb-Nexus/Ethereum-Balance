#!/usr/bin/python3
#
#  This script use etherscan.io API to fetch Ethereum addresses balance.
#
#  Copyright 2016 Chiheb Nexus
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from urllib.request import Request, urlopen
from json import loads
import sys, argparse

class EthBalance:
    def __init__(self, args):
        self.API_TOKEN = "_Your_API_Token"
        self.explorer = "https://api.etherscan.io/api?module=account&action=balancemulti&address="

        parser = argparse.ArgumentParser(description = """
        This script fetch Ethereum addresses balance using etherscan.io API
        """)
        parser.add_argument('-F', '--file', help = "Path of the stored Ethereum addresses", required = True)
        parser.add_argument('-O', '--out', help = "Output file name", required = True)

        arguments = parser.parse_args()
        self.in_file, self.out_file = arguments.file, arguments.out

        self.check()

    def load(self, address = ""):
        try:
            url = self.explorer + address + "&tag=latest&apikey=" + self.API_TOKEN
            request = Request(url, headers= {'User-Agent' :\
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
            response = urlopen(request)
            data = loads(response.read().decode("utf8"))

            return data

        except Exception as e:
            print("Error occured during fetching data from etherscan", e)

    def parseInput(self, data_list = []):
        parsed_list, add, final_list = [], "", []
        parsed_list = [data_list[i:i + 20] for i in range(0, len(data_list), 20)]

        for i in parsed_list:
            for j in i:
                if j != "\n":
                    add += j.replace('\n', '') +','
            final_list.append(add[:len(add)-1])
            add = ""

        return final_list

    def check(self):
        try:
            with open(self.in_file, 'r') as input_file:
                d = input_file.readlines()
                parsed_list = self.parseInput(d)
                for multipleAdd in parsed_list:
                    data = self.load(address = multipleAdd)
                    for i in data["result"]:
                        # Trying to print the most accurate float values with 16 numbers after the point
                        print("%s  :  %.16f ETH" %(i["account"], float(i["balance"])/1000000000000000000))
                        with open(self.out_file, 'a') as out_file:
                            out_file.write("%s  :  %.16f ETH" %(i["account"], float(i["balance"])/1000000000000000000))

        except Exception as e:
            print("Error occured during file handling", e)

# test
if __name__ == '__main__':
    app = EthBalance(sys.argv[1:])
