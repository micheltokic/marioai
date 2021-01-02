package de.lmu.parl.action;

import static de.lmu.parl.proto.ActionProtos.Action;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.util.ReferenceCountUtil;

public class ActionHandler extends SimpleChannelInboundHandler<Action> {

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) { // (2)
        try {
            Action action = (Action) msg;
            int actionNumber = action.getActionNumber();
            System.out.println("Action Number: " + actionNumber);
            System.out.println(action.toString());

            Action res = Action.newBuilder().setActionNumber(1337).build();
            ctx.writeAndFlush(res);
    }
        catch (ClassCastException e) {
            ByteBuf in = (ByteBuf) msg;
            try {
                while (in.isReadable()) { // (1)
                    System.out.print((char) in.readByte());
                    System.out.flush();
                }
            } finally {
                ReferenceCountUtil.release(msg); // (2)
            }

        }

    }

    protected void channelRead0(ChannelHandlerContext channelHandlerContext, Action action) throws Exception {
        System.out.println(action);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) { // (4)
        // Close the connection when an exception is raised.
        cause.printStackTrace();
        ctx.close();
    }
}
