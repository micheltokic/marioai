cd marioai-engine/
mvn install
cd ../marioai-server/
mvn install
cd ..
cp marioai-server/target/marioai-server-0.2-jar-with-dependencies.jar gym-marioai/gym_marioai/server/
