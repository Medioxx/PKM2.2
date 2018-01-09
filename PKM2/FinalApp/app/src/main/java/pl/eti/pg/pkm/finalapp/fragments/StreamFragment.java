package pl.eti.pg.pkm.finalapp.fragments;

import android.app.ProgressDialog;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.NavigationView;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.github.niqdev.mjpeg.DisplayMode;
import com.github.niqdev.mjpeg.Mjpeg;
import com.github.niqdev.mjpeg.MjpegView;

import butterknife.ButterKnife;
import pl.eti.pg.pkm.finalapp.R;

/**
 * Created by EO NETWORKS on 03.12.2017.
 */

//klasa odpowiedzialna za odbiór streamu
public class StreamFragment extends Fragment implements  NavigationView.OnNavigationItemSelectedListener{

    //get_stream -> endpoint streamu || get_recorded -> endpoint nagrania
    //http potrzebny do komunikacji z restapi
    private String videoURL = "http://192.168.2.67:5000/get_stream";
    //zmienna przechowująca stream
    private MjpegView mjpegView1;
    //stała określająca możliwy czas na odbiór streamu
    private static final int TIMEOUT = 5;
    //przycisk odpowiedzialny za start i stop streamu
    private Button btnPlayPause;

    //metoda odpowiedzialna za wyświetlanie odpowiedniego fragmentu
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_stream, null);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        //definicja przyciusku
        btnPlayPause = (Button) view.findViewById(R.id.play_stop_btn);

        //podpięcie akcji na przycisk
        view.findViewById(R.id.play_stop_btn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                try {
                    //jeśli stream nie jest włączony to spróbuj go włączyć oraz ustaw tekst "Zatrzymaj stream" na przycisku
                    if (!mjpegView1.isStreaming()) {
                        loadIpCam();
                        btnPlayPause.setText(R.string.stop_stream);
                    } else { //jeśli stream jest włączony to go zatrzymaj
                        mjpegView1.stopPlayback();
                        mjpegView1.clearStream();
                        btnPlayPause.setText(R.string.start_stream);
                    }
                } catch (Exception ex) {

                }
            }
        });

        //definicja  obszaru zajmowanego przez stream
        mjpegView1 = (MjpegView) view.findViewById(R.id.mjpegViewDefault2);
        ButterKnife.bind(view);
    }



    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        return false;
    }

    private void loadIpCam() {
        //odbiór streamu, podanie zdefiniowanych parametrów poprzez metodę "open"
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
                        });
    }
    //okreżlenie orientacji aplikacji
    private DisplayMode calculateDisplayMode() {
        int orientation = getResources().getConfiguration().orientation;
        return orientation == Configuration.ORIENTATION_LANDSCAPE ?
                DisplayMode.FULLSCREEN : DisplayMode.FULLSCREEN;
    }
    //metoda na kliknięcie pauzy
    @Override
    public void onPause() {
        super.onPause();
        mjpegView1.stopPlayback();
    }


}