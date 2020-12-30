# marioai
This is a clone of the MarioAI engine https://code.google.com/archive/p/marioai/downloads, where all dependencies are managed via Maven.

# Requirements
 * Java 1.8 with Maven plugin

# 1) Build and install MarioAI engine
 * cd marioai-engine
 * mvn clean package install
 * (optionally build JAR with sources): mvn source:jar install
 
# 2) Build and run Demo-Agent
 * cd marioai-demo-agent
 * mvn clean package
 * java -jar target/mario-demo-agent-0.0.2-SNAPSHOT.jar

