package pl.eti.pg.pkm.finalapp.fragments;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import pl.eti.pg.pkm.finalapp.Algorithm;
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
//klasa odpowiedzialna za sterowanie wyborem algorytmów
public class AlgorithmsFragment extends Fragment{

    //definicja adapteru przechowującego listę algorytmów
    private MyCustomAdapter dataAdapter = null;
    //definicja timer'a wysyłającego aktualną mapę algorytmów co sekundę do restapi
    private Timer timer;
    //retrofit dostosowuje interfejs Java do wywołań HTTP za pomocą adnotacji na zadeklarowanych metodach
    private Retrofit retrofit;
    //zmienna definiująca web service
    private MyWebService service;
    //mapa przechowująca poszczególne algorytmy -> klucz = nazwa algorytmu, wartość = False/True
    private Map<String, String> actualAlgortithmsMap;
    //URL Eti
    private final static String IP_ETI = "http://172.20.16.103:5000";

    //metoda odpowiedzialna za wyświetlanie odpowiedniego fragmentu
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_algorithms, null);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        //definicja wszystkich algorytmów oraz początkowe ustawienie ich wartości na False
        actualAlgortithmsMap = new HashMap<>();
        actualAlgortithmsMap.put("train", "False");
        actualAlgortithmsMap.put("depot", "False");
        actualAlgortithmsMap.put("face", "False");
        actualAlgortithmsMap.put("hand", "False");
        actualAlgortithmsMap.put("movement", "False");
        actualAlgortithmsMap.put("obstacles", "False");
        actualAlgortithmsMap.put("station", "False");


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

        //timer wysyłający aktualną listę wybranych algorytmów co sekundę do restapi
        timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                service.postAlgorithms(actualAlgortithmsMap).enqueue(new Callback<Map<String, String>>() {
                    @Override
                    public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {

                    }

                    @Override
                    public void onFailure(Call<Map<String, String>> call, Throwable t) {

                    }
                });
            }
        },0 , 1000);

        displayListView(view);
    }

    //wyświetlanie zaznaczonych algorytmów poprzez checkbox + nazwa algorytmu
    private void displayListView(View view) {

        //algorytmy są przechowywane na liście
        List<Algorithm> algorithmsList = new ArrayList<Algorithm>();

        //dodanie poszczególnych algorytmów oraz początkowe przypisanie im wartości false -> odznaczone
        Algorithm algorithms = new Algorithm("Zajezdnia", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Przeszkody", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Twarz", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Pociąg", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Perony", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Ruch ręką", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Ruch pociągu", false);
        algorithmsList.add(algorithms);

        //na podstawie listy algorytmów tworzone są checkboxy oraz przypisane im nazwy
        dataAdapter = new MyCustomAdapter(this.getContext(), R.layout.activity_listview, algorithmsList);
        ListView listView = view.findViewById(R.id.algorithmsListView);

        listView.setAdapter(dataAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Algorithm algorithms = (Algorithm) parent.getItemAtPosition(position);
            }
        });
    }

    //adapter tworzony do udostępniania widoków
    public class MyCustomAdapter extends ArrayAdapter<Algorithm> {
        //lista do przechowywanie algorytmów
        private ArrayList<Algorithm> algorithmsList;
        //aktualny context
        private Context adapterContext;

        public MyCustomAdapter(Context context, int textviewResourceId, List<Algorithm> algorithmsList) {
            super(context, textviewResourceId, algorithmsList);
            this.algorithmsList = new ArrayList<Algorithm>();
            this.algorithmsList.addAll(algorithmsList);
            this.adapterContext = context;
        }

        //prywatna klasa definiująca nazwy algorytmów do checkbox'ow
        private class ViewHolder {
            CheckBox name;
        }

        @NonNull
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {


            ViewHolder holder = null;
            Log.v("ConvertView", String.valueOf(position));
            if (convertView == null) {
                LayoutInflater vi = (LayoutInflater) adapterContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                //definicja listView czyli komponentu odpowiedzialnego za wyświetlanie listy
                convertView = vi.inflate(R.layout.activity_listview, null);

                holder = new ViewHolder();
                //odniesienie do checkboxa
                holder.name = convertView.findViewById(R.id.checkBox1);

                convertView.setTag(holder);
                //akcja na checkbox
                holder.name.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        CheckBox checkBox = (CheckBox) view;
                        //pobranie tagu checkbox'a i przypisanie go do algorytmu
                        Algorithm algorithm = (Algorithm) checkBox.getTag();
                        //zaznaczenie lub odnaczenie checkbox'a
                        algorithm.setSelected(checkBox.isChecked());
                        //pobieranie informacji o zaznaczonym lub odznacznym checkbox'ie i konwersja do Stringa
                        String actualBool = algorithm.getSelected().toString();
                        //zamiana true -> True oraz false -> False
                        actualBool = actualBool.substring(0,1).toUpperCase() + actualBool.substring(1).toLowerCase();
                        //aktualizacja listy
                        algorithmsMapUpdate(algorithm.getName(), actualBool);
                    }
                });
            } else {
                holder = (ViewHolder) convertView.getTag();
            }
            Algorithm algorithm = algorithmsList.get(position);
            //przypisanie tekstu
            holder.name.setText(algorithm.getName());
            //odznaczenie lub zaznaczenie
            holder.name.setChecked(algorithm.getSelected());
            //otagowanie
            holder.name.setTag(algorithm);

            return convertView;
        }
    }

    //metoda porównująca aktualnie wybrane algorytmy i aktualizacja mapy algorytmów
    public void algorithmsMapUpdate(String algorithm, String algorithmBool) {
        if (algorithm.equals("Zajezdnia")) {
            this.actualAlgortithmsMap.put("depot", algorithmBool);
        } else if (algorithm.equals("Przeszkody")) {
            this.actualAlgortithmsMap.put("obstacles", algorithmBool);
        } else if (algorithm.equals("Twarz")) {
            this.actualAlgortithmsMap.put("face", algorithmBool);
        } else if (algorithm.equals("Pociąg")) {
            this.actualAlgortithmsMap.put("train", algorithmBool);
        } else if (algorithm.equals("Perony")) {
            this.actualAlgortithmsMap.put("station", algorithmBool);
        } else if (algorithm.equals("Ruch ręką")) {
            this.actualAlgortithmsMap.put("hand", algorithmBool);
        } else if (algorithm.equals("Ruch pociągu")) {
            this.actualAlgortithmsMap.put("movement", algorithmBool);
        }
    }
}
