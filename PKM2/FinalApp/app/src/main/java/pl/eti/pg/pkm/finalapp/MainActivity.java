package pl.eti.pg.pkm.finalapp;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import pl.eti.pg.pkm.finalapp.fragments.AlgorithmsFragment;
import pl.eti.pg.pkm.finalapp.fragments.ControlFragment;
import pl.eti.pg.pkm.finalapp.fragments.StreamFragment;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener{

    private DrawerLayout drawer;
    private Toolbar toolbar;
    private NavigationView navigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FragmentManager fragmentManager = getSupportFragmentManager();
        fragmentManager.beginTransaction().add(R.id.screen_area, new StreamFragment(), "stream_tag").commit();

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
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_exit) {
            android.os.Process.killProcess(android.os.Process.myPid());
        }
        return super.onOptionsItemSelected(item);
    }


    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        int id = item.getItemId();
        FragmentManager fragmentManager = getSupportFragmentManager();

        if (id == R.id.nav_stream) {
            if (fragmentManager.findFragmentByTag("stream_tag") != null) {
                fragmentManager.beginTransaction().show(fragmentManager.findFragmentByTag("stream_tag")).commit();
                setTitle(R.string.title_stream);
            } else {
                fragmentManager.beginTransaction().add(R.id.screen_area, new StreamFragment(), "stream_tag").commit();
                setTitle(R.string.title_stream);
            }
            if (fragmentManager.findFragmentByTag("algorithms_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("algorithms_tag")).commit();
            }
            if (fragmentManager.findFragmentByTag("control_tag") != null) {
                fragmentManager.beginTransaction().hide(fragmentManager.findFragmentByTag("control_tag")).commit();
            }
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
