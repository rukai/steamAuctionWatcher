#!/bin/env python3
import urllib.request
import urllib.parse
import re
import itertools

def getPage(item):
    item = item.strip() #Item not unicode safe
    response = urllib.request.urlopen(item)
    return response.read().decode("unicode_escape")


#get status of each auction item
def getAuctionItems():
    with open("auctionItems.txt") as itemsFile:
        for item in itemsFile:
            page = getPage(item)

            #grep items left, name and highest bid
            remaining = searchValue(r'<span class="sep_text">\s*?(\S*?) of this item remaining', page)
            name = searchValue(r'<div class="auction_game_name">\s*(.*?)\s*</div>', page)
            highestBid = searchValue(r'currently has the highest bid: (.*?) Gems', page)
            yield (remaining, name, highestBid, item)

#Takes a regex and returns the first group in the page
def searchValue(regex, page):
    result = re.search(regex, page)
    if result:
        return result.group(1)
    else:
        return "Error"

#Show status of each auction item
def displayAuctionItems(items):
    items = itertools.chain([("Remaining", "Name", "Highest Bid", "Dummy")], items)
    for remaining, name, highestBid, _ in items:
        print(remaining, name, highestBid, sep="-")

def main():
    #Show when current auction round ends.
    testData = getPage("http://steamcommunity.com/auction/item/1890-2014-Holiday-Profile")
    endDate = searchValue("This auction round will end at (.*?)\.", testData)
    print("Auction ends at", endDate) #Scrape from holiday profile
    
    #Show status of each auction item
    displayAuctionItems(getAuctionItems())

main()
