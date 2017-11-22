package pl.eti.pg.pkm.pkm.drawers;

import android.app.ProgressDialog;
import android.content.Intent;
import android.content.res.Configuration;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.Toast;
import android.widget.VideoView;

import com.github.niqdev.mjpeg.DisplayMode;
import com.github.niqdev.mjpeg.Mjpeg;
import com.github.niqdev.mjpeg.MjpegView;

import butterknife.ButterKnife;
import pl.eti.pg.pkm.pkm.R;

public class StreamDrawer extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener, View.OnClickListener{

    DrawerLayout drawer;
    NavigationView navigationView;
    Toolbar toolbar = null;
    private Button btnPlayPause;
    private ProgressDialog progressDialog;
    private String videoURL = "http://192.168.1.3:5000/video_feed";
    private static final int TIMEOUT = 5;
    MjpegView mjpegView1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stream_drawer);
        btnPlayPause = (Button) findViewById(R.id.play_stop_btn);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        mjpegView1 = (MjpegView) findViewById(R.id.mjpegViewDefault2);
        ButterKnife.bind(this);
    }

    @Override
    public void onClick(View view) {
        progressDialog = new ProgressDialog(StreamDrawer.this);
        progressDialog.setMessage("Please wait...");
        progressDialog.setCanceledOnTouchOutside(false);
        progressDialog.show();
        try {
            if (!mjpegView1.isStreaming()) {
                loadIpCam();

            } else {
                mjpegView1.stopPlayback();
                mjpegView1.clearStream();
            }
        } catch (Exception ex) {

        }
        progressDialog.dismiss();

    }


    private DisplayMode calculateDisplayMode() {
        int orientation = getResources().getConfiguration().orientation;
        return orientation == Configuration.ORIENTATION_LANDSCAPE ?
                DisplayMode.FULLSCREEN : DisplayMode.FULLSCREEN;
    }

    private void loadIpCam() {
        Mjpeg.newInstance()
                .open(videoURL, TIMEOUT)
                .subscribe(
                        inputStream -> {
                            mjpegView1.setSource(inputStream);
                            mjpegView1.setDisplayMode(calculateDisplayMode());
                            mjpegView1.showFps(true);

                        },
                        throwable -> {
                            Log.e(getClass().getSimpleName(), "mjpeg error", throwable);
                            Toast.makeText(this, "Error", Toast.LENGTH_LONG).show();
                        });
    }



    @Override
    protected void onPause() {
        super.onPause();
        mjpegView1.stopPlayback();
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.stream_drawer, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();
        switch (id) {
            case R.id.nav_stream:
                Intent streamIntent = new Intent(StreamDrawer.this, StreamDrawer.class);
                startActivity(streamIntent);
                break;
            case R.id.nav_algorithms:
                Intent algorithmsIntent = new Intent(StreamDrawer.this, AlgorithmsDrawer.class);
                startActivity(algorithmsIntent);
                break;
            case R.id.nav_control:
                Intent controlIntent = new Intent(StreamDrawer.this, ControlDrawer.class);
                startActivity(controlIntent);
                break;
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
