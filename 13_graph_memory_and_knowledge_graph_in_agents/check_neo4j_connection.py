import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print(f"Connecting to: {NEO4J_URI}")

# Test Neo4j connection
def test_neo4j():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    try:
        driver.verify_connectivity()
        print("✅ Neo4j connection successful!")
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as count")
            print(f"Node count: {result.single()['count']}")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
    finally:
        driver.close()

test_neo4j()