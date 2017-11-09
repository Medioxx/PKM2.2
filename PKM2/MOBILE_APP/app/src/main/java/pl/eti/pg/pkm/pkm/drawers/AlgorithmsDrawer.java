package pl.eti.pg.pkm.pkm.drawers;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

import pl.eti.pg.pkm.pkm.Algorithm;
import pl.eti.pg.pkm.pkm.R;

public class AlgorithmsDrawer extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    DrawerLayout drawer;
    NavigationView navigationView;
    Toolbar toolbar = null;
    private MyCustomAdapter dataAdapter = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_algorithms_drawer);

        displayListView();
        checkButtonClick();

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
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
                Intent streamIntent = new Intent(AlgorithmsDrawer.this, StreamDrawer.class);
                startActivity(streamIntent);
                break;
            case R.id.nav_algorithms:
                Intent algorithmsIntent = new Intent(AlgorithmsDrawer.this, AlgorithmsDrawer.class);
                startActivity(algorithmsIntent);
                break;
            case R.id.nav_control:
                Intent controlIntent = new Intent(AlgorithmsDrawer.this, ControlDrawer.class);
                startActivity(controlIntent);
                break;
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    private void displayListView() {

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

        dataAdapter = new MyCustomAdapter(this, R.layout.activity_listview, algorithmsList);
        ListView listView = (ListView) findViewById(R.id.listView1);

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

        public MyCustomAdapter(Context context, int textviewResourceId, List<Algorithm> algorithmsList) {
            super(context, textviewResourceId, algorithmsList);
            this.algorithmsList = new ArrayList<Algorithm>();
            this.algorithmsList.addAll(algorithmsList);
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
                LayoutInflater vi = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
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

    private void checkButtonClick() {
        Button myButton = (Button) findViewById(R.id.findSelected);
        myButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                StringBuffer responseText = new StringBuffer();
                responseText.append("Wybrane algorytmy:");
                int counter = 0;
                ArrayList<Algorithm> algorithmsArrayList = dataAdapter.algorithmsList;

                for(int i = 0; i < algorithmsArrayList.size(); i++) {
                    Algorithm algorithm = algorithmsArrayList.get(i);

                    if (algorithm.isSelected()) {
                        responseText.append("\n" + algorithm.getName());
                        counter++;
                    }
                }
                if (counter == 0) {
                    Toast.makeText(getApplicationContext(), "Nie wybrano algorytmu", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getApplicationContext(), responseText, Toast.LENGTH_LONG).show();
                }
                counter = 0;
            }
        });
    }
}
