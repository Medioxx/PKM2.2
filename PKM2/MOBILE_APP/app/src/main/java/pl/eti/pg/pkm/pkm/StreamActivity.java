package pl.eti.pg.pkm.pkm;

import android.content.res.Configuration;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import com.github.niqdev.mjpeg.DisplayMode;
import com.github.niqdev.mjpeg.Mjpeg;
import com.github.niqdev.mjpeg.MjpegView;

import org.androidannotations.annotations.EView;

import butterknife.BindView;
import butterknife.ButterKnife;

/**
 * Created by adambelniak on 05.11.2017.
 */

public class StreamActivity extends AppCompatActivity {

    private static final int TIMEOUT = 5;

//    @BindView(R.id.mjpegViewDefault2)
    MjpegView mjpegView1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
//        mjpegView1 = (MjpegView) findViewById(R.id.mjpegViewDefault2);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stream);
        mjpegView1 = (MjpegView) findViewById(R.id.mjpegViewDefault2);

        ButterKnife.bind(this);
    }

    private String getPreference(String key) {
        return PreferenceManager
                .getDefaultSharedPreferences(this)
                .getString(key, "");
    }

    private DisplayMode calculateDisplayMode() {
        int orientation = getResources().getConfiguration().orientation;
        return orientation == Configuration.ORIENTATION_LANDSCAPE ?
                DisplayMode.FULLSCREEN : DisplayMode.FULLSCREEN;
    }

    private void loadIpCam() {
        Mjpeg.newInstance()
                .open("http://192.168.1.3:5000/video_feed", TIMEOUT)
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
    protected void onResume() {
        super.onResume();
        loadIpCam();
    }

    @Override
    protected void onPause() {
        super.onPause();
        mjpegView1.stopPlayback();
    }

}
