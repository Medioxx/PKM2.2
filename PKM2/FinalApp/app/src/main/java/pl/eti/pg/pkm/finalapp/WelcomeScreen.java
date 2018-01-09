package pl.eti.pg.pkm.finalapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;

/**
 * Created by EO NETWORKS on 03.12.2017.
 */

//screen wyswietlany po uruchomieniu aplikacji
public class WelcomeScreen extends AppCompatActivity {

    //zmienne definiujace obrazek oraz tekst pod nim
    private TextView textView;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //ustawienie aktualnego layoutu, zdefiniowanego jako activity_welcome
        setContentView(R.layout.activity_welcome);
        //ustawienie tekstu pod logo obrazka "Eti"
        textView = (TextView) findViewById(R.id.textView);
        //ustawienie obrazka jako logo "Eti"
        imageView = (ImageView) findViewById(R.id.imageView);
        //ustawienie animacji zdefiniowanej w pliku "welcometransition", animacja trwa 2s
        Animation myAnimation = AnimationUtils.loadAnimation(this, R.anim.welcometransition);
        textView.startAnimation(myAnimation);
        imageView.startAnimation(myAnimation);
        //tworzony jest wątek który, po upływie 4s przełącza bieżącą aktywność do klasy MainActivity. Tzn jest ładowany kolejny ekran
        final Intent intent = new Intent(this, MainActivity.class);
        Thread timer = new Thread(){
            public void run() {
                try {
                    sleep(4000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    startActivity(intent);
                    finish();
                }
            }
        };
        timer.start();
    }
}
