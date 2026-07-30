import java.lang.reflect.Field;

public class Expose {

    public static void main(String[] args) {
        Confidential message = new Confidential("top secret text");
        Field secretField = null;
        try {
            secretField = Confidential.class.getDeclaredField("secret");
        }
        catch (NoSuchFieldException e) {
            System.err.println(e);
            System.exit(1);
        }
        secretField.setAccessible(true); // 破除访问限制！
        try {
            String wasHidden = (String) secretField.get(message);
            System.out.println("message.secret = " + wasHidden);
        }
        catch (IllegalAccessException e) { 
            // 调用 setAccessible(true) 之后不会发生
            System.err.println(e);
        }   
    }
}
