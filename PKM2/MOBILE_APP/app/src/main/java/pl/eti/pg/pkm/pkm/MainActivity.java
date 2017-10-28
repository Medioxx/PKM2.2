package pl.eti.pg.pkm.pkm;

import android.app.ProgressDialog;
import android.content.Context;
import android.media.MediaPlayer;
import android.net.Uri;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    private ProgressDialog progressDialog;
    private VideoView videoView;
    private ImageButton btnPlayPause;
    private String videoURL = "https://archive.org/download/ksnn_compilation_master_the_internet/ksnn_compilation_master_the_internet_512kb.mp4";
    private MyCustomAdapter dataAdapter = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        displayListView();

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

    private void displayListView() {

        List<Algorithm> algorithmsList = new ArrayList<Algorithm>();

        Algorithm algorithm = new Algorithm("Zajezdnia", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Przeszkody", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Twarz", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Banan", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Perony", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Ruch ręką", false);
        algorithmsList.add(algorithm);
        algorithm = new Algorithm("Ruch pociągu", false);
        algorithmsList.add(algorithm);

//        dataAdapter = new MyCustomAdapter(this, R.layout.activity_listview, algorithmsList);
        ListView listView = (ListView) findViewById(R.id.listView1);

        listView.setAdapter(dataAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                Algorithm algorithm = (Algorithm) adapterView.getItemAtPosition(position);
                Toast.makeText(getApplicationContext(), "Wybrano algorytm: " + algorithm.getName(), Toast.LENGTH_SHORT).show();


            }
        });


    }

    private class MyCustomAdapter extends ArrayAdapter<Algorithm> {
        private ArrayList<Algorithm> algorithmsList;

        public MyCustomAdapter(Context context, int textviewResourceid, ArrayList<Algorithm> algorithmsList) {
            super(context, textviewResourceid, algorithmsList);
            this.algorithmsList = new ArrayList<Algorithm>();
            this.algorithmsList.addAll(algorithmsList);

        }
    }

    private class ViewHolder {
        TextView code;
        CheckBox name;

    }


    public View getView(int position, View convertView, ViewGroup parent) {
        return null;
    }

}
