from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal

HERE = Path(__file__).parent

# lookit GRAFFF
g = Graph()

# Namespace
EX = Namespace("http://example.org/game#")
g.bind("ex", EX)

# Convenience functions
def p(data_string:str) -> None:
    prefix_string = """@prefix ex: <http://example.org/game#> .
                        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."""
    g.parse(data=prefix_string + "\n\n" +data_string, format="turtle")

def q(data_string:str) -> None:
    prefix_string = """PREFIX ex: <http://example.org/game#>"""
    construct_query = prefix_string + data_string
    return g.query(construct_query)


def qri(query_string):
    inferred_graph = q(query_string)
    for triple in inferred_graph:
        g.add(triple)

def query_pickups():
    data_string = """
    CONSTRUCT {
        ex:Inventory ex:contains ?item .
    }
    WHERE {
        ?pickup a ex:Pickup ;
            ex:item ?item;
            ex:target ex:Inventory . 
        
        ?item a ex:PickupableItem .
    }"""
    qri(data_string)

# Classes
g.add((EX.Room, RDF.type, RDFS.Class))

p("ex:Event a rdfs:Class .")


# Properties
p("ex:contains a rdfs:Property ;" \
                "rdfs:domain ex:Room ;" \
                "rdfs:range ex:Item .")


# Characters
p("ex:Character a rdfs:Class .")
p("ex:Protagonist a ex:Character .")

# Events
p("ex:Pickup a rdfs:Event .")
p("ex:actor a rdfs:Property ;" \
                "rdfs:domain ex:Pickup ;" \
                "rdfs:range ex:Character .")
p("ex:item a rdfs:Property ;" \
                "rdfs:domain ex:Pickup ;" \
                "rdfs:range ex:PickupableItem .")
p("ex:source a rdfs:Property ;" \
                "rdfs:domain ex:Pickup ;" \
                "rdfs:range ex:Room .")
p("ex:target a rdfs:Property ;" \
                "rdfs:domain ex:Pickup ;" \
                "rdfs:range ex:Room .")



p("ex:Door a rdfs:Class .")
p("ex:Openable a rdfs:Class .")
p("ex:Door a ex:Openable .")

p("ex:canBeOpenedBy a rdfs:Property ;"\
                "rdfs:domain ex:Door ;" \
                "rdfs:range rdfs:Resource .")


p("ex:Item a rdfs:Class .")
p("ex:SturdyObject a rdfs:Class .")

p("ex:PickupableItem a rdfs:Class ; rdfs:subClassOf ex:Item .")
p("ex:Poker a ex:PickupableItem .")
p("ex:Poker a ex:SturdyObject .")
p("ex:BookOfMatches a ex:PickupableItem .")
p("ex:DiningRoom a ex:Room .")
p("ex:DiningRoom ex:contains ex:Poker .")
p("ex:Pickup1 a ex:Pickup ;" \
"ex:actor ex:Protagonist;" \
"ex:item ex:Poker;" \
"ex:source ex:DiningRoom;" \
"ex:target ex:Inventory.")

p("ex:Kitchen a ex:Room .")
p("ex:Kitchen ex:contains ex:BookOfMatches .")

p("ex:Pickup2 a ex:Pickup ;" \
"ex:actor ex:Protagonist;" \
"ex:item ex:BookOfMatches;" \
"ex:source ex:Kitchen;" \
"ex:target ex:Inventory.")

p("ex:Pantry a ex:Room .")
p("ex:Trapdoor a ex:Door .")
p("ex:Pantry ex:contains ex:Trapdoor .")

p("ex:Trapdoor ex:canBeOpenedBy ex:SturdyObject .")


query_pickups()

if (EX.Inventory, EX.contains, EX.Poker) in g:
    print("Inv has Pok")
else:
    print("ting went wrong")

print([row.item.split("#")[1] for row in q("""
SELECT ?item
WHERE {
ex:Inventory ex:contains ?item .
?item a ?item2 .                                          
ex:Trapdoor ex:canBeOpenedBy ?item2 .
}
""")])

print([row.item.split("#")[1] for row in q("""
  SELECT ?item
  WHERE {
    ex:Inventory ex:contains ?item .
  }
  """)])


# g.parse(data=ttl_data, format="turtle")

# File Handling
ttl_file = HERE / "game_kg.ttl"

# for s, p, o in g:
#     print(f"s:{s}, p:{p}, o:{o}")





# Loading
# g2 = Graph()
# g2.parse(ttl_file, format="turtle")
# print(g2)
# print(g)

# Storage
g.serialize(destination=ttl_file, format="turtle")