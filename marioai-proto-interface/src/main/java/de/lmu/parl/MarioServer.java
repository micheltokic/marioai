package de.lmu.parl;

import java.io.*;
import java.net.*;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;


public class MarioServer {

    private final int port;
    private ServerSocket serverSocket;
    private final Controller controller;

    public MarioServer(int port) {
        this.port = port;
        this.controller = new Controller();

        try {
            this.serverSocket = new ServerSocket(port);
        } catch (IOException e) {
            System.out.println("unable to initialize server socket: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * handles a client connection until termination.
     * There can be only one client connection at a time.
     * @param in
     * @param out
     */
    private void handleConnection(InputStream in, OutputStream out) {
        while (true) {
            try {
                MarioMessage msg = MarioMessage.parseDelimitedFrom(in);
                if (msg == null) break;

                switch (msg.getType()) {
                    case INIT:
                        controller.handleInitMessage(msg);
                        break;
                    case RESET:
                        controller.handleResetMessage().writeDelimitedTo(out);
                        break;
                    case ACTION:
                        controller.handleActionMessage(msg).writeDelimitedTo(out);
                        break;
                    //case RENDER:
                    //    msgHandler.handleRenderMessage(msg);
                    //    break;
                }
            } catch (IOException e) {
                System.out.println("IOException occurred during client handling, closing connection");
                break;
            }
        }
    }

    /**
     * main loop; wait for incoming client connections
     */
    public void run() {
        System.out.println("Server is listening on port " + port);

        try {
            while (true) {
                Socket sock = serverSocket.accept();
                System.out.println("client connection established.");

                handleConnection(sock.getInputStream(), sock.getOutputStream());

                if (!sock.isClosed()) sock.close();

                System.out.println("client connection closed.");
            }

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getMessage());
            ex.printStackTrace();
        }

        System.out.println("Server terminated.");
    }

    public static void main(String[] args) {
        MarioServer server = new MarioServer(8080);
        server.run();
    }
}
