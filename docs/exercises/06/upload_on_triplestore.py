import os

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from SPARQLWrapper import POST, SPARQLWrapper

BASE_DIR = os.path.join(os.path.dirname(__file__))

g = Graph()

SCHEMA = Namespace("http://schema.org/")
g.bind("schema", SCHEMA)

data = pd.read_csv(os.path.join(BASE_DIR, 'data', 'rdf_source.csv'))

for index, row in data.iterrows():
    wine_uri = URIRef(f"http://example.org/wine/{row['Wine_ID']}")
    
    g.add((wine_uri, RDF.type, SCHEMA.Product))
    g.add((wine_uri, SCHEMA.isProductOf, Literal(row['Winery'], datatype=XSD.string)))
    year = row['Year']
    if year != "N.V.":
        g.add((wine_uri, SCHEMA.productionDate, Literal(year, datatype=XSD.gYear)))
    g.add((wine_uri, SCHEMA.productID, Literal(row['Wine_ID'], datatype=XSD.string)))
    g.add((wine_uri, SCHEMA.name, Literal(row['Wine'], datatype=XSD.string)))
    g.add((wine_uri, SCHEMA.ratingValue, Literal(row['Rating'], datatype=XSD.float)))
    g.add((wine_uri, SCHEMA.reviewCount, Literal(row['Reviews'], datatype=XSD.integer)))
    g.add((wine_uri, SCHEMA.price, Literal(row['Price'], datatype=XSD.float)))
    g.add((wine_uri, SCHEMA.isFromRegion, Literal(row['Region'], datatype=XSD.string)))
    g.add((wine_uri, SCHEMA.material, Literal(row['Primary_Grape'], datatype=XSD.string)))
    g.add((wine_uri, SCHEMA.isNatural, Literal(row['Natural'], datatype=XSD.boolean)))
    g.add((wine_uri, SCHEMA.category, Literal(row['Style'], datatype=XSD.string)))
    g.add((wine_uri, SCHEMA.countryCode, Literal(row['Country_Code'], datatype=XSD.string)))

sparql = SPARQLWrapper("http://192.168.10.57:9999/blazegraph/sparql")
sparql.setMethod(POST)
sparql.setQuery("INSERT DATA {" + g.serialize(format='nt') + "}")
sparql.query()