package pl.eti.pg.pkm.finalapp.fragments;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Map;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import pl.eti.pg.pkm.finalapp.MyWebService;
import pl.eti.pg.pkm.finalapp.R;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by EO NETWORKS on 03.12.2017.
 */
//klasa odpowiedzialna za sterowanie pociągiem, jego prędkością oraz siecią neuronową
public class ControlFragment extends Fragment {

    //retrofit dostosowuje interfejs Java do wywołań HTTP za pomocą adnotacji na zadeklarowanych metodach
    private Retrofit retrofit;
    //zmienna definiująca web service
    private MyWebService service;
    //mapa przechowująca poszczególne algorytmy -> klucz = ruch pociągu/prędkość, wartość = żądany ruch/prędkość
    private Map<String, String> actualControlMap;
    //definicja tekstu pokazującego szybkość pociągu
    private TextView velocityTextView;
    //komponent do sterowania szybkością pociągu
    private SeekBar seekBar;
    //definicja początkowej wartości seekbar'u
    private int progress = 7;
    //URL Eti
    private final static String IP_ETI = "http://172.20.16.103:5000";

    //metoda odpowiedzialna za wyświetlanie odpowiedniego fragmentu
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_control, null);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        //defincja odpowiedniego tekstu dla prędkości
        velocityTextView = (TextView) view.findViewById(R.id.velocity_text);
        //defincja seekbar
        seekBar = (SeekBar) view.findViewById(R.id.seekbar_control);
        //ustawienie wielkości wyświetlanego tekstu
        velocityTextView.setTextSize(24);
        //Przedstawienie aktualnej prędkości pociągu
        velocityTextView.setText("Podana prędkość: " + progress);
        //ustawienie maksymalnej prędkości na 14
        seekBar.setMax(14);
        seekBar.setProgress(progress);
        //definicja mapy w której będzie przesyłany ruch pociągu (cofanie -> -1, stop -> 0, jazda w przód -> 1) oraz prędkość
        actualControlMap = new HashMap<>();
        actualControlMap.put("control", "0");
        actualControlMap.put("velocity", "0");

        //definicja fabryki uzywanej do połączenia, za pomocą której można wysyłać żądania HTTP i odczytywać ich odpowiedzi
        OkHttpClient.Builder okHttpClientBuilder = new OkHttpClient.Builder();
        HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
        logging.setLevel(HttpLoggingInterceptor.Level.BODY);
        okHttpClientBuilder.addInterceptor(logging);
        //budowanie URL i komunikacja z restapi
        retrofit = new Retrofit.Builder()
                .baseUrl(IP_ETI)
                .client(okHttpClientBuilder.build())
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        //tworzenie web serwisu
        service = retrofit.create(MyWebService.class);

        //event na zmianę wartości seekbar
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                progress = i;
                velocityTextView.setTextSize(24);
                velocityTextView.setText("Podana prędkość: " + progress);

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
        //definicja akcji na przycisk cofania
        view.findViewById(R.id.backwardBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actualControlMap.put("control", "-1");
                actualControlMap.put("velocity", Integer.toString(progress));
                service.postControl(actualControlMap).enqueue(new Callback<Map<String, String>>() {
                    @Override
                    public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {

                    }

                    @Override
                    public void onFailure(Call<Map<String, String>> call, Throwable t) {

                    }
                });
            }
        });
        //definicja akcji na przycisk jazdy w przód
        view.findViewById(R.id.forwardBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actualControlMap.put("control", "1");
                actualControlMap.put("velocity", Integer.toString(progress));
                service.postControl(actualControlMap).enqueue(new Callback<Map<String, String>>() {
                    @Override
                    public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {

                    }

                    @Override
                    public void onFailure(Call<Map<String, String>> call, Throwable t) {

                    }
                });
            }
        });
        //definicja akcji na przycisk stop
        view.findViewById(R.id.stopBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                actualControlMap.put("control", "0");
                actualControlMap.put("velocity", "0");
                service.postControl(actualControlMap).enqueue(new Callback<Map<String, String>>() {
                    @Override
                    public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {

                    }

                    @Override
                    public void onFailure(Call<Map<String, String>> call, Throwable t) {

                    }
                });
            }
        });
        //definicja akcji na przycisk sieci neuronowej
        view.findViewById(R.id.neuroneBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                service.postNeural().enqueue(new Callback<Void>() {
                    @Override
                    public void onResponse(Call<Void> call, Response<Void> response) {

                    }

                    @Override
                    public void onFailure(Call<Void> call, Throwable t) {

                    }
                });
            }
        });
    }



}
