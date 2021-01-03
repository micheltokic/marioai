package de.lmu.parl.handlers;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;
import static de.lmu.parl.proto.MarioProtos.Init;
import static de.lmu.parl.proto.MarioProtos.Action;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.util.ReferenceCountUtil;

public class MessageHandler extends SimpleChannelInboundHandler<MarioMessage> {

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) { // (2)
        try {
            MarioMessage marioMessage = (MarioMessage) msg;

            switch (marioMessage.getType()) {
                case INIT:
                    Init init = marioMessage.getInit();
                    Init resInit = Init.newBuilder().mergeFrom(init).build();
                    MarioMessage resMsg = MarioMessage.newBuilder()
                            .setType(MarioMessage.Type.INIT)
                            .setInit(resInit).build();
                    ctx.writeAndFlush(resMsg);
                    break;
                case ACTION:
                    Action action = marioMessage.getAction();
                    Action resAction = Action.newBuilder().mergeFrom(action).build();
                    ctx.writeAndFlush(resAction);
            }
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

    protected void channelRead0(ChannelHandlerContext channelHandlerContext, MarioMessage msg) throws Exception {
        System.out.println(msg);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) { // (4)
        // Close the connection when an exception is raised.
        cause.printStackTrace();
        ctx.close();
    }
}
