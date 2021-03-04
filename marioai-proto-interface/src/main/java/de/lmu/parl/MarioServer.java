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
            this.serverSocket = new ServerSocket(port, 0, InetAddress.getByName(null));
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
    private void handleConnection(BufferedInputStream in, BufferedOutputStream out) {
        while (true) {
            try {
                MarioMessage msg = MarioMessage.parseDelimitedFrom(in);
                if (msg == null) break;

                switch (msg.getType()) {
                    case INIT:
                        controller.handleInitMessage(msg).writeDelimitedTo(out);
                        out.flush();
                        break;
                    case RESET:
                        controller.handleResetMessage().writeDelimitedTo(out);
                        out.flush();
                        break;
                    case ACTION:
                        controller.handleActionMessage(msg).writeDelimitedTo(out);
                        out.flush();
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

                BufferedInputStream in = new BufferedInputStream(sock.getInputStream());
                BufferedOutputStream out = new BufferedOutputStream(sock.getOutputStream());
                handleConnection(in, out);
                //handleConnection(sock.getInputStream(), sock.getOutputStream());

                if (!sock.isClosed()) sock.close();

                System.out.println("client connection closed.");
                controller.reset();
            }

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getMessage());
            ex.printStackTrace();
        }

        System.out.println("Server terminated.");
    }

    public static void main(String[] args) {
        int port = 8080;

        // simple parsing of --port / -p argument.
        // For more args use something like commons-cli    http://blog.wenzlaff.de/?p=12952
        if (args.length == 2 && (args[0].equals("--port") || args[0].equals("-p"))) {
            try {
                port = Integer.parseInt(args[1]);
            } catch (NumberFormatException e) {
                System.out.println("Error: unable to parse parameter ".concat(args[0]));
                System.exit(1);
            }
        }

        MarioServer server = new MarioServer(port);
        server.run();
    }
}
