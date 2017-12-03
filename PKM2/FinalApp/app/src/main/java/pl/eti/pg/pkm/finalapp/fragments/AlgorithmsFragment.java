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
import java.util.List;

import pl.eti.pg.pkm.finalapp.Algorithm;
import pl.eti.pg.pkm.finalapp.R;

/**
 * Created by EO NETWORKS on 03.12.2017.
 */

public class AlgorithmsFragment extends Fragment{

    private MyCustomAdapter dataAdapter = null;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_algorithms, null);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        displayListView(view);
    }

    private void displayListView(View view) {

        List<Algorithm> algorithmsList = new ArrayList<Algorithm>();

        Algorithm algorithms = new Algorithm("Zajezdnia", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Przeszkody", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Twarz", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Banan", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Perony", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Ruch ręką", false);
        algorithmsList.add(algorithms);
        algorithms = new Algorithm("Ruch pociągu", false);
        algorithmsList.add(algorithms);

        dataAdapter = new MyCustomAdapter(this.getContext(), R.layout.activity_listview, algorithmsList);
        ListView listView = view.findViewById(R.id.algorithmsListView);

        listView.setAdapter(dataAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Algorithm algorithms = (Algorithm) parent.getItemAtPosition(position);
//                if(algorithms.isSelected() == true)
//                    Toast.makeText(getApplicationContext(), "Wybrano algorytm: " + algorithms.getName(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    public class MyCustomAdapter extends ArrayAdapter<Algorithm> {
        private ArrayList<Algorithm> algorithmsList;

        private Context adapterContext;

        public MyCustomAdapter(Context context, int textviewResourceId, List<Algorithm> algorithmsList) {
            super(context, textviewResourceId, algorithmsList);
            this.algorithmsList = new ArrayList<Algorithm>();
            this.algorithmsList.addAll(algorithmsList);
            this.adapterContext = context;
        }

        private class ViewHolder {
            CheckBox name;

        }


        //akcja na checkboxa
        @NonNull
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {


            ViewHolder holder = null;
            Log.v("ConvertView", String.valueOf(position));
            if (convertView == null) {
                LayoutInflater vi = (LayoutInflater) adapterContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                convertView = vi.inflate(R.layout.activity_listview, null);

                holder = new ViewHolder();
                holder.name = convertView.findViewById(R.id.checkBox1);

                convertView.setTag(holder);

                holder.name.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        CheckBox checkBox = (CheckBox) view;
                        Algorithm algorithms = (Algorithm) checkBox.getTag();
                        algorithms.setSelected(checkBox.isChecked());
                    }
                });
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            Algorithm algorithm = algorithmsList.get(position);
            holder.name.setText(algorithm.getName());
            holder.name.setChecked(algorithm.isSelected());
            holder.name.setTag(algorithm);

            return convertView;
        }
    }
}
