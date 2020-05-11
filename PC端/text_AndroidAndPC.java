import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

public class Test {

    final static Scanner s = new Scanner(System.in);

    public static void main(String[] args) {
        try {
            // 这句adb命令可以不用.执行下面两句也可以实现转发.只是为了避免重复开启service所以在转发端口前先stop一下   
            Runtime.getRuntime().exec("adb shell am broadcast -a NotifyServiceStop");
            //转发的关键代码
            Runtime.getRuntime().exec("adb forward tcp:8000 tcp:2580");
            Runtime.getRuntime().exec("adb shell am broadcast -a NotifyServiceStart");
            System.out.println("adb command success!");
            new Thread(){
                @Override
                public void run() {

                    try {
                        Socket socket = new Socket("127.0.0.1", 8000);
                        // 将信息通过这个对象来发送给Server
                        PrintWriter out = new PrintWriter(new BufferedWriter(
                                new OutputStreamWriter(socket.getOutputStream(),"utf-8")),
                                true);

                        // 接收服务器信息
                        BufferedReader in = new BufferedReader(
                                new InputStreamReader(socket.getInputStream(),"utf-8"));

                        //首先发送请求类型
                        String msg="我来自电脑！";
                        msg = s.nextLine();
                        out.println(msg);
                        out.flush();

                        msg = in.readLine();
                        System.out.println(msg);

                    } catch (UnknownHostException e) {
                        // TODO 自动生成的 catch 块
                        e.printStackTrace();
                    } catch (IOException e) {
                        // TODO 自动生成的 catch 块
                        e.printStackTrace();
                    }

                }
            }.start();
        } catch (IOException e) {
            // TODO 自动生成的 catch 块
            e.printStackTrace();
        }

    }
}
