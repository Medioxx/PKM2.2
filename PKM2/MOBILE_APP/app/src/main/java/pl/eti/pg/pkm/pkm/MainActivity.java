package pl.eti.pg.pkm.pkm;

import android.app.ProgressDialog;
import android.media.MediaPlayer;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.VideoView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    private ProgressDialog progressDialog;
    private VideoView videoView;
    private ImageButton btnPlayPause;
    private String videoURL = "https://archive.org/download/ksnn_compilation_master_the_internet/ksnn_compilation_master_the_internet_512kb.mp4";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        videoView = (VideoView)findViewById(R.id.videoView);
        btnPlayPause = (ImageButton) findViewById(R.id.btn_play_pause);
        btnPlayPause.setOnClickListener(this);

    }

    @Override
    public void onClick(View view) {
        progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setMessage("Please wait...");
        progressDialog.setCanceledOnTouchOutside(false);
        progressDialog.show();
        try {
            if (!videoView.isPlaying()) {
                Uri uri = Uri.parse(videoURL);
                videoView.setVideoURI(uri);
                videoView.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                    @Override
                    public void onCompletion(MediaPlayer mediaPlayer) {
                        btnPlayPause.setImageResource(R.drawable.ic_play);
                    }
                });
            } else {
                videoView.pause();
                btnPlayPause.setImageResource(R.drawable.ic_play);
                progressDialog.dismiss();
            }
        } catch (Exception ex){

        }

        videoView.requestFocus();
        videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {

            @Override
            public void onPrepared(MediaPlayer mediaPlayer) {
                progressDialog.dismiss();
                mediaPlayer.setLooping(true);
                videoView.start();
                btnPlayPause.setImageResource(R.drawable.ic_pause);
            }
        });
    }
}
