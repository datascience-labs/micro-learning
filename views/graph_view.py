from neo4j import GraphDatabase
from config.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class GraphView:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def insert_node(self, node):
        label = node.__class__.__name__  # 예: VideoSegment, Channel
        props = node.dict()
        query = f"MERGE (n:{label} {{id: $id}}) SET n += $props"
        with self.driver.session() as session:
            session.run(query, id=props['id'], props=props)

    def insert_relationship(self, from_id, to_id, rel_type, from_label="Node", to_label="Node"):
        query = f"""
        MATCH (a:{from_label} {{id: $from_id}}), (b:{to_label} {{id: $to_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, from_id=from_id, to_id=to_id)
