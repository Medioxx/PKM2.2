package pl.eti.pg.pkm.finalapp;

import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import java.util.Timer;

import pl.eti.pg.pkm.finalapp.fragments.AlgorithmsFragment;
import pl.eti.pg.pkm.finalapp.fragments.ControlFragment;
import pl.eti.pg.pkm.finalapp.fragments.StreamFragment;
import retrofit2.Retrofit;


//główna klasa programu odpowiedzialna za zarządzanie fragmentami i komunikację między nimi
public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    //komponent odpowiedzialny za tworzenie panelu bocznego
    private DrawerLayout drawer;
    //komponent defiuniujacy naglowek aplikacji
    private Toolbar toolbar;
    //komponent umieszczony w DrawerLayout, definiujący standardowe menu panelu bocznego
    private NavigationView navigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //ustawienie aktualnego layoutu, definiuje on NavigationView
        setContentView(R.layout.activity_main);
        //ustawienie właściwości toolbara
        toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        //definicja FragmentMenager'a jest on używany do zarządzania fragmenami
        FragmentManager fragmentManager = getSupportFragmentManager();
        //początkowo ustawiany jest fragment odpowiedzialny za odtwarzanie stream'u, oraz nadawany jest mu tag aby w łatwy sposób móc się do niego odnieść
        fragmentManager.beginTransaction().add(R.id.screen_area, new StreamFragment(), "stream_tag").commit();
        //definicja DrawerLayout czyli layoutu połączonego z menu bocznym
        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
    }

    //metoda pozwalająca używania przycisku cofania
    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    //metoda tworząca listę akcji dostępnych w prawym górnym, rozwijanym menu aplikacji
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    //metoda odpowiedzialna na reakcję w przypadku kliknięcia rozwijanego menu (prawy górny róg aplikacji) -> w naszym przypadku przycisk "Zakończ" zamyka aplikację
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_exit) {
            android.os.Process.killProcess(android.os.Process.myPid());
        }
        return super.onOptionsItemSelected(item);
    }


    //metoda wywoływana na wybór odpowiedniej sekcji z menu bocznego
    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        //pobieranie id, aktualnie wybranego fragmentu
        int id = item.getItemId();
        //odwołanie do FragmentManager'a
        FragmentManager fragmentManager = getSupportFragmentManager();

        //sprawdzanie id wybranego layoutu
        if (id == R.id.nav_stream) {
            //sprawdzenie czy nie został przypisany już tag to layoutu odpowiedzialnego za wyświetlanie streamu
            //jeśli tag istnieje to zostaje aktualnie wyświetlony
            if (fragmentManager.findFragmentByTag("stream_tag") != null) {
                fragmentManager.beginTransaction().show(fragmentManager.findFragmentByTag("stream_tag")).commit();
                setTitle(R.string.title_stream);
                //jeśli tag nie istnieje, jest tworzony
            } else {
                fragmentManager.beginTransaction().add(R.id.screen_area, new StreamFragment(), "stream_tag").commit();
                setTitle(R.string.title_stream);
            }
            //inne fragmenty niż w tym przypadku stream są chowane
            if (fragmentManager.findFragmentByTag("algorithms_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("algorithms_tag")).commit();
            }
            if (fragmentManager.findFragmentByTag("control_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("control_tag")).commit();
            }
            //analogiczna logika działa programu do pierwszego warunku
        } else if (id == R.id.nav_algorithms) {
            if (fragmentManager.findFragmentByTag("algorithms_tag") != null) {
                fragmentManager.beginTransaction().show(fragmentManager.findFragmentByTag("algorithms_tag")).commit();
                setTitle(R.string.title_algorithms);
            } else {
                fragmentManager.beginTransaction().add(R.id.screen_area, new AlgorithmsFragment(), "algorithms_tag").commit();
                setTitle(R.string.title_algorithms);
            }
            if (fragmentManager.findFragmentByTag("stream_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("stream_tag")).commit();
            }
            if (fragmentManager.findFragmentByTag("control_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("control_tag")).commit();
            }
        } else if (id == R.id.nav_control) {
            if (fragmentManager.findFragmentByTag("control_tag") != null) {
                fragmentManager.beginTransaction().show(fragmentManager.findFragmentByTag("control_tag")).commit();
                setTitle(R.string.title_control);
            } else {
                fragmentManager.beginTransaction().add(R.id.screen_area, new ControlFragment(), "control_tag").commit();
                setTitle(R.string.title_control);
            }
            if (fragmentManager.findFragmentByTag("stream_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("stream_tag")).commit();
            }
            if (fragmentManager.findFragmentByTag("algorithms_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("algorithms_tag")).commit();
            }
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

}
