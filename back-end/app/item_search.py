
import requests
from bs4 import BeautifulSoup
import json
import time
from .item_scraper import item_scrape

# Sample list of ingredients the user wishes to avoid
undesired_ingredients = ['caramel']  # You can dynamically receive this list from user input

def check_ingredients(ingredients, undesired_ingredients):
    # Convert ingredients to lowercase for case-insensitive comparison
    ingredients_lower = ingredients.lower()

    # Check for any undesired ingredients in the ingredients list
    if ingredients_lower and not any(ingredient.lower() in ingredients_lower for ingredient in undesired_ingredients):
        return True  # No undesired ingredients found
    else:
        return False  # Undesired ingredient is present

def web_scrape(search_item):


    base_url = "https://www.walmart.com/search?q="
    url = f"{base_url}{search_item}"  # This should produce 'https://www.walmart.com/search?q=bread'
    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'cookie': 'abqme=true; _pxhd=f7fef0417af123cd90662d559902a27b163997e4c6d95573fb9ab9e83f83f876:16dcdaec-424a-11ef-9a27-0799341f58dc; _pxvid=170051d8-424a-11ef-8f52-32fc7c8b42eb; vtc=YwNwFUIXWC7lLOSTtzb7DI; QuantumMetricUserID=2c1b46288969ae0b6c235a2ad10d9517; wm_accept_language=en-US; __pxvid=c40a43f1-688d-11ef-9370-0242ac120002; salsify_session_id=9bc47afe-7057-4184-8055-baf5a183f126; adblocked=false; io_id=294cd38d-9128-4588-a1d6-bfac9cba7152; sptimestamp=1728845990823; dimensionData=944; ACID=f4d67440-3afb-4b13-bf8c-a5bc741bc9e6; _msit=77bc11f85af66057d1a116e6b247eadbwmart; _m=9; hasACID=true; userAppVersion=us-web-1.170.0-4aebb136688943aaf6196029e1a81c901f0427df-102212; _gid=GA1.2.865160891.1729968922; _ga=GA1.1.1233379695.1725983849; __hstc=195562739.d165a9e84ad2834ceb3108ffba220993.1729987912833.1729987912833.1729987912833.1; hubspotutk=d165a9e84ad2834ceb3108ffba220993; _fbp=fb.1.1729987913356.783286821228666244; _gcl_au=1.1.468209944.1729987913; _ga_LBH66B4XCL=GS1.1.1729987326.3.1.1729987933.0.0.0; mp_706c95f0b1efdbcfcce0f666821c2237_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A192cb50a308385-0d39c75355f2cf-26011951-144000-192cb50a308385%22%2C%22%24device_id%22%3A%20%22192cb50a308385-0d39c75355f2cf-26011951-144000-192cb50a308385%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fretaillink.login.wal-mart.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22retaillink.login.wal-mart.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22Is%20Internal%22%3A%20false%2C%22MP%20V%22%3A%20%22aurora%22%2C%22mart%22%3A%20%22US%22%2C%22internationalSeller%22%3A%20false%2C%22userLocale%22%3A%20%22en-US%22%2C%22isGSE%22%3A%20false%2C%22New%20Navigation%22%3A%20false%2C%22%24search_engine%22%3A%20%22google%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Oct+26+2024+19%3A13%3A53+GMT-0500+(Central+Daylight+Time)&version=202308.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b7a18e4f-8c88-4446-a2fc-021f358368c9&interactionCount=1&landingPath=NotLandingPage&groups=C0007%3A1%2CC0008%3A1%2CC0009%3A1%2CC0010%3A1&AwaitingReconsent=false&geolocation=US%3BTX; OptanonAlertBoxClosed=2024-10-27T00:13:53.378Z; brwsr=59a0af7f-93f8-11ef-9581-891a026fc9d5; IR_PI=59a0af7f-93f8-11ef-9581-891a026fc9d5%7C1729988034601; _ga_1LB22TM2MG=GS1.1.1729988034.1.1.1729988192.60.0.0; _intlbu=false; _shcc=US; assortmentStoreId=2599; hasLocData=1; bm_mi=3406B92F81FEA8F932BF9BECA71E3A9B~YAAQ7BjQFz0faceSAQAA/P9wzhnLF9SDF/wJiu2RtBNmTPk68PA6bZCPubcH7mJgpkuE4CWwi2PqAAcY8Bs90PI5ScdCPvIGl9uYDM9AyM9873Ssk5NxASTAJRa4l1JDDEDCKo/uHbr4LQg8YeXJCwyDuXWGK+9NUgxosIpPBlfi3lW3UdLGkA2KbcH0gJSaBXkuzw/gelaIOYTfVzdryuWu1J5WjBUAAUBawNwEKHByfW24cX52+YiUoa+HX1B2vD4etFImrrzgugMi3m04dPlYTXliucm08KHCPNNEAp9M0W+Erp+aB0hjub78Nt+TWlijAOPW~1; pxcts=32008aa4-9472-11ef-856f-42e831c8c054; ak_bmsc=CC60FA0E71BEA518F3A01B2DEAE5C221~000000000000000000000000000000~YAAQ7BjQF8khaceSAQAAIgRxzhkNWFrzYfi425O1AuUdPTOyFzsX1B2aanZ4Ee9R0kmEpfcpW9VPSoKynhzIPFD6wo8fdYa417dvXVlJNKlSKijAtORQkDcNAq/YZlpslmg6NUky2zHVIzLZyQRrVyVfEE+QqXRDNtM0otpIa51FxYrbfy5HEI/YNv+9r+D6fDUyndAqCJjmATMsSgXQHDc8rYaAJeFrePKGBt+5/lgMrbyZzYhiOZZhXJ9zhallxWpGB8CkAN+A2rJGTGkE3f1Y2Scc9QtbYbxIO0c0wnVlKYoeJ0h834NywA8OmONpupGemrmFjcQCKf3rPrYwPYLN57BvYCVwArb7Z6fhgDxNALAhBcQAerHSeY6TqzWwC65bP0DOreRIx7lx6FRAYuMk91XdUxwU0J/uwbUw8Y35N6V2w/tj1INxl7hH5CkXZEGVoZuQQSfl6vTGC+vwnbd44WtUGLkTHVfQEVKlOZrQMld0DgLU; AID=wmlspartner%3Dwmtlabs%3Areflectorid%3D22222222220220085369%3Alastupd%3D1730040373142; com.wm.reflector=%22reflectorid%3A22222222220220085369%40lastupd%3A1730040373142%40firstcreate%3A1728845986887%22; auth=MTAyOTYyMDE4aIOBhULU1HrA2LuvD8x0Ei7tnX7PbBrWDbNcoJd0TadgbTRShCZ3KychkEs54qaxWo55hf7gNrx%2BPi%2FtYpYz9jfd%2BhJ5nyMF9CuxrvjJMkjRpGGQH7%2FK9SiPkTqcIsoY767wuZloTfhm7Wk2KcjygmNzsF5Ho8U7SJCh0TVScOltEnBX25oVpio%2BgfdmAsMNDmWCDdZcDiqfVK0agtBRtAo%2BcuBzw3BRC1x13bKyXOsUMk70P8glgOEpLOprhDfMJ0tmvH1FCaN9tZDh4SCrHbnA4%2Bol9jRab0a8siZujq1kkzMGkP4WSA%2FvEBL3b95oiJdRwb2R6rSqDIb%2BC1cs4ydJX5a8DN5gg0lJ%2B9QUsciCluD0Fc4%2B5ieBLREbvJ%2Bg8KLB4LbUlOuSctMQNtSoHpE5WBBdZBCyKnCQAR7o6eg%3D; bstc=bWFA5CipSRi1qDVGhKtR1c; mobileweb=0; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=-G6VK|5qF5V|99IVe|9jX6b|C76br|EfoLY|FB6K6|NbX17|OQe8n|Sgh15|T_-Pl|UUz4s|_-4YS|_iY7J|a_jm5|dwc1S|fdm-7|gzgHW|k6DSt|pRup4|yHzXk|ycAS6; exp-ck=5qF5V199IVe29jX6b1EfoLY1FB6K61NbX172OQe8n2Sgh151T_-Pl2UUz4s1_iY7J3a_jm52fdm-71gzgHW2k6DSt1pRup41ycAS62; _astc=ee107dda177e259fc11ab3ba2d2454f6; xpm=1%2B1730040373%2BYwNwFUIXWC7lLOSTtzb7DI~%2B0; locGuestData=eyJpbnRlbnQiOiJQSUNLVVAiLCJpc0V4cGxpY2l0IjpmYWxzZSwic2Vjb25kYXJ5SW50ZW50IjoiaW5zdG9yZSIsInN0b3JlSW50ZW50IjoiUElDS1VQIiwibWVyZ2VGbGFnIjp0cnVlLCJpc0RlZmF1bHRlZCI6ZmFsc2UsInBpY2t1cCI6eyJub2RlSWQiOiIyNTk5IiwidGltZXN0YW1wIjoxNzI5NjIyNzA3MTY2LCJzZWxlY3Rpb25UeXBlIjoiTFNfU0VMRUNURUQiLCJzZWxlY3Rpb25Tb3VyY2UiOiJJUF9TTklGRkVEX0JZX0xTIn0sInNoaXBwaW5nQWRkcmVzcyI6eyJ0aW1lc3RhbXAiOjE3Mjk2MjI3MDcxNjYsInR5cGUiOiJwYXJ0aWFsLWxvY2F0aW9uIiwiZ2lmdEFkZHJlc3MiOmZhbHNlLCJwb3N0YWxDb2RlIjoiNzgyNDkiLCJkZWxpdmVyeVN0b3JlTGlzdCI6W3sibm9kZUlkIjoiMjU5OSIsInR5cGUiOiJERUxJVkVSWSIsInRpbWVzdGFtcCI6MTcyOTYxNTE5NDU3MywiZGVsaXZlcnlUaWVyIjpudWxsLCJzZWxlY3Rpb25UeXBlIjoiTFNfU0VMRUNURUQiLCJzZWxlY3Rpb25Tb3VyY2UiOiJJUF9TTklGRkVEX0JZX0xTIn1dLCJjaXR5IjoiU2FuIEFudG9uaW8iLCJzdGF0ZSI6IlRYIn0sInBvc3RhbENvZGUiOnsidGltZXN0YW1wIjoxNzI5NjIyNzA3MTY2LCJiYXNlIjoiNzgyNDkifSwibXAiOltdLCJtc3AiOnsibm9kZUlkcyI6WyI1MTQ2IiwiMzA1NyIsIjEyMzUiLCI0MTYyIiwiNDEzMSIsIjMxMDciLCIyODY0IiwiNTE0NSJdLCJ0aW1lc3RhbXAiOjE3Mjk2MjI3MDcxNTZ9LCJtcERlbFN0b3JlQ291bnQiOjAsInZhbGlkYXRlS2V5IjoicHJvZDp2MjpmNGQ2NzQ0MC0zYWZiLTRiMTMtYmY4Yy1hNWJjNzQxYmM5ZTYifQ%3D%3D; locDataV3=eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJQSUNLVVAiLCJwaWNrdXAiOlt7Im5vZGVJZCI6IjI1OTkiLCJkaXNwbGF5TmFtZSI6IlNhbiBBbnRvbmlvIFN1cGVyY2VudGVyIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiNzgyNDkiLCJhZGRyZXNzTGluZTEiOiI1NTU1IERFIFpBVkFMQSBSRCIsImNpdHkiOiJTYW4gQW50b25pbyIsInN0YXRlIjoiVFgiLCJjb3VudHJ5IjoiVVMifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjI5LjU2NDU5MiwibG9uZ2l0dWRlIjotOTguNTk2MDgxfSwic2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwidW5TY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJzdG9yZUhycyI6IjA2OjAwLTIzOjAwIiwiYWxsb3dlZFdJQ0FnZW5jaWVzIjpbIlRYIl0sInN1cHBvcnRlZEFjY2Vzc1R5cGVzIjpbIlBJQ0tVUF9CQUtFUlkiLCJQSUNLVVBfU1BFQ0lBTF9FVkVOVCIsIlBJQ0tVUF9DVVJCU0lERSIsIkFDQyIsIlBJQ0tVUF9JTlNUT1JFIiwiQUNDX0lOR1JPVU5EIl0sInRpbWVab25lIjoiQ1NUIiwic3RvcmVCcmFuZEZvcm1hdCI6IldhbG1hcnQgU3VwZXJjZW50ZXIiLCJzZWxlY3Rpb25UeXBlIjoiTFNfU0VMRUNURUQifSx7Im5vZGVJZCI6IjUxNDYifSx7Im5vZGVJZCI6IjMwNTcifSx7Im5vZGVJZCI6IjEyMzUifSx7Im5vZGVJZCI6IjQxNjIifSx7Im5vZGVJZCI6IjQxMzEifSx7Im5vZGVJZCI6IjMxMDcifSx7Im5vZGVJZCI6IjI4NjQifSx7Im5vZGVJZCI6IjUxNDUifV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6MjkuNTY4NSwibG9uZ2l0dWRlIjotOTguNjEzOSwicG9zdGFsQ29kZSI6Ijc4MjQ5IiwiY2l0eSI6IlNhbiBBbnRvbmlvIiwic3RhdGUiOiJUWCIsImNvdW50cnlDb2RlIjoiVVNBIiwiZ2lmdEFkZHJlc3MiOmZhbHNlLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQ2hpY2FnbyIsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJUWCJdfSwiYXNzb3J0bWVudCI6eyJub2RlSWQiOiIyNTk5IiwiZGlzcGxheU5hbWUiOiJTYW4gQW50b25pbyBTdXBlcmNlbnRlciIsImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsibm9kZUlkIjoiMjU5OSIsImRpc3BsYXlOYW1lIjoiU2FuIEFudG9uaW8gU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI3ODI0OSIsImFkZHJlc3NMaW5lMSI6IjU1NTUgREUgWkFWQUxBIFJEIiwiY2l0eSI6IlNhbiBBbnRvbmlvIiwic3RhdGUiOiJUWCIsImNvdW50cnkiOiJVUyJ9LCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6MjkuNTY0NTkyLCJsb25naXR1ZGUiOi05OC41OTYwODF9LCJ0eXBlIjoiREVMSVZFUlkiLCJzY2hlZHVsZWRFbmFibGVkIjpmYWxzZSwidW5TY2hlZHVsZWRFbmFibGVkIjpmYWxzZSwiYWNjZXNzUG9pbnRzIjpbeyJhY2Nlc3NUeXBlIjoiREVMSVZFUllfQUREUkVTUyJ9XSwiaXNFeHByZXNzRGVsaXZlcnlPbmx5IjpmYWxzZSwiYWxsb3dlZFdJQ0FnZW5jaWVzIjpbIlRYIl0sInN1cHBvcnRlZEFjY2Vzc1R5cGVzIjpbIkRFTElWRVJZX0FERFJFU1MiLCJBQ0MiXSwidGltZVpvbmUiOiJDU1QiLCJzdG9yZUJyYW5kRm9ybWF0IjoiV2FsbWFydCBTdXBlcmNlbnRlciIsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCJ9LCJpc2dlb0ludGxVc2VyIjpmYWxzZSwicmVmcmVzaEF0IjoxNzMwMDQzOTc0OTU4LCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6ZjRkNjc0NDAtM2FmYi00YjEzLWJmOGMtYTViYzc0MWJjOWU2In0%3D; wmlh=a683bbe873049a4223d780ba3de3cd3e5e25706b416c2484c760483590a967e9; _px3=cce53039c407193e25bad9f6562d96e913f4c420d2b2ecf4ef10c17165377728:TSNJhOrMKeQwFwapZJpusOODkV4X8aye8yqrRXUE/TCcjUOQarZxBm/kYHRlZzxWjrZ+YpHs1LU+IOt/7yOr7g==:1000:FX+gpvWW2Qngn3GgRPbx9RKq7ae3PL2+ai8KpP8/ksCOrfp3H7sMai9QRo6iNGayQ/DmOFk8oY5lJVongdcquw73VqjTMQns/xReNAPY1idpAsYaYb3es9bzAPQInfNlRO9Wf6BAiEAUu/zsk5CkuzVzBCF2Z8/ZbhbaI3vx8i3x4brjPoztwvQxF2lbDJMEN3qx1znBPKjprolC/Dhw+26jTbWTE6OfVC3n0ST/arg=; __cf_bm=nqdjQV5sS.GoJYmMtpS9iAWUYgvFwIMb_MkQGPwnUjU-1730040375-1.0.1.1-fpoz7W19r36Q0pw58.JFQudvhk_mOwOuQTpXlRrRrMEeqHMO.XcvPmkaNrncJyk_ei7.rADP2NF.NkNVDtKbRcVaOFMHPJbMxTbUTfA38_s; if_id=FMEZARSF8Dd5YwcJLPjxGGlPxmoG90Tw9StPnXQhHG2O7oRXxYIkMw4IdCziRWaRBI4KMFFYAArcFXjBFT7uXR/4t3IQ6CDF/KsPY3pXfQZXcFSNBoqR4wNd74/n0wzj+rBOuZnj/HZHzB1/0jk6PDCH9p1J7l4kmUEliLft8+rzpjh8VfDOUl+6iH5Aa1xUs3kD/UEKVNqSUyOSh+dc3hG/3v6BSMv9FpDkItzjPL5lquKdvzxBzW+ENSPKCti8DQDsNmMbWEnUBrS9O97HCKvZ; TS016ef4c8=0142d85684eaa21b2d6849ee6c83a7a361ebc938b050d3c4cef1fca581393f269a2670ca5cb37b690941d94f4648af1dd65b981228; TS01f89308=0142d85684eaa21b2d6849ee6c83a7a361ebc938b050d3c4cef1fca581393f269a2670ca5cb37b690941d94f4648af1dd65b981228; TS8cb5a80e027=08e47d199cab20007a5109f1eb8d4391b343e481fb621e59f36761d39de3e5bba474c7d77f6c745108a41c2171113000fd20661b21b1a716a8828c9092be060b887baa992d63a8e08ad6ba22a7e5b090026b434a8ee63a5fbdaa56e38aab1010; _pxde=65f16951745e9c96f8f9536f5a0e03381561aa75c7301cd9da5cda0a4fa3b3e5:eyJ0aW1lc3RhbXAiOjE3MzAwNDAzODEzMzV9; xptwj=uz:c64ee03ac5d223192c0d:uy6oEd9xKTdLwf5hxVSuCvg4D384McHD2tvqzBSeDFR2wD7QKMb7JBg7/HORFSdS5BXhoCeXXlT0vBD0a1N+YXhzXE0nbe8/oRrdCCyybRHO3Vvrmhi/QZkUMiUCaSUykR+IK3UovkJqqpREAo6M8sqW/i1YpJXAl3DuNwqfQF5zt4aHVa2jnf10PUopDvcj3GqP1IZunAGSxPnZCi7x/66ihc694hZLMMbeURwv2g==; akavpau_p2=1730040981~id=265e020e55ce4ed4bbc31b56344e7a5e; xptc=_m%2B9~assortmentStoreId%2B2599; xptwg=4277157042:1A698782F71EE30:41920D4:19DABA93:8DE481EF:472C26C0:; TS012768cf=01cf30a731e008e1b52151d2e0ae55cd602eb5fecea911670cd5c92f30e858616081eb179153a77a640145faf31105bb9932b2df60; TS01a90220=01cf30a731e008e1b52151d2e0ae55cd602eb5fecea911670cd5c92f30e858616081eb179153a77a640145faf31105bb9932b2df60; TS2a5e0c5c027=087fad2231ab2000e2c6513c498078eac315e032d67a26405f9226e85ac054ccd62cd52b6151fb200834fbea5a1130001ec503ca9730a91c3afbf228900f2fe2ef42308dad7bd23b9ac2823cfb010899345f9be5f69670bc5170f5110380d4c1; bm_sv=79A0C36F82918910BC49D9EA37153C01~YAAQ7BjQF65CaceSAQAAGENxzhni6bQxrK2+pI8mwt/+v/OyAnw5ZfUQjEELEECzoak3tFZvnx1zW9zsv1Bi3/4HNgpKeiHkNd8B/eeTPrws1bo4kj4oZfYxgJVl01KkXuwFIttc6tfftI4WqS+zZ2nMJNIo6G3nX3h4RJ2wZwKDxEQB7FuIQoY1uFzMcNqtn1xO27jX0x5gyeQf09VC39hnTkdWwR2QGVXmpG1Qlgmcu2Pctg2pTg6z6N9boR97uNw=~1',
      'downlink': '10',
      'dpr': '1.25',
      'priority': 'u=0, i',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-mobile': '?1',
      'sec-ch-ua-platform': '"Android"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
    }
    r = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')

    script = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})

    products = []  # Moved products here to ensure it's defined if script is not found
    if script:
        jsonInfo = json.loads(script.text)
        item_initialData = jsonInfo['props']['pageProps']['initialData']['searchResult']['itemStacks']

        if isinstance(item_initialData, list) and len(item_initialData) > 0:
            first_item_stack = item_initialData[0]

            if 'items' in first_item_stack:
                item_iresult = first_item_stack['items']

                if isinstance(item_iresult, list):
                    products = []
                    for item in item_iresult:
                        canonical_url = item.get('canonicalUrl')
                        if not canonical_url:  # Skip item if canonicalUrl is None
                            print("No canonicalUrl found for item.")
                            continue  # Move to the next item

                        product = {
                            "canonical_url": canonical_url,
                            "thumbnail_url": item.get('imageInfo').get('thumbnailUrl'),
                            "product_name": item.get('name'),
                            "product_price": item.get('price')
                        }

                        # Call item_scrape only if canonical_url exists
                        ingredients = item_scrape(search_item, canonical_url)
                        if check_ingredients(ingredients, undesired_ingredients) and check_ingredients(item.get('name'),undesired_ingredients):
                            products.append(product)
                            print(f"Canonical URL: {canonical_url}")

                    print("\nAll products:")
                    print("\n".join(str(product) for product in products))
                    return products
                else:
                    print("Expected a list for 'items', but got:", type(item_iresult))
            else:
                print("'items' key not found in the first item stack.")
        else:
            print("Expected itemStacks to be a non-empty list.")
    else:
        print("No script tag found with id '__NEXT_DATA__'.")