
def pullData():
    import json
    import requests
    
    url = "https://world.openfoodfacts.org/api/v0/product/{}.json"
    
    product_barcode = str(input("Product barcode?: ")).strip()
    
    url = url.format(product_barcode)
    
    response = requests.get(url)
    
    query = json.loads(response.text)
    
    # returns productName, brandName, product_barcode, and nutriments[]

    return query["product"]["product_name"], query["product"]["brands"], product_barcode, query["product"]["nutriments"]

# # # # # # # # # # # # # # # # # # # # # # # # 

#print("{} - {}".format(query["product"]["product_name"],query['product']['brands']))
#print("")

#for i in query['product']['nutriments']:
#    if '100g' in i:
#        print("{}: {}".format(i, str(query['product']['nutriments'][i])))
