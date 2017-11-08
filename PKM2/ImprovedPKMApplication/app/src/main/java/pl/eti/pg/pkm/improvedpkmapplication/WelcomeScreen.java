package pl.eti.pg.pkm.improvedpkmapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;

import pl.eti.pg.pkm.improvedpkmapplication.drawers.StreamDrawer;

/**
 * Created by EO NETWORKS on 07.11.2017.
 */

public class WelcomeScreen extends AppCompatActivity{
    private TextView textView;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);
        textView = (TextView) findViewById(R.id.textView);
        imageView = (ImageView) findViewById(R.id.imageView);
        Animation myAnimation = AnimationUtils.loadAnimation(this, R.anim.welcometransition);
        textView.startAnimation(myAnimation);
        imageView.startAnimation(myAnimation);
        final Intent intent = new Intent(this, StreamDrawer.class);
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
